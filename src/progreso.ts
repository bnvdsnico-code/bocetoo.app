// Progreso del alumno guardado en su cuenta (así lo ve en cualquier dispositivo).
// - GET  /api/progreso                     → clases completadas, entregas y última clase vista
// - PUT  /api/progreso                     → guarda lo que manda el navegador (las clases por diplomatura se reemplazan;
//                                            las entregas se combinan y gana la más reciente)
// - GET/PUT /api/progreso/img/:carrera/:clase → imagen de una entrega (JPEG en data URL, hasta 1,5 MB)
// Todo requiere sesión iniciada con Google. KV: "prog:<email>" e "img:<email>:<carrera>:<clase>".

import { currentSession, type AuthEnv } from "./auth";

const CARRERAS = ["interiores", "industrial", "grafico", "indumentaria"];
const CID = /^s(0[1-9]|1[0-6])d[1-5]$/;
const MAX_IMG = 1_500_000;
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "private, no-store" } });
const str = (v: unknown, max: number) => (typeof v === "string" ? v.slice(0, max) : "");

type Entrega = { carrera: string; clase: string; t: string; k: string; u: string; e: boolean; fecha: string; resumen: string; corregir: number | null; img?: boolean };
type Progreso = { progreso: Record<string, string[]>; entregas: Record<string, Entrega>; ultima: { carrera: string; clase: string; fecha: string } | null; actualizado: string };

const vacio = (): Progreso => ({ progreso: {}, entregas: {}, ultima: null, actualizado: "" });
const key = (email: string) => `prog:${email}`;

async function load(env: AuthEnv, email: string): Promise<Progreso> {
  const raw = await env.SUSCRIPCIONES!.get(key(email));
  try { return raw ? { ...vacio(), ...JSON.parse(raw) } : vacio(); } catch { return vacio(); }
}

function cleanEntrega(v: any): Entrega | null {
  if (!v || !CARRERAS.includes(v.carrera) || !CID.test(v.clase) || !v.fecha || isNaN(Date.parse(v.fecha))) return null;
  const u = str(v.u, 120);
  return {
    carrera: v.carrera, clase: v.clase, t: str(v.t, 160), k: str(v.k, 80), u: u.startsWith("/cursos/") ? u : "",
    e: !!v.e, fecha: new Date(v.fecha).toISOString(), resumen: str(v.resumen, 600),
    corregir: Number.isInteger(v.corregir) && v.corregir >= 0 && v.corregir < 100 ? v.corregir : null
  };
}

export async function progreso(req: Request, env: AuthEnv, sub: string): Promise<Response> {
  if (!env.SUSCRIPCIONES) return json({ error: "no_configurado" }, 503);
  const s = await currentSession(req, env);
  if (!s) return json({ error: "sin_sesion" }, 401);

  // Imagen de una entrega
  const mi = sub.match(/^\/img\/([a-z]+)\/(s\d\dd\d)$/);
  if (mi) {
    const [, carrera, clase] = mi;
    if (!CARRERAS.includes(carrera) || !CID.test(clase)) return json({ error: "no_encontrado" }, 404);
    const k = `img:${s.email}:${carrera}:${clase}`;
    if (req.method === "GET") {
      const data = await env.SUSCRIPCIONES.get(k);
      const m = data && data.match(/^data:image\/jpeg;base64,([A-Za-z0-9+/=]+)$/);
      if (!m) return json({ error: "no_encontrado" }, 404);
      const bytes = Uint8Array.from(atob(m[1]), (c) => c.charCodeAt(0));
      return new Response(bytes, { headers: { "content-type": "image/jpeg", "cache-control": "private, max-age=300" } });
    }
    if (req.method === "PUT") {
      const body = await req.text();
      if (body.length > MAX_IMG || !/^data:image\/jpeg;base64,[A-Za-z0-9+/=]+$/.test(body)) return json({ error: "imagen_invalida" }, 400);
      await env.SUSCRIPCIONES.put(k, body);
      const p = await load(env, s.email);
      const e = Object.values(p.entregas).find((x) => x.carrera === carrera && x.clase === clase);
      if (e && !e.img) { e.img = true; await env.SUSCRIPCIONES.put(key(s.email), JSON.stringify(p)); }
      return json({ ok: true });
    }
    return json({ error: "method_not_allowed" }, 405);
  }
  if (sub !== "") return json({ error: "not_found" }, 404);

  if (req.method === "GET") return json(await load(env, s.email));
  if (req.method !== "PUT") return json({ error: "method_not_allowed" }, 405);

  const raw = await req.text();
  if (raw.length > 200_000) return json({ error: "demasiado_grande" }, 413);
  let body: any;
  try { body = JSON.parse(raw); } catch { return json({ error: "json_invalido" }, 400); }
  const p = await load(env, s.email);

  if (body.progreso && typeof body.progreso === "object") {
    for (const c of CARRERAS) {
      const v = body.progreso[c];
      if (Array.isArray(v)) p.progreso[c] = [...new Set(v.filter((x: unknown) => typeof x === "string" && CID.test(x)))].slice(0, 80);
    }
  }
  if (body.entregas && typeof body.entregas === "object") {
    for (const v of Object.values(body.entregas).slice(0, 400)) {
      const e = cleanEntrega(v);
      if (!e) continue;
      const k = `${e.carrera}:${e.clase}`;
      const prev = p.entregas[k];
      if (!prev || prev.fecha < e.fecha) p.entregas[k] = { ...e, img: prev && prev.fecha === e.fecha ? prev.img : false };
    }
  }
  const u = body.ultima;
  if (u && CARRERAS.includes(u.carrera) && CID.test(u.clase) && !isNaN(Date.parse(u.fecha))) {
    const fecha = new Date(u.fecha).toISOString();
    if (!p.ultima || p.ultima.fecha < fecha) p.ultima = { carrera: u.carrera, clase: u.clase, fecha };
  }
  p.actualizado = new Date().toISOString();
  await env.SUSCRIPCIONES.put(key(s.email), JSON.stringify(p));
  return json(p);
}
