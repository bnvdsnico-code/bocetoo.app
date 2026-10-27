// Ingreso de alumnos con Google (OpenID Connect) y control de acceso a las clases.
// - /auth/google: lleva a Google con un "state" de un solo uso (cookie) para evitar falsificaciones.
// - /auth/callback: canjea el código en Google (servidor a servidor), toma el email verificado y abre una sesión.
// - Sesión: cookie HttpOnly + Secure con un id aleatorio; los datos viven en KV ("sess:<id>").
// - Acceso: una clase se ve si el email del alumno tiene una suscripción "authorized" que la incluya.

import type { MpEnv } from "./suscripciones";

export interface AuthEnv extends MpEnv { GOOGLE_CLIENT_ID?: string; GOOGLE_CLIENT_SECRET?: string }

const SESSION_COOKIE = "boceto_sesion";
const STATE_COOKIE = "boceto_estado";
const SESSION_DAYS = 30;
const CARRERAS = new Set(["interiores", "industrial", "grafico", "indumentaria"]);

const randomId = (n = 24) => [...crypto.getRandomValues(new Uint8Array(n))].map((b) => b.toString(16).padStart(2, "0")).join("");
const appUrl = (env: AuthEnv, req: Request) => (env.APP_URL || new URL(req.url).origin).replace(/\/+$/, "");
export const googleReady = (env: AuthEnv) => !!(env.GOOGLE_CLIENT_ID && env.GOOGLE_CLIENT_SECRET);
const redirectUri = (env: AuthEnv, req: Request) => `${new URL(req.url).origin}/auth/callback`;

function cookies(req: Request) {
  const out: Record<string, string> = {};
  for (const part of (req.headers.get("cookie") || "").split(";")) {
    const i = part.indexOf("=");
    if (i > 0) out[part.slice(0, i).trim()] = decodeURIComponent(part.slice(i + 1).trim());
  }
  return out;
}
const cookie = (name: string, value: string, maxAge: number) =>
  `${name}=${encodeURIComponent(value)}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAge}`;

// Solo rutas internas del sitio como destino de vuelta (evita redirecciones abiertas).
const safePath = (p: string | null) => (p && /^\/[A-Za-z0-9/_\-.?=&%]*$/.test(p) && !p.startsWith("//") ? p : "/panel.html");

function redirect(location: string, setCookies: string[] = []) {
  const h = new Headers({ Location: location, "Cache-Control": "no-store" });
  for (const c of setCookies) h.append("Set-Cookie", c);
  return new Response(null, { status: 302, headers: h });
}

/* GET /auth/google?volver=/ruta */
export async function authStart(req: Request, env: AuthEnv) {
  if (!googleReady(env) || !env.SUSCRIPCIONES) return new Response("El ingreso con Google todavía no está configurado.", { status: 503 });
  const volver = safePath(new URL(req.url).searchParams.get("volver"));
  const state = randomId(16);
  await env.SUSCRIPCIONES.put(`estado:${state}`, volver, { expirationTtl: 600 });
  const q = new URLSearchParams({
    client_id: env.GOOGLE_CLIENT_ID!, redirect_uri: redirectUri(env, req), response_type: "code",
    scope: "openid email profile", state, prompt: "select_account"
  });
  return redirect(`https://accounts.google.com/o/oauth2/v2/auth?${q}`, [cookie(STATE_COOKIE, state, 600)]);
}

/* GET /auth/callback?code&state */
export async function authCallback(req: Request, env: AuthEnv) {
  if (!env.GOOGLE_CLIENT_ID || !env.GOOGLE_CLIENT_SECRET || !env.SUSCRIPCIONES) return new Response("Ingreso no configurado.", { status: 503 });
  const url = new URL(req.url);
  const code = url.searchParams.get("code"), state = url.searchParams.get("state") || "";
  if (!code || !state || cookies(req)[STATE_COOKIE] !== state) return redirect("/acceso.html?error=estado");
  const volver = await env.SUSCRIPCIONES.get(`estado:${state}`);
  if (!volver) return redirect("/acceso.html?error=estado");
  await env.SUSCRIPCIONES.delete(`estado:${state}`);

  // Canje del código directamente con Google (TLS): el id_token recibido así es confiable.
  const res = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST", headers: { "content-type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ code, client_id: env.GOOGLE_CLIENT_ID, client_secret: env.GOOGLE_CLIENT_SECRET, redirect_uri: redirectUri(env, req), grant_type: "authorization_code" })
  }).catch(() => null);
  const data: any = res && res.ok ? await res.json().catch(() => null) : null;
  if (!data?.id_token) { console.error("auth: canje rechazado", res?.status ?? 0); return redirect("/acceso.html?error=google"); }
  let claims: any = null;
  try {
    const bin = atob(data.id_token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/"));
    claims = JSON.parse(new TextDecoder().decode(Uint8Array.from(bin, (c) => c.charCodeAt(0))));
  } catch { /* inválido */ }
  const issOk = claims && (claims.iss === "https://accounts.google.com" || claims.iss === "accounts.google.com");
  if (!claims || !issOk || claims.aud !== env.GOOGLE_CLIENT_ID || !claims.email || claims.email_verified !== true || claims.exp * 1000 < Date.now()) {
    return redirect("/acceso.html?error=google");
  }
  const sid = randomId();
  const sesion = { email: String(claims.email).toLowerCase(), nombre: claims.name || "", foto: claims.picture || "", creada: new Date().toISOString() };
  await env.SUSCRIPCIONES.put(`sess:${sid}`, JSON.stringify(sesion), { expirationTtl: SESSION_DAYS * 86400 });
  // Ficha del alumno para el panel de administración (primer y último ingreso)
  const previo = JSON.parse((await env.SUSCRIPCIONES.get(`usuario:${sesion.email}`)) || "null");
  await env.SUSCRIPCIONES.put(`usuario:${sesion.email}`, JSON.stringify({ email: sesion.email, nombre: sesion.nombre, foto: sesion.foto, primerIngreso: previo?.primerIngreso || sesion.creada, ultimoIngreso: sesion.creada }));
  return redirect(volver, [cookie(SESSION_COOKIE, sid, SESSION_DAYS * 86400), cookie(STATE_COOKIE, "", 0)]);
}

/* GET /auth/salir */
export async function authLogout(req: Request, env: AuthEnv) {
  const sid = cookies(req)[SESSION_COOKIE];
  if (sid && env.SUSCRIPCIONES) await env.SUSCRIPCIONES.delete(`sess:${sid}`);
  return redirect("/", [cookie(SESSION_COOKIE, "", 0)]);
}

export async function currentSession(req: Request, env: AuthEnv): Promise<{ email: string; nombre: string; foto: string } | null> {
  const sid = cookies(req)[SESSION_COOKIE];
  if (!sid || !/^[a-f0-9]{48}$/.test(sid) || !env.SUSCRIPCIONES) return null;
  const raw = await env.SUSCRIPCIONES.get(`sess:${sid}`);
  return raw ? JSON.parse(raw) : null;
}

/* Diplomaturas habilitadas para un email: según sus suscripciones activas. */
export async function accessFor(env: AuthEnv, email: string) {
  const kv = env.SUSCRIPCIONES!;
  const ids: string[] = JSON.parse((await kv.get(`email:${email}`)) || "[]");
  const carreras = new Set<string>();
  const suscripciones: Array<{ id: string; plan: string; carrera: string | null; status: string; matricula: string | null }> = [];
  for (const id of ids) {
    const raw = await kv.get(`sub:${id}`);
    if (!raw) continue;
    const s = JSON.parse(raw);
    suscripciones.push({ id, plan: s.plan, carrera: s.carrera, status: s.status, matricula: s.matricula || null });
    if (s.status !== "authorized") continue;
    if (s.plan === "todas") CARRERAS.forEach((c) => carreras.add(c));
    else if (s.carrera) carreras.add(s.carrera);
  }
  return { carreras: [...carreras], suscripciones };
}

/* GET /api/yo: sesión y accesos del alumno (sin datos sensibles) */
export async function me(req: Request, env: AuthEnv) {
  const s = await currentSession(req, env);
  const body = s ? { ingresado: true, email: s.email, nombre: s.nombre, foto: s.foto, ...(await accessFor(env, s.email)) } : { ingresado: false, googleListo: googleReady(env) };
  return new Response(JSON.stringify(body), { headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
}

/* Clases: la primera de cada diplomatura es libre; el resto requiere suscripción activa. */
// También cubre las direcciones sin ".html" (Cloudflare las sirve igual).
const CLASE = /^\/cursos\/(interiores|industrial|grafico|indumentaria)\/semana-(\d\d)\/clase-(\d)(?:\.html)?\/?$/i;
export async function guardClass(req: Request, env: AuthEnv, serve: () => Promise<Response>): Promise<Response | null> {
  const path = decodeURIComponent(new URL(req.url).pathname);
  const m = path.match(CLASE);
  if (!m) return null;                                // no es una clase: sigue el camino normal
  const [, carreraRaw, semana, clase] = m;
  const carrera = carreraRaw.toLowerCase();
  if (semana === "01" && clase === "1") return null; // clase de prueba gratis
  const s = await currentSession(req, env);
  const permitido = s ? (await accessFor(env, s.email)).carreras.includes(carrera) : false;
  if (!permitido) {
    const q = new URLSearchParams({ carrera, volver: path, ...(s ? { motivo: "sin-suscripcion" } : {}) });
    return redirect(`/acceso.html?${q}`);
  }
  const res = await serve();
  const out = new Response(res.body, res);
  out.headers.set("Cache-Control", "private, no-store");
  return out;
}

// Asocia una suscripción nueva al email del alumno (lista de ids por email).
export async function linkSubscription(env: MpEnv, email: string, id: string) {
  const kv = env.SUSCRIPCIONES!;
  const ids: string[] = JSON.parse((await kv.get(`email:${email}`)) || "[]");
  if (!ids.includes(id)) ids.push(id);
  await kv.put(`email:${email}`, JSON.stringify(ids));
}

export { appUrl as _appUrl };
