// Certificados de finalización.
// - GET  /api/certificados               → por diplomatura: clases hechas, si se puede emitir y el certificado si ya existe
// - POST /api/certificados/:carrera      → emite el certificado (80/80 clases en la cuenta + haber estado suscripto)
// - GET  /certificado/:id                → página pública para ver, imprimir/guardar en PDF y verificar
// KV: "cert:<id>" (datos) y "certs:<email>" (ids por diplomatura).

import { currentSession, type AuthEnv } from "./auth";
import { avisar } from "./avisos";

const CARRERAS: Record<string, { titulo: string; col: string; soft: string }> = {
  interiores: { titulo: "Diseño de Interiores y Mobiliario", col: "#C2410C", soft: "#FBE7DC" },
  industrial: { titulo: "Diseño Industrial", col: "#1D4ED8", soft: "#E3ECFF" },
  grafico: { titulo: "Diseño Gráfico", col: "#6D28D9", soft: "#EEE7FD" },
  indumentaria: { titulo: "Diseño de Indumentaria", col: "#BE185D", soft: "#FCE7F1" }
};
const TOTAL = 80;
const CID = /^s(0[1-9]|1[0-6])d[1-5]$/;
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "private, no-store" } });
const esc = (s: string) => s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));
const nuevoId = () => {
  const abc = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"; // sin letras ni números que se confundan
  return [...crypto.getRandomValues(new Uint8Array(10))].map((b) => abc[b % abc.length]).join("").replace(/^(.{5})/, "$1-");
};

type Cert = { id: string; carrera: string; nombre: string; email: string; fecha: string };

async function estado(env: AuthEnv, email: string) {
  const kv = env.SUSCRIPCIONES!;
  const prog = JSON.parse((await kv.get(`prog:${email}`)) || "{}");
  const ids: string[] = JSON.parse((await kv.get(`email:${email}`)) || "[]");
  const pagadas = new Set<string>();
  for (const id of ids) {
    const raw = await kv.get(`sub:${id}`);
    if (!raw) continue;
    const s = JSON.parse(raw);
    if (!s.status || s.status === "pending") continue; // nunca se cobró
    if (s.plan === "todas") Object.keys(CARRERAS).forEach((c) => pagadas.add(c));
    else if (s.carrera) pagadas.add(s.carrera);
  }
  const mios: Record<string, string> = JSON.parse((await kv.get(`certs:${email}`)) || "{}");
  const out: Record<string, { hechas: number; total: number; suscripto: boolean; puede: boolean; certificado: Cert | null }> = {};
  for (const c of Object.keys(CARRERAS)) {
    const hechas = new Set(((prog.progreso || {})[c] || []).filter((x: string) => CID.test(x))).size;
    const certRaw = mios[c] ? await kv.get(`cert:${mios[c]}`) : null;
    const certificado = certRaw ? JSON.parse(certRaw) : null;
    out[c] = { hechas, total: TOTAL, suscripto: pagadas.has(c), puede: !certificado && hechas >= TOTAL && pagadas.has(c), certificado };
  }
  return { out, mios };
}

export async function certificados(req: Request, env: AuthEnv, sub: string): Promise<Response> {
  if (!env.SUSCRIPCIONES) return json({ error: "no_configurado" }, 503);
  const s = await currentSession(req, env);
  if (!s) return json({ error: "sin_sesion", message: "Ingresá con Google para ver tus certificados." }, 401);

  if (sub === "" && req.method === "GET") return json({ nombre: s.nombre, carreras: (await estado(env, s.email)).out });

  const m = sub.match(/^\/([a-z]+)$/);
  if (!m || !CARRERAS[m[1]]) return json({ error: "not_found" }, 404);
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);
  const carrera = m[1];
  let body: any = {};
  try { body = await req.json(); } catch { /* sin cuerpo */ }
  const nombre = String(body.nombre || s.nombre || "").replace(/<[^>]*>/g, "").replace(/[\u0000-\u001f<>]/g, " ").replace(/\s+/g, " ").trim().slice(0, 80);
  if (nombre.length < 3) return json({ error: "nombre", message: "Escribí tu nombre completo como querés que figure en el certificado." }, 400);

  const { out, mios } = await estado(env, s.email);
  const e = out[carrera];
  if (e.certificado) return json({ certificado: e.certificado });
  if (!e.suscripto) return json({ error: "sin_suscripcion", message: "El certificado es para quienes cursaron la diplomatura con una suscripción." }, 403);
  if (e.hechas < TOTAL) return json({ error: "incompleto", message: `Te faltan ${TOTAL - e.hechas} clases para terminar la diplomatura.` }, 409);

  const cert: Cert = { id: nuevoId(), carrera, nombre, email: s.email, fecha: new Date().toISOString() };
  await env.SUSCRIPCIONES.put(`cert:${cert.id}`, JSON.stringify(cert));
  mios[carrera] = cert.id;
  await env.SUSCRIPCIONES.put(`certs:${s.email}`, JSON.stringify(mios));
  await avisar(env, `Certificado emitido · ${CARRERAS[carrera].titulo}`, `${nombre} (${s.email}) terminó ${CARRERAS[carrera].titulo}.\nCertificado: https://bocetoo.app/certificado/${cert.id}`);
  return json({ certificado: cert }, 201);
}

/* GET /certificado/:id — página pública del certificado */
export async function paginaCertificado(env: AuthEnv, id: string): Promise<Response> {
  const raw = /^[A-Z2-9]{5}-[A-Z2-9]{5}$/.test(id) && env.SUSCRIPCIONES ? await env.SUSCRIPCIONES.get(`cert:${id}`) : null;
  const html = (titulo: string, cuerpo: string, status = 200) => new Response(`<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(titulo)}</title><meta name="robots" content="noindex"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&amp;family=Inter:wght@400;500;600&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/certificado.css"></head><body>${cuerpo}</body></html>`,
    { status, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "public, max-age=300" } });

  if (!raw) return html("Certificado no encontrado · boceto", `<main class="nf"><a class="brand" href="/"><span class="marks" aria-hidden="true"><i></i><i></i><i></i><i></i></span>boceto</a><h1>No encontramos ese certificado</h1><p>Revisá que el código esté bien escrito. Los certificados de boceto tienen un código como <b>ABCDE-12345</b>.</p></main>`, 404);

  const c: Cert = JSON.parse(raw);
  const k = CARRERAS[c.carrera];
  const fecha = new Date(c.fecha).toLocaleDateString("es-AR", { day: "numeric", month: "long", year: "numeric", timeZone: "America/Argentina/Buenos_Aires" });
  const url = `bocetoo.app/certificado/${c.id}`;
  return html(`Certificado de ${c.nombre} · ${k.titulo} · boceto`, `
<div class="tools"><a href="/panel.html">← Mi panel</a><button type="button" onclick="window.print()">Imprimir o guardar en PDF</button></div>
<main class="cert" style="--c:${k.col};--soft:${k.soft}">
  <div class="band" aria-hidden="true"></div>
  <header><span class="brand"><span class="marks" aria-hidden="true"><i></i><i></i><i></i><i></i></span>boceto</span><span class="kind">Certificado de finalización</span></header>
  <section class="body">
    <p class="lead">Certificamos que</p>
    <h1>${esc(c.nombre)}</h1>
    <p class="lead">completó la diplomatura</p>
    <h2>${esc(k.titulo)}</h2>
    <p class="meta">16 semanas · 80 clases · 80 horas de cursada online</p>
  </section>
  <footer>
    <div><span class="lbl">Fecha</span><b>${fecha}</b></div>
    <div><span class="lbl">Código</span><b>${c.id}</b></div>
    <div class="ver"><span class="lbl">Verificá este certificado en</span><b>${url}</b></div>
  </footer>
  <p class="nota">boceto · escuela de diseño online. Curso libre de formación: no es un título oficial.</p>
</main>`);
}
