// Suscripciones de boceto con Mercado Pago (Argentina), modelo "con plan".
// El navegador solo manda qué oferta elige (plan + carrera), el email y el token de tarjeta de un solo uso.
// Montos, frecuencia e ID del plan salen siempre del catálogo del servidor.

type KV = {
  get: (k: string) => Promise<string | null>;
  put: (k: string, v: string, o?: { expirationTtl?: number }) => Promise<void>;
  delete: (k: string) => Promise<void>;
};

export interface MpEnv {
  MP_ACCESS_TOKEN?: string;
  MP_PUBLIC_KEY?: string;
  APP_URL?: string;
  ADMIN_KEY?: string;
  MP_SUBSCRIPTION_PLAN_ID?: string;       // plan "Tu diplomatura" (si se carga a mano)
  MP_SUBSCRIPTION_PLAN_ID_TODAS?: string; // plan "Todas las diplomaturas" (si se carga a mano)
  SUSCRIPCIONES?: KV;
}

const MP_API = "https://api.mercadopago.com";
const CARRERAS: Record<string, string> = {
  interiores: "Interiores y Mobiliario", industrial: "Industrial", grafico: "Gráfico", indumentaria: "Indumentaria"
};

// Catálogo confiable de ofertas: la única fuente de precios y planes.
const SUBSCRIPTION_OFFERS = {
  diplomatura: {
    reason: "boceto · Tu diplomatura", amount: 63000, repetitions: 4 as number | null,
    planEnv: "MP_SUBSCRIPTION_PLAN_ID" as const, kvKey: "plan:diplomatura", needsCarrera: true
  },
  todas: {
    reason: "boceto · Todas las diplomaturas", amount: 83000, repetitions: null as number | null,
    planEnv: "MP_SUBSCRIPTION_PLAN_ID_TODAS" as const, kvKey: "plan:todas", needsCarrera: false
  }
};
type OfferKey = keyof typeof SUBSCRIPTION_OFFERS;

const json = (data: unknown, status = 200, extra: Record<string, string> = {}) =>
  new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...extra } });
const fail = (error: string, message: string, status: number) => json({ error, message }, status);

const appUrl = (env: MpEnv, req: Request) => (env.APP_URL || new URL(req.url).origin).replace(/\/+$/, "");
const randomId = () => [...crypto.getRandomValues(new Uint8Array(16))].map((b) => b.toString(16).padStart(2, "0")).join("");
const mpHeaders = (env: MpEnv) => ({ Authorization: `Bearer ${env.MP_ACCESS_TOKEN}`, "Content-Type": "application/json" });

async function resolveOffer(env: MpEnv, plan: unknown, carrera: unknown) {
  if (typeof plan !== "string" || !(plan in SUBSCRIPTION_OFFERS)) return null;
  const offer = SUBSCRIPTION_OFFERS[plan as OfferKey];
  if (offer.needsCarrera && (typeof carrera !== "string" || !CARRERAS[carrera])) return null;
  const planId = env[offer.planEnv] || (env.SUSCRIPCIONES ? await env.SUSCRIPCIONES.get(offer.kvKey) : null);
  const trustedOffer = { key: plan as OfferKey, ...offer, carrera: offer.needsCarrera ? (carrera as string) : null, planId };
  return trustedOffer;
}

// Estados de la suscripción que muestra el sitio. Cualquier otro valor se trata como "pending".
const KNOWN = new Set(["pending", "authorized", "paused", "canceled"]);
const normalizeStatus = (s: unknown) => (typeof s === "string" && KNOWN.has(s) ? s : "pending");

async function readRecord(env: MpEnv, id: string, llave: string | null) {
  if (!env.SUSCRIPCIONES || !/^[A-Za-z0-9_-]{6,64}$/.test(id) || !llave) return null;
  const raw = await env.SUSCRIPCIONES.get(`sub:${id}`);
  if (!raw) return null;
  const rec = JSON.parse(raw);
  return rec.llave === llave ? rec : null;
}

/* GET /api/mp-config: Public Key para MercadoPago.js, siempre sin caché */
export function mpConfig(env: MpEnv) {
  if (!env.MP_PUBLIC_KEY) return fail("mp_not_configured", "Los pagos todavía no están configurados. Probá más tarde.", 503);
  return json({ publicKey: env.MP_PUBLIC_KEY }, 200, { "cache-control": "no-store, max-age=0" });
}

/* GET /api/ofertas: precios para mostrar (solo lectura, salen del catálogo) */
export function ofertas() {
  const out: Record<string, unknown> = {};
  for (const [k, o] of Object.entries(SUBSCRIPTION_OFFERS)) out[k] = { reason: o.reason, amount: o.amount, repetitions: o.repetitions, needsCarrera: o.needsCarrera };
  return json({ ofertas: out, carreras: CARRERAS });
}

/* POST /api/subscriptions: crea la suscripción autorizada con el plan del servidor */
export async function createSubscription(req: Request, env: MpEnv) {
  if (!env.MP_ACCESS_TOKEN || !env.SUSCRIPCIONES) return fail("mp_not_configured", "Los pagos todavía no están configurados. Probá más tarde.", 503);
  let input: any;
  try { input = await req.json(); } catch { return fail("bad_request", "No pudimos leer el formulario. Recargá la página e intentá nuevamente.", 400); }

  const trustedOffer = await resolveOffer(env, input?.plan, input?.carrera);
  if (!trustedOffer) return fail("bad_offer", "Elegí una diplomatura válida antes de suscribirte.", 400);
  if (!trustedOffer.planId) return fail("plan_missing", "El plan todavía no está creado. Avisanos y lo resolvemos.", 503);

  const email = typeof input?.email === "string" ? input.email.trim().toLowerCase() : "";
  const cardToken = typeof input?.cardToken === "string" ? input.cardToken : "";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 120) return fail("bad_email", "Revisá el email: lo usamos para tu cuenta y tus avisos de pago.", 400);
  if (!/^[A-Za-z0-9]{16,64}$/.test(cardToken)) return fail("bad_card", "No pudimos validar la tarjeta. Revisá los datos e intentá nuevamente.", 400);

  // Evita dobles envíos del mismo alumno a la misma oferta durante un minuto.
  const lockKey = `lock:${email}:${trustedOffer.key}:${trustedOffer.carrera || "-"}`;
  if (await env.SUSCRIPCIONES.get(lockKey)) return fail("in_progress", "Ya estamos procesando tu suscripción. Esperá unos segundos.", 409);
  await env.SUSCRIPCIONES.put(lockKey, "1", { expirationTtl: 60 });

  const externalReference = `boceto-${trustedOffer.key}-${trustedOffer.carrera || "todas"}-${randomId()}`;
  const subscriptionBackUrl = `${appUrl(env, req)}/inscripcion.html?estado=volver`;
  const body = {
    preapproval_plan_id: trustedOffer.planId,
    payer_email: email,
    card_token_id: cardToken,
    external_reference: externalReference,
    back_url: subscriptionBackUrl,
    status: "authorized"
  };

  let res: Response;
  try {
    res = await fetch("https://api.mercadopago.com/preapproval", { method: "POST", headers: mpHeaders(env), body: JSON.stringify(body) });
  } catch {
    await env.SUSCRIPCIONES.delete(lockKey);
    return fail("mp_unreachable", "No pudimos conectar con Mercado Pago. Intentá nuevamente en unos minutos.", 502);
  }
  const data: any = await res.json().catch(() => ({}));
  if (!res.ok || !data?.id) {
    await env.SUSCRIPCIONES.delete(lockKey); // se puede reintentar enseguida con otra tarjeta
    console.error("suscripciones: alta rechazada", res.status, data?.status ?? "", String(data?.message ?? "").slice(0, 160));
    const msg = res.status === 400 || res.status === 422
      ? "Mercado Pago rechazó la tarjeta. Probá con otra tarjeta o revisá los datos."
      : "No se pudo crear la suscripción. Intentá nuevamente en unos minutos.";
    return fail("mp_rejected", msg, res.status >= 500 ? 502 : 402);
  }

  const llave = randomId();
  const record = {
    id: String(data.id), llave, externalReference, plan: trustedOffer.key, carrera: trustedOffer.carrera, email,
    status: normalizeStatus(data.status), creada: new Date().toISOString()
  };
  await env.SUSCRIPCIONES.put(`sub:${record.id}`, JSON.stringify(record));
  await env.SUSCRIPCIONES.put(`ref:${externalReference}`, record.id);
  return json({ id: record.id, llave, status: record.status, plan: record.plan, carrera: record.carrera, reason: trustedOffer.reason, amount: trustedOffer.amount });
}

/* GET /api/subscriptions/:id: estado actualizado desde Mercado Pago (requiere la llave del alumno) */
export async function getSubscription(req: Request, env: MpEnv, id: string) {
  if (!env.MP_ACCESS_TOKEN || !env.SUSCRIPCIONES) return fail("mp_not_configured", "Los pagos todavía no están configurados.", 503);
  const rec = await readRecord(env, id, req.headers.get("x-llave"));
  if (!rec) return fail("not_found", "No encontramos esa suscripción en este navegador.", 404);
  const res = await fetch(`https://api.mercadopago.com/preapproval/${encodeURIComponent(id)}`, { headers: mpHeaders(env) }).catch(() => null);
  const data: any = res && res.ok ? await res.json().catch(() => null) : null;
  if (data) {
    rec.status = normalizeStatus(data.status);
    rec.proximoCobro = data.next_payment_date || null;
    await env.SUSCRIPCIONES.put(`sub:${id}`, JSON.stringify(rec));
  }
  return json({ id: rec.id, status: rec.status, plan: rec.plan, carrera: rec.carrera, proximoCobro: rec.proximoCobro || null, actualizado: !!data });
}

/* POST /api/subscriptions/:id/:accion: solo pause, reactivate o cancel */
const LIFECYCLE: Record<string, "paused" | "authorized" | "canceled"> = { pause: "paused", reactivate: "authorized", cancel: "canceled" };
export async function changeSubscription(req: Request, env: MpEnv, id: string, accion: string) {
  const status = LIFECYCLE[accion];
  if (!status) return fail("bad_action", "Acción no permitida.", 400);
  if (!env.MP_ACCESS_TOKEN || !env.SUSCRIPCIONES) return fail("mp_not_configured", "Los pagos todavía no están configurados.", 503);
  const rec = await readRecord(env, id, req.headers.get("x-llave"));
  if (!rec) return fail("not_found", "No encontramos esa suscripción en este navegador.", 404);
  if (rec.status === "canceled") return fail("already_canceled", "Esta suscripción ya está cancelada.", 409);
  const res = await fetch(`https://api.mercadopago.com/preapproval/${encodeURIComponent(id)}`, {
    method: "PUT", headers: mpHeaders(env), body: JSON.stringify({ status })
  }).catch(() => null);
  const data: any = res ? await res.json().catch(() => ({})) : {};
  if (!res || !res.ok) {
    console.error("suscripciones: cambio rechazado", res?.status ?? 0, accion);
    return fail("mp_rejected", "Mercado Pago no aceptó el cambio. Intentá nuevamente en unos minutos.", 502);
  }
  rec.status = normalizeStatus(data.status || status);
  await env.SUSCRIPCIONES.put(`sub:${id}`, JSON.stringify(rec));
  return json({ id, status: rec.status });
}

/* POST /api/admin/planes: crea los planes una sola vez. Solo con la clave de administración. */
export async function provisionPlans(req: Request, env: MpEnv) {
  const key = req.headers.get("x-admin-key") || "";
  if (!env.ADMIN_KEY || env.ADMIN_KEY.length < 12 || key !== env.ADMIN_KEY) return fail("forbidden", "Clave de administración incorrecta.", 403);
  if (!env.MP_ACCESS_TOKEN || !env.SUSCRIPCIONES) return fail("mp_not_configured", "Faltan MP_ACCESS_TOKEN o el almacenamiento.", 503);
  const backUrl = `${appUrl(env, req)}/inscripcion.html?estado=volver`;
  const result: Record<string, unknown> = {};
  for (const [k, offer] of Object.entries(SUBSCRIPTION_OFFERS)) {
    const existing = env[offer.planEnv] || await env.SUSCRIPCIONES.get(offer.kvKey);
    if (existing) {
      const check = await fetch(`${MP_API}/preapproval_plan/${encodeURIComponent(existing)}`, { headers: mpHeaders(env) }).catch(() => null);
      if (check && check.ok) { result[k] = { id: existing, creado: false }; continue; }
    }
    const auto_recurring: Record<string, unknown> = { frequency: 1, frequency_type: "months", transaction_amount: offer.amount, currency_id: "ARS" };
    if (offer.repetitions) auto_recurring.repetitions = offer.repetitions;
    const res = await fetch(`${MP_API}/preapproval_plan`, {
      method: "POST", headers: mpHeaders(env), body: JSON.stringify({ reason: offer.reason, auto_recurring, back_url: backUrl })
    }).catch(() => null);
    const data: any = res ? await res.json().catch(() => ({})) : {};
    if (!res || !res.ok || !data?.id) { result[k] = { error: res?.status ?? 0, message: String(data?.message ?? "sin respuesta").slice(0, 200) }; continue; }
    await env.SUSCRIPCIONES.put(offer.kvKey, String(data.id));
    result[k] = { id: data.id, creado: true };
  }
  return json({ planes: result });
}
