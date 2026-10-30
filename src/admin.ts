// Panel de administración (solo para las cuentas de Google listadas en ADMINS).
// - GET  /api/admin/resumen                      → alumnos, suscripciones, avance, solicitudes y certificados
// - POST /api/admin/solicitudes/:codigo          → { estado: "atendida" | "recibida", nota? }
// - POST /api/admin/pruebas                       → { email, dias, carreras: ["todas"] | [...] } da acceso de prueba
// - DELETE /api/admin/pruebas/:email              → quita el acceso de prueba
// Lee todo de KV con list(); pensado para decenas o cientos de alumnos.

import { currentSession, type AuthEnv } from "./auth";

const PRECIOS: Record<string, number> = { diplomatura: 63000, todas: 83000 };
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "private, no-store" } });

const admins = (env: any) => String(env.ADMINS || "bnvds.nico@gmail.com").toLowerCase().split(/[,\s]+/).filter(Boolean);

async function todas(env: AuthEnv, prefix: string) {
  const kv: any = env.SUSCRIPCIONES;
  const out: Array<{ key: string; value: any }> = [];
  let cursor: string | undefined;
  do {
    const page = await kv.list({ prefix, cursor, limit: 1000 });
    const vals = await Promise.all(page.keys.map((k: { name: string }) => kv.get(k.name)));
    page.keys.forEach((k: { name: string }, i: number) => { try { if (vals[i]) out.push({ key: k.name, value: JSON.parse(vals[i]) }); } catch { /* valor no JSON */ } });
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);
  return out;
}

export async function admin(req: Request, env: AuthEnv, sub: string): Promise<Response> {
  if (!env.SUSCRIPCIONES || !(env.SUSCRIPCIONES as any).list) return json({ error: "no_configurado" }, 503);
  const s = await currentSession(req, env);
  if (!s) return json({ error: "sin_sesion" }, 401);
  if (!admins(env).includes(s.email)) return json({ error: "prohibido", email: s.email }, 403);

  if (sub === "/resumen" && req.method === "GET") {
    const [subs, progs, usuarios, solicitudes, certs, accesosPrueba] = await Promise.all(
      ["sub:", "prog:", "usuario:", "solicitud:", "cert:", "prueba:"].map((p) => todas(env, p)));
    const alumnos = new Map<string, any>();
    const alumno = (email: string) => {
      if (!alumnos.has(email)) alumnos.set(email, { email, nombre: "", primerIngreso: null, ultimoIngreso: null, ultimaActividad: null, suscripciones: [], avance: {}, entregas: 0, certificados: [] });
      return alumnos.get(email);
    };
    for (const { value: u } of usuarios) Object.assign(alumno(u.email), { nombre: u.nombre || "", primerIngreso: u.primerIngreso, ultimoIngreso: u.ultimoIngreso });
    for (const { value: x } of subs) {
      if (!x.id) continue;
      alumno(String(x.cuenta || x.email).toLowerCase()).suscripciones.push({
        id: x.id, plan: x.plan, carrera: x.carrera || null, status: x.status, emailPago: x.email, creada: x.creada,
        proximoCobro: x.proximoCobro || null, alDia: x.alDia ?? null, ultimaCuota: x.ultimaCuota || null, matricula: x.matricula || null
      });
    }
    for (const { key, value: p } of progs) {
      const a = alumno(key.slice("prog:".length));
      for (const [c, ids] of Object.entries(p.progreso || {})) if (Array.isArray(ids) && ids.length) a.avance[c] = ids.length;
      a.entregas = Object.values(p.entregas || {}).filter((e: any) => e && e.e).length;
      a.ultimaActividad = p.actualizado || null;
    }
    for (const { value: c } of certs) alumno(c.email).certificados.push({ id: c.id, carrera: c.carrera, fecha: c.fecha });

    // Usuarios de prueba de Mercado Pago (de la etapa de pruebas): se muestran aparte y no suman en los totales
    const esPrueba = (a: any) => /@testuser\.com$/i.test(a.email) || a.suscripciones.some((x: any) => /@testuser\.com$/i.test(String(x.emailPago || "")));
    const pruebas = [...alumnos.values()].filter(esPrueba).map((a) => a.email);
    pruebas.forEach((e) => alumnos.delete(e));
    const lista = [...alumnos.values()].sort((a, b) => String(b.ultimaActividad || b.ultimoIngreso || "").localeCompare(String(a.ultimaActividad || a.ultimoIngreso || "")));
    const subsTodas = lista.flatMap((a) => a.suscripciones);
    const activas = subsTodas.filter((x) => x.status === "authorized");
    return json({
      generado: new Date().toISOString(),
      totales: {
        cuentas: lista.length,
        activas: activas.length,
        porPlan: { diplomatura: activas.filter((x) => x.plan === "diplomatura").length, todas: activas.filter((x) => x.plan === "todas").length },
        conProblemaDePago: activas.filter((x) => x.alDia === false).length,
        pausadas: subsTodas.filter((x) => x.status === "paused").length,
        canceladas: subsTodas.filter((x) => x.status === "canceled").length,
        ingresoMensual: activas.reduce((t, x) => t + (PRECIOS[x.plan] || 0), 0),
        matriculasPagas: subsTodas.filter((x) => x.matricula === "approved").length,
        certificados: certs.length,
        solicitudesPendientes: solicitudes.filter((x) => x.value.estado !== "atendida").length
      },
      alumnos: lista,
      cuentasDePrueba: pruebas,
      accesosDePrueba: accesosPrueba.map((x) => x.value).filter((p) => Date.parse(p.hasta) > Date.now()).sort((a, b) => String(a.hasta).localeCompare(String(b.hasta))),
      solicitudes: solicitudes.map((x) => x.value).sort((a, b) => String(b.fecha).localeCompare(String(a.fecha)))
    });
  }

  const m = sub.match(/^\/solicitudes\/((?:ARR|BAJ)-\d{8}-[0-9A-F]{8})$/);
  if (m && req.method === "POST") {
    const k = `solicitud:${m[1]}`;
    const raw = await env.SUSCRIPCIONES.get(k);
    if (!raw) return json({ error: "no_encontrada" }, 404);
    let body: any = {};
    try { body = await req.json(); } catch { /* vacío */ }
    const estado = body.estado === "recibida" ? "recibida" : "atendida";
    const sol = { ...JSON.parse(raw), estado, nota: String(body.nota || "").slice(0, 500), atendidaPor: estado === "atendida" ? s.email : null, atendidaEl: estado === "atendida" ? new Date().toISOString() : null };
    await env.SUSCRIPCIONES.put(k, JSON.stringify(sol));
    return json(sol);
  }
  if (sub === "/pruebas" && req.method === "POST") {
    let body: any = {};
    try { body = await req.json(); } catch { /* vacío */ }
    const email = String(body.email || "").trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 120) return json({ error: "email", message: "Revisá el correo." }, 400);
    const dias = Math.max(1, Math.min(90, Math.round(Number(body.dias) || 7)));
    const validas = ["interiores", "industrial", "grafico", "indumentaria"];
    const pedidas: string[] = Array.isArray(body.carreras) ? body.carreras.map(String) : ["todas"];
    const carreras = pedidas.includes("todas") ? ["todas"] : pedidas.filter((c) => validas.includes(c));
    if (!carreras.length) return json({ error: "carreras", message: "Elegí al menos una diplomatura." }, 400);
    const ahora = new Date(), hasta = new Date(ahora.getTime() + dias * 86400000);
    const p = { email, carreras, dias, desde: ahora.toISOString(), hasta: hasta.toISOString(), por: s.email };
    await env.SUSCRIPCIONES.put(`prueba:${email}`, JSON.stringify(p), { expirationTtl: dias * 86400 + 86400 } as any);
    return json(p);
  }
  const q = sub.match(/^\/pruebas\/(.+)$/);
  if (q && req.method === "DELETE") {
    const email = decodeURIComponent(q[1]).trim().toLowerCase();
    await (env.SUSCRIPCIONES as any).delete(`prueba:${email}`);
    return json({ ok: true, email });
  }
  return json({ error: "not_found" }, 404);
}
