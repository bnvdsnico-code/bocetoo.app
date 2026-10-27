// Entrada para Cloudflare Workers: el asistente, las suscripciones de Mercado Pago y el resto del sitio como archivos estáticos (carpeta public).
import { onRequestPost } from "../functions/api/asistente";
import { mpWebhook } from "./webhook";
import { createRequest } from "./solicitudes";
import { authStart, authCallback, authLogout, me, guardClass } from "./auth";
import { progreso } from "./progreso";
import { createEnrollmentFee, confirmEnrollmentFee } from "./matricula";
import { mpConfig, ofertas, createSubscription, getSubscription, changeSubscription, ensurePlans, paymentsStatus, type MpEnv } from "./suscripciones";

interface Env extends MpEnv { ASSETS: { fetch: (req: Request) => Promise<Response> }; [k: string]: any }

const notAllowed = () => Response.json({ error: "method_not_allowed" }, { status: 405 });

export default {
  async fetch(request: Request, env: Env, ctx: any): Promise<Response> {
    const url = new URL(request.url);
    const { pathname } = url;
    const method = request.method;

    // www.bocetoo.app y la dirección vieja (workers.dev) → bocetoo.app.
    // /api/* queda en las dos (el webhook de Mercado Pago apunta a workers.dev) y también /auth/callback,
    // para que termine bien un ingreso que empezó en la dirección vieja.
    const vieja = url.hostname.endsWith(".workers.dev") && method === "GET" && !pathname.startsWith("/api/") && pathname !== "/auth/callback";
    if (url.hostname === "www.bocetoo.app" || vieja) {
      url.hostname = "bocetoo.app";
      return Response.redirect(url.toString(), 301);
    }

    if (pathname === "/api/asistente") {
      if (method !== "POST") return notAllowed();
      return (onRequestPost as any)({ request, env, waitUntil: ctx?.waitUntil?.bind(ctx) });
    }
    if (pathname === "/auth/google") return authStart(request, env);
    if (pathname === "/auth/callback") return authCallback(request, env);
    if (pathname === "/auth/salir") return authLogout(request, env);
    if (pathname === "/api/yo") return method === "GET" ? me(request, env) : notAllowed();
    if (pathname === "/api/progreso" || pathname.startsWith("/api/progreso/")) return progreso(request, env, pathname.slice("/api/progreso".length));
    if (pathname === "/api/mp-config") return method === "GET" ? mpConfig(env) : notAllowed();
    if (pathname === "/api/ofertas") return method === "GET" ? ofertas() : notAllowed();
    if (pathname === "/api/estado-pagos") return method === "GET" ? paymentsStatus(env) : notAllowed();
    if (pathname === "/api/mp/webhook") return method === "POST" ? mpWebhook(request, env, ctx) : notAllowed();
    if (pathname === "/api/solicitudes") return method === "POST" ? createRequest(request, env) : notAllowed();
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

    // Clases: solo con suscripción activa (la primera de cada diplomatura es libre)
    const protegida = await guardClass(request, env, () => env.ASSETS.fetch(request));
    if (protegida) return protegida;

    return env.ASSETS.fetch(request);
  },

  // Tarea programada (cada 15 minutos): crea los planes de Mercado Pago si todavía no existen.
  async scheduled(_event: unknown, env: Env, ctx: any): Promise<void> {
    ctx.waitUntil(ensurePlans(env).then((r) => console.log("planes", JSON.stringify(r))));
  }
};
