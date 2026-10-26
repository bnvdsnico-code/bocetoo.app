// Botón de arrepentimiento y Botón de baja de servicio (Defensa del Consumidor, Argentina).
// Sin registro ni pasos extra: el consumidor completa un formulario y recibe en pantalla, al instante,
// un código de identificación de su solicitud. Las solicitudes quedan guardadas en KV con la clave "solicitud:<código>".

import type { MpEnv } from "./suscripciones";

const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });

const TIPOS: Record<string, string> = { arrepentimiento: "ARR", baja: "BAJ" };
const limpio = (v: unknown, max: number) => (typeof v === "string" ? v.replace(/[\u0000-\u001f]/g, " ").trim().slice(0, max) : "");

/* POST /api/solicitudes  { tipo, nombre, email, dni?, detalle? } */
export async function createRequest(req: Request, env: MpEnv) {
  if (!env.SUSCRIPCIONES) return json({ error: "unavailable", message: "No pudimos registrar la solicitud. Escribinos por email." }, 503);
  let input: any;
  try { input = await req.json(); } catch { return json({ error: "bad_request", message: "No pudimos leer el formulario." }, 400); }
  const tipo = limpio(input?.tipo, 20);
  if (!TIPOS[tipo]) return json({ error: "bad_type", message: "Tipo de solicitud inválido." }, 400);
  const nombre = limpio(input?.nombre, 120), email = limpio(input?.email, 120).toLowerCase();
  const dni = limpio(input?.dni, 20), detalle = limpio(input?.detalle, 1000);
  if (!nombre || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
    return json({ error: "bad_input", message: "Completá tu nombre y un email válido para poder responderte." }, 400);
  }
  const fecha = new Date();
  const sufijo = [...crypto.getRandomValues(new Uint8Array(4))].map((b) => b.toString(16).padStart(2, "0")).join("").toUpperCase();
  const codigo = `${TIPOS[tipo]}-${fecha.toISOString().slice(0, 10).replace(/-/g, "")}-${sufijo}`;
  await env.SUSCRIPCIONES.put(`solicitud:${codigo}`, JSON.stringify({
    codigo, tipo, nombre, email, dni, detalle, fecha: fecha.toISOString(), estado: "recibida"
  }));
  console.log("solicitud recibida", tipo, codigo);
  return json({ codigo, fecha: fecha.toISOString() });
}
