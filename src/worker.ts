// Entrada para Cloudflare Workers: el asistente, las suscripciones de Mercado Pago y el resto del sitio como archivos estáticos (carpeta public).
import { onRequestPost } from "../functions/api/asistente";
import { mpWebhook } from "./webhook";
import { createEnrollmentFee, confirmEnrollmentFee } from "./matricula";
import { mpConfig, ofertas, createSubscription, getSubscription, changeSubscription, ensurePlans, paymentsStatus, type MpEnv } from "./suscripciones";

interface Env extends MpEnv { ASSETS: { fetch: (req: Request) => Promise<Response> }; [k: string]: any }

const notAllowed = () => Response.json({ error: "method_not_allowed" }, { status: 405 });

export default {
  async fetch(request: Request, env: Env, ctx: any): Promise<Response> {
    const { pathname } = new URL(request.url);
    const method = request.method;

    if (pathname === "/api/asistente") {
      if (method !== "POST") return notAllowed();
      return (onRequestPost as any)({ request, env, waitUntil: ctx?.waitUntil?.bind(ctx) });
    }
    if (pathname === "/api/mp-config") return method === "GET" ? mpConfig(env) : notAllowed();
    if (pathname === "/api/ofertas") return method === "GET" ? ofertas() : notAllowed();
    if (pathname === "/api/estado-pagos") return method === "GET" ? paymentsStatus(env) : notAllowed();
    if (pathname === "/api/mp/webhook") return method === "POST" ? mpWebhook(request, env, ctx) : notAllowed();
    if (pathname === "/api/matricula") return method === "POST" ? createEnrollmentFee(request, env) : notAllowed();
    if (pathname === "/api/matricula/confirmar") return method === "POST" ? confirmEnrollmentFee(request, env) : notAllowed();
    if (pathname === "/api/subscriptions") return method === "POST" ? createSubscription(request, env) : notAllowed();

    // GET /api/subscriptions/:id  → estado
    // POST /api/subscriptions/:id/:accion (pause | reactivate | cancel)
    const m = pathname.match(/^\/api\/subscriptions\/([A-Za-z0-9_-]+)(?:\/(pause|reactivate|cancel))?$/);
    if (m) {
      if (!m[2]) return method === "GET" ? getSubscription(request, env, m[1]) : notAllowed();
      return method === "POST" ? changeSubscription(request, env, m[1], m[2]) : notAllowed();
    }
    if (pathname.startsWith("/api/")) return Response.json({ error: "not_found" }, { status: 404 });

    return env.ASSETS.fetch(request);
  },

  // Tarea programada (cada 15 minutos): crea los planes de Mercado Pago si todavía no existen.
  async scheduled(_event: unknown, env: Env, ctx: any): Promise<void> {
    ctx.waitUntil(ensurePlans(env).then((r) => console.log("planes", JSON.stringify(r))));
  }
};
