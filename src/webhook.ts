// Receptor de notificaciones (webhooks) de Mercado Pago: POST /api/mp/webhook
// 1) Valida la firma x-signature (HMAC-SHA256) con MP_WEBHOOK_SECRET.
// 2) Responde 200 enseguida y procesa después (ctx.waitUntil).
// 3) Es idempotente: vuelve a consultar el estado actual en Mercado Pago, así repetir un aviso no cambia nada.

import type { MpEnv } from "./suscripciones";

interface WebhookEnv extends MpEnv { MP_WEBHOOK_SECRET?: string }

const MP_API = "https://api.mercadopago.com";
const KNOWN = new Set(["pending", "authorized", "paused", "canceled"]);

const hex = (buf: ArrayBuffer) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
function safeEqual(a: string, b: string) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

async function validSignature(req: Request, secret: string, dataId: string) {
  const signature = req.headers.get("x-signature") || "";
  const requestId = req.headers.get("x-request-id") || "";
  const parts = Object.fromEntries(signature.split(",").map((p) => p.split("=").map((s) => s.trim())));
  const ts = parts.ts, v1 = parts.v1;
  if (!ts || !v1 || !requestId || !dataId) return false;
  const canonical = `id:${dataId};request-id:${requestId};ts:${ts};`;
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const expected = hex(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(canonical)));
  return safeEqual(expected, v1.toLowerCase());
}

const mpGet = (env: WebhookEnv, path: string) =>
  fetch(`${MP_API}${path}`, { headers: { Authorization: `Bearer ${env.MP_ACCESS_TOKEN}` } })
    .then((r) => (r.ok ? r.json() : null)).catch(() => null) as Promise<any>;

// Actualiza el registro de la suscripción guardado en KV (lo crea si llegó un aviso de una suscripción desconocida).
async function updateSubscription(env: WebhookEnv, id: string, patch: Record<string, unknown>) {
  const kv = env.SUSCRIPCIONES!;
  const raw = await kv.get(`sub:${id}`);
  const rec = raw ? JSON.parse(raw) : { id, creada: new Date().toISOString(), origen: "webhook" };
  Object.assign(rec, patch, { actualizado: new Date().toISOString() });
  await kv.put(`sub:${id}`, JSON.stringify(rec));
  if (rec.externalReference) await kv.put(`ref:${rec.externalReference}`, id);
}

async function processEvent(env: WebhookEnv, type: string, dataId: string) {
  if (type === "subscription_preapproval") {
    const pre = await mpGet(env, `/preapproval/${encodeURIComponent(dataId)}`);
    if (!pre) return;
    await updateSubscription(env, String(pre.id), {
      status: KNOWN.has(pre.status) ? pre.status : "pending",
      proximoCobro: pre.next_payment_date || null,
      externalReference: pre.external_reference || undefined
    });
  } else if (type === "subscription_authorized_payment") {
    const cuota = await mpGet(env, `/authorized_payments/${encodeURIComponent(dataId)}`);
    if (!cuota?.preapproval_id) return;
    // Estado del cobro de la cuota: si falla, la suscripción queda marcada para revisar el acceso.
    const pagoOk = cuota.payment?.status === "approved" || cuota.status === "processed";
    await updateSubscription(env, String(cuota.preapproval_id), {
      ultimaCuota: { id: String(cuota.id), estado: cuota.payment?.status || cuota.status || "desconocido", monto: cuota.transaction_amount ?? null, fecha: cuota.date_created || null },
      alDia: pagoOk
    });
  } else if (type === "payment") {
    const pago = await mpGet(env, `/v1/payments/${encodeURIComponent(dataId)}`);
    if (!pago) return;
    await env.SUSCRIPCIONES!.put(`pago:${pago.id}`, JSON.stringify({ estado: pago.status, detalle: pago.status_detail, monto: pago.transaction_amount, ref: pago.external_reference || null, fecha: pago.date_last_updated || null }), { expirationTtl: 60 * 60 * 24 * 400 });
  }
}

export async function mpWebhook(req: Request, env: WebhookEnv, ctx: { waitUntil: (p: Promise<unknown>) => void }) {
  if (!env.MP_WEBHOOK_SECRET || !env.MP_ACCESS_TOKEN || !env.SUSCRIPCIONES) return new Response("not configured", { status: 503 });
  const url = new URL(req.url);
  let body: any = {};
  try { body = await req.json(); } catch { /* algunos avisos llegan sin cuerpo */ }
  // Mercado Pago firma con el data.id de la URL (en minúsculas si es alfanumérico).
  const rawId = url.searchParams.get("data.id") || String(body?.data?.id ?? "");
  const dataId = /^[a-z0-9]+$/i.test(rawId) ? rawId.toLowerCase() : rawId;
  const type = String(url.searchParams.get("type") || body?.type || body?.topic || "");
  if (!(await validSignature(req, env.MP_WEBHOOK_SECRET, dataId))) return new Response("invalid signature", { status: 401 });

  ctx.waitUntil(processEvent(env, type, rawId).catch((e) => console.error("webhook: error al procesar", type, String(e).slice(0, 160))));
  return new Response("ok", { status: 200 });
}
