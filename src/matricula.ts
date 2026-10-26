// Matrícula única de boceto ($45.000) con Checkout Pro de Mercado Pago.
// El alumno ya suscripto toca "Pagar matrícula con Mercado Pago": el servidor crea una preferencia y lo redirige a init_point.
// El pago se confirma del lado del servidor (consulta /v1/payments) y también por webhook.

import type { MpEnv } from "./suscripciones";

const MATRICULA = { titulo: "Matrícula única · boceto", monto: 45000, moneda: "ARS" };

const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const fail = (error: string, message: string, status: number) => json({ error, message }, status);
const headers = (env: MpEnv) => ({ Authorization: `Bearer ${env.MP_ACCESS_TOKEN}`, "Content-Type": "application/json" });

async function record(env: MpEnv, id: unknown, llave: unknown) {
  if (!env.SUSCRIPCIONES || typeof id !== "string" || !/^[A-Za-z0-9_-]{6,64}$/.test(id) || typeof llave !== "string") return null;
  const raw = await env.SUSCRIPCIONES.get(`sub:${id}`);
  const rec = raw ? JSON.parse(raw) : null;
  return rec && rec.llave === llave ? rec : null;
}

/* POST /api/matricula: crea la preferencia de Checkout Pro y devuelve init_point */
export async function createEnrollmentFee(req: Request, env: MpEnv) {
  if (!env.MP_ACCESS_TOKEN || !env.SUSCRIPCIONES) return fail("mp_not_configured", "Los pagos todavía no están configurados.", 503);
  let input: any;
  try { input = await req.json(); } catch { return fail("bad_request", "No pudimos leer el pedido. Recargá la página.", 400); }
  const rec = await record(env, input?.id, input?.llave);
  if (!rec) return fail("not_found", "Primero suscribite a una diplomatura desde esta página.", 404);
  if (rec.matricula === "approved") return fail("already_paid", "La matrícula ya está paga.", 409);

  const appUrl = (env.APP_URL || new URL(req.url).origin).replace(/\/+$/, "");
  // auto_return solo con una dirección pública HTTPS (Mercado Pago lo rechaza con localhost).
  const publicAppUrl = /^https:\/\//i.test(appUrl) && !/^https:\/\/(?:localhost|127\.0\.0\.1|0\.0\.0\.0)(?::|\/|$)/i.test(appUrl);
  const back = `${appUrl}/inscripcion.html?matricula=`;
  const body = {
    items: [{ id: "matricula", title: MATRICULA.titulo, quantity: 1, unit_price: MATRICULA.monto, currency_id: MATRICULA.moneda }],
    payer: rec.email ? { email: rec.email } : undefined,
    back_urls: { success: `${back}ok`, failure: `${back}error`, pending: `${back}pendiente` },
    ...(publicAppUrl ? { auto_return: "approved" } : {}),
    notification_url: publicAppUrl ? `${appUrl}/api/mp/webhook?source_news=webhooks` : undefined,
    external_reference: `matricula:${rec.id}`,
    statement_descriptor: "BOCETO"
  };
  let res: Response;
  try {
    res = await fetch("https://api.mercadopago.com/checkout/preferences", {
      method: "POST",
      headers: { ...headers(env), "X-Idempotency-Key": `matricula-${rec.id}-${Date.now()}` },
      body: JSON.stringify(body)
    });
  } catch {
    return fail("mp_unreachable", "No pudimos conectar con Mercado Pago. Intentá nuevamente.", 502);
  }
  const data: any = await res.json().catch(() => ({}));
  if (!res.ok || !data?.init_point) {
    console.error("matricula: preferencia rechazada", res.status, String(data?.message ?? "").slice(0, 160));
    return fail("mp_rejected", "No se pudo iniciar el pago de la matrícula. Intentá nuevamente en unos minutos.", 502);
  }
  // Siempre init_point: Mercado Pago no tiene un entorno aparte para pruebas.
  return json({ init_point: data.init_point });
}

/* Registra el estado de la matrícula a partir de un pago verificado en Mercado Pago. */
export async function applyEnrollmentPayment(env: MpEnv, pago: any) {
  const ref = String(pago?.external_reference || "");
  if (!ref.startsWith("matricula:") || !env.SUSCRIPCIONES) return false;
  const id = ref.slice("matricula:".length);
  const raw = await env.SUSCRIPCIONES.get(`sub:${id}`);
  if (!raw) return false;
  const rec = JSON.parse(raw);
  if (rec.matricula === "approved") return true; // un pago aprobado no se pisa con otro estado
  rec.matricula = pago.status || "pending";
  rec.matriculaPago = String(pago.id);
  await env.SUSCRIPCIONES.put(`sub:${id}`, JSON.stringify(rec));
  return true;
}

/* POST /api/matricula/confirmar: al volver de Mercado Pago, verifica el pago del lado del servidor */
export async function confirmEnrollmentFee(req: Request, env: MpEnv) {
  if (!env.MP_ACCESS_TOKEN) return fail("mp_not_configured", "Los pagos todavía no están configurados.", 503);
  let input: any;
  try { input = await req.json(); } catch { return fail("bad_request", "Pedido inválido.", 400); }
  const rec = await record(env, input?.id, input?.llave);
  if (!rec) return fail("not_found", "No encontramos tu suscripción en este navegador.", 404);
  const paymentId = String(input?.paymentId || "");
  if (!/^\d{4,20}$/.test(paymentId)) return json({ matricula: rec.matricula || null });
  const res = await fetch(`https://api.mercadopago.com/v1/payments/${paymentId}`, { headers: headers(env) }).catch(() => null);
  const pago: any = res && res.ok ? await res.json().catch(() => null) : null;
  if (!pago || pago.external_reference !== `matricula:${rec.id}`) return fail("mismatch", "No pudimos confirmar ese pago.", 400);
  await applyEnrollmentPayment(env, pago);
  const raw = await env.SUSCRIPCIONES!.get(`sub:${rec.id}`);
  return json({ matricula: raw ? JSON.parse(raw).matricula : pago.status });
}
