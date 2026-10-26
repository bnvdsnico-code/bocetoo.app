// Asistente de IA de boceto. Recibe la conversación (y una imagen opcional del Bocetador)
// y responde con Claude a través del AI Gateway de Netlify, que inyecta ANTHROPIC_API_KEY y ANTHROPIC_BASE_URL.
import type { Config } from "@netlify/functions";

const SYSTEM = `Sos el asistente de aprendizaje de boceto, una escuela online de diseño sin profesores con cuatro carreras: Diseño de Interiores y Mobiliario, Diseño Industrial, Diseño Gráfico y Diseño de Indumentaria.
Respondés en español rioplatense, con voseo, en tono cálido, claro y concreto, como un buen docente de taller.
Ayudás con dudas de las diplomaturas, ejercicios, correcciones de bocetos y planificación del estudio. Si te piden algo que no tiene que ver con diseño o con la escuela, lo decís con amabilidad y volvés al tema.
Si no estás seguro de un dato técnico, lo aclarás. Nunca inventes precios, fechas ni políticas de la escuela.`;

// Modelos a probar en orden; ASISTENTE_MODEL permite elegir otro sin tocar el código.
const MODELS = ["claude-sonnet-4-5-20250929", "claude-sonnet-4-5", "claude-haiku-4-5"];
const MAX_CHARS = 24000;
const MAX_IMAGE_B64 = 5_000_000; // ~3,7 MB de imagen
const IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"];

type Turn = { role: "user" | "assistant"; content: string };

const fail = (error: string, status: number) => Response.json({ error }, { status });

export default async (req: Request) => {
  if (req.method !== "POST") return fail("method_not_allowed", 405);

  let body: any;
  try { body = await req.json(); } catch { return fail("bad_request", 400); }

  const turns: Turn[] = Array.isArray(body?.messages) ? body.messages : [];
  if (!turns.length || turns.length > 24) return fail("bad_request", 400);
  let chars = 0;
  for (const t of turns) {
    if ((t?.role !== "user" && t?.role !== "assistant") || typeof t?.content !== "string" || !t.content.trim()) return fail("bad_request", 400);
    chars += t.content.length;
  }
  if (turns[0].role !== "user" || turns[turns.length - 1].role !== "user") return fail("bad_request", 400);
  if (chars > MAX_CHARS) return fail("too_large", 413);

  const image = body?.image;
  if (image && (typeof image.data !== "string" || !IMAGE_TYPES.includes(image.mediaType) || image.data.length > MAX_IMAGE_B64)) {
    return fail("too_large", 413);
  }

  const apiKey = Netlify.env.get("ANTHROPIC_API_KEY");
  const baseUrl = (Netlify.env.get("ANTHROPIC_BASE_URL") || "https://api.anthropic.com").replace(/\/+$/, "");
  if (!apiKey) return fail("ai_unavailable", 503);

  const messages = turns.map((t, i) => {
    if (i === turns.length - 1 && image) {
      return {
        role: "user",
        content: [
          { type: "image", source: { type: "base64", media_type: image.mediaType, data: image.data } },
          { type: "text", text: t.content }
        ]
      };
    }
    return { role: t.role, content: t.content };
  });
  const maxTokens = Math.max(100, Math.min(1200, Number(body?.maxTokens) || 800));
  const preferred = Netlify.env.get("ASISTENTE_MODEL");
  const models = preferred ? [preferred, ...MODELS] : MODELS;

  for (const model of models) {
    let res: Response;
    try {
      res = await fetch(`${baseUrl}/v1/messages`, {
        method: "POST",
        headers: { "content-type": "application/json", "x-api-key": apiKey, "anthropic-version": "2023-06-01" },
        body: JSON.stringify({ model, max_tokens: maxTokens, system: SYSTEM, messages })
      });
    } catch (e) {
      console.error("asistente: sin conexión con el modelo", e);
      return fail("upstream_error", 502);
    }
    if (res.ok) {
      const data: any = await res.json();
      const text = (data.content || []).filter((b: any) => b.type === "text").map((b: any) => b.text).join("").trim();
      if (!text) return fail("empty_completion", 502);
      return Response.json({ text, truncated: data.stop_reason === "max_tokens", model });
    }
    const detail = await res.text().catch(() => "");
    console.error(`asistente: ${model} respondió ${res.status}`, detail.slice(0, 400));
    if (res.status === 429) return fail("rate_limited", 429);
    if (res.status === 401 || res.status === 403) return fail("ai_unavailable", 503);
    // 404 o 400 por modelo no disponible: probar el siguiente
    if (res.status === 404 || (res.status === 400 && /model/i.test(detail))) continue;
    return fail("upstream_error", 502);
  }
  return fail("ai_unavailable", 503);
};

export const config: Config = {
  path: "/api/asistente",
  method: "POST",
  rateLimit: { windowLimit: 20, windowSize: 60, aggregateBy: ["ip", "domain"] }
};
