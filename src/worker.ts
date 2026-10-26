// Entrada para Cloudflare Workers: el asistente en /api/asistente y el resto del sitio como archivos estáticos (carpeta public).
import { onRequestPost } from "../functions/api/asistente";

interface Env { ASSETS: { fetch: (req: Request) => Promise<Response> }; [k: string]: any }

export default {
  async fetch(request: Request, env: Env, ctx: any): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === "/api/asistente") {
      if (request.method !== "POST") return Response.json({ error: "method_not_allowed" }, { status: 405 });
      return (onRequestPost as any)({ request, env, waitUntil: ctx?.waitUntil?.bind(ctx) });
    }
    return env.ASSETS.fetch(request);
  }
};
