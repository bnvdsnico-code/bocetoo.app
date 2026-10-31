// Asistente de IA de boceto en Cloudflare Pages: POST /api/asistente
// Recibe la conversación (y una imagen opcional del Bocetador) y responde en texto.
// Con la variable ANTHROPIC_API_KEY usa Claude; si no está, usa Workers AI (gratis, sin tarjeta).

import conocimiento from "../../src/conocimiento.json";

interface Env {
  AI?: { run: (model: string, input: unknown) => Promise<any> };
  ANTHROPIC_API_KEY?: string;
  ASISTENTE_MODEL?: string;    // modelo de Claude preferido
  WORKERS_AI_MODEL?: string;   // modelo de Workers AI preferido
}

const BASE = `Sos el asistente de aprendizaje de boceto, una escuela online de diseño sin profesores con cuatro carreras: Diseño de Interiores y Mobiliario, Diseño Industrial, Diseño Gráfico y Diseño de Indumentaria.
Respondés en español rioplatense, con voseo, en tono cálido, claro y concreto, como un buen docente de taller.
Ayudás con dudas de las diplomaturas, ejercicios, correcciones de bocetos y planificación del estudio. Si te piden algo que no tiene que ver con diseño o con la escuela, lo decís con amabilidad y volvés al tema.
Si no estás seguro de un dato técnico, lo aclarás. Nunca inventes precios, fechas ni políticas de la escuela.`;

// Base de conocimiento: índice de las 320 clases, generado con tools/kb.py
type Clase = { c: string; s: number; d: number; t: string; o: string; u: string; h: string[]; l: string; a: string; n: string };
const KB = conocimiento as { cursos: Record<string, { nombre: string; semanas: string[] }>; clases: Clase[] };

const VACIAS = new Set("para como cual cuál cuando donde dónde esta este esto estos estas tiene tienen sobre entre desde hasta porque pero sino hace hacer puedo puede pueden quiero tengo tenes tenés sus las los del que qué una uno unos unas con por mas más muy ser son era fue hay todo toda todos todas otra otro clase clases semana diplomatura curso boceto".split(" "));
const norm = (t: string) => t.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
const palabras = (t: string) => norm(t).match(/[a-z0-9ñ.]{3,}/g)?.map((w) => w.replace(/\.+$/, "")).filter((w) => w.length > 2 && !VACIAS.has(w)) ?? [];

let indice: { fuerte: Set<string>; resto: Set<string> }[] | null = null;
let idf: Map<string, number> | null = null;
function preparar() {
  if (indice) return;
  indice = KB.clases.map((k) => ({
    fuerte: new Set(palabras([k.t, k.o, ...k.h].join(" "))),
    resto: new Set(palabras([k.l, k.a, k.n].join(" ")))
  }));
  const df = new Map<string, number>();
  for (const i of indice) for (const w of new Set([...i.fuerte, ...i.resto])) df.set(w, (df.get(w) || 0) + 1);
  idf = new Map([...df].map(([w, n]) => [w, Math.log(1 + KB.clases.length / n)]));
}

// Devuelve el bloque de material para la pregunta: programa resumido + clases relacionadas.
function material(pregunta: string, pagina: string): string {
  preparar();
  const m = /^\/cursos\/([a-z]+)(?:\/semana-(\d+)\/clase-(\d))?/.exec(pagina || "");
  const curso = m && KB.cursos[m[1]] ? m[1] : "";
  const actual = m && m[2] ? `/cursos/${m[1]}/semana-${m[2]}/clase-${m[3]}.html` : "";
  // Las palabras con números (leyes, normas: 27.521, 4504) valen más
  const q = [...new Set(palabras(pregunta))];
  const puntajes = KB.clases.map((k, i) => {
    let p = 0;
    for (const w of q) {
      const v = idf!.get(w) || 0;
      const peso = /\d/.test(w) ? 2 : 1;
      if (indice![i].fuerte.has(w)) p += 2 * v * peso;
      else if (indice![i].resto.has(w)) p += v * peso;
    }
    if (p > 0 && curso && k.c === curso) p *= 1.3;
    return { k, p };
  }).filter((x) => x.p > 0 && x.k.u !== actual).sort((a, b) => b.p - a.p).slice(0, 4);

  const prog = Object.entries(KB.cursos).map(([slug, c]) =>
    `${c.nombre} (/cursos/${slug}/programa.html): ` + c.semanas.map((t, i) => `${i + 1}. ${t}`).join("; ")).join("\n");
  const clases = puntajes.map(({ k }) => {
    const n = KB.cursos[k.c]?.nombre || k.c;
    return [`• ${n}, semana ${k.s} (${k.t}), clase ${k.d} — ${k.u}`,
      k.o && `Objetivo: ${k.o}`,
      k.h.length ? `Temas: ${k.h.join("; ")}` : "",
      k.l && `Resumen: ${k.l}`,
      k.a && `Referentes: ${k.a}`,
      k.n && `Norma: ${k.n}`].filter(Boolean).join("\n");
  }).join("\n\n");
  return `\n\nAbajo tenés el MATERIAL DE BOCETO: el programa de las diplomaturas y las clases que más se relacionan con la pregunta. Basate en él antes que en tu conocimiento general. Cuando una clase responda la duda, nombrala (diplomatura, semana y clase) y pasá su enlace tal cual aparece (empieza con /cursos/). Sobre normas y referentes, citá solo lo que figura en el material; si no está, decí que no lo tenés verificado. Las normas pueden cambiar: sugerí confirmar la versión vigente cuando importe.\n\nMATERIAL DE BOCETO\nPrograma (16 semanas por diplomatura):\n${prog}` +
    (clases ? `\n\nClases relacionadas con la pregunta:\n${clases}` : "") +
    (actual ? `\n\nEl alumno está mirando la clase ${actual}; su contenido viene en el mensaje.` : "");
}

const CLAUDE_MODELS = ["claude-sonnet-5-5", "claude-haiku-5-5", "claude-sonnet-4-5", "claude-haiku-4-5"];
// Gratis dentro del cupo diario de Workers AI. Gemma 4 es el más capaz y el que menos cupo gasta; los otros quedan de respaldo.
const WORKERS_MODELS = ["@cf/google/gemma-4-26b-a4b-it", "@cf/meta/llama-4-scout-17b-16e-instruct", "@cf/meta/llama-3.2-11b-vision-instruct"];
const MAX_CHARS = 24000;
const MAX_IMAGE_B64 = 5_000_000; // ~3,7 MB de imagen
const IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"];

type Turn = { role: "user" | "assistant"; content: string };
type Image = { data: string; mediaType: string } | undefined;

const fail = (error: string, status: number) => Response.json({ error }, { status });

// Límite simple por visitante: 20 consultas por minuto (por instancia del servidor).
const hits = new Map<string, number[]>();
function limited(ip: string) {
  const now = Date.now(), win = hits.get(ip)?.filter((t) => now - t < 60_000) ?? [];
  win.push(now); hits.set(ip, win);
  if (hits.size > 5000) hits.clear();
  return win.length > 20;
}

async function claude(env: Env, turns: Turn[], image: Image, maxTokens: number, system: string): Promise<Response | null> {
  const messages = turns.map((t, i) => i === turns.length - 1 && image
    ? { role: "user", content: [{ type: "image", source: { type: "base64", media_type: image.mediaType, data: image.data } }, { type: "text", text: t.content }] }
    : { role: t.role, content: t.content });
  const models = env.ASISTENTE_MODEL ? [env.ASISTENTE_MODEL, ...CLAUDE_MODELS] : CLAUDE_MODELS;
  for (const model of models) {
    let res: Response;
    try {
      res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "content-type": "application/json", "x-api-key": env.ANTHROPIC_API_KEY!, "anthropic-version": "2023-06-01" },
        body: JSON.stringify({ model, max_tokens: maxTokens, system, messages })
      });
    } catch (e) { console.error("asistente: sin conexión con Claude", e); return null; }
    if (res.ok) {
      const data: any = await res.json();
      const text = (data.content || []).filter((b: any) => b.type === "text").map((b: any) => b.text).join("").trim();
      if (!text) return fail("empty_completion", 502);
      return Response.json({ text, truncated: data.stop_reason === "max_tokens", model });
    }
    const detail = await res.text().catch(() => "");
    console.error(`asistente: ${model} respondió ${res.status}`, detail.slice(0, 400));
    if (res.status === 429) return fail("rate_limited", 429);
    if (res.status === 404 || (res.status === 400 && /model/i.test(detail))) continue;
    return null; // clave inválida, sin saldo, etc.: probamos con Workers AI
  }
  return null;
}

// Workers AI a veces devuelve la respuesta ya convertida en objeto cuando el modelo escribió JSON
function textoDe(out: any): string {
  const r = out?.response ?? out?.result?.response ?? out?.choices?.[0]?.message?.content;
  if (r == null) return "";
  return (typeof r === "string" ? r : JSON.stringify(r)).trim();
}

async function workersAI(env: Env, turns: Turn[], image: Image, maxTokens: number, system: string, json = false): Promise<Response> {
  if (!env.AI) return fail("ai_unavailable", 503);
  const messages: any[] = [{ role: "system", content: system }];
  turns.forEach((t, i) => {
    if (i === turns.length - 1 && image) {
      messages.push({ role: "user", content: [
        { type: "text", text: t.content },
        { type: "image_url", image_url: { url: `data:${image.mediaType};base64,${image.data}` } }
      ] });
    } else messages.push({ role: t.role, content: t.content });
  });
  const models = env.WORKERS_AI_MODEL ? [env.WORKERS_AI_MODEL, ...WORKERS_MODELS] : WORKERS_MODELS;
  for (const model of models) {
    try {
      let out: any;
      if (json && !image) {
        try { out = await env.AI.run(model, { messages, max_tokens: maxTokens, response_format: { type: "json_object" } }); }
        catch (e: any) { console.error(`asistente: ${model} sin modo JSON`, String(e?.message || e).slice(0, 200)); }
      }
      if (!textoDe(out)) out = await env.AI.run(model, { messages, max_tokens: maxTokens });
      const text = textoDe(out);
      if (text) return Response.json({ text, truncated: false, model });
      console.error(`asistente: ${model} respondió vacío`, JSON.stringify(out).slice(0, 300));
    } catch (e: any) {
      const msg = String(e?.message || e);
      console.error(`asistente: ${model} falló`, msg.slice(0, 400));
      if (/limit|quota|neuron/i.test(msg)) return fail("rate_limited", 429);
    }
  }
  return fail("ai_unavailable", 503);
}

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  if (limited(request.headers.get("cf-connecting-ip") || "anon")) return fail("rate_limited", 429);

  let body: any;
  try { body = await request.json(); } catch { return fail("bad_request", 400); }

  const turns: Turn[] = Array.isArray(body?.messages) ? body.messages : [];
  if (!turns.length || turns.length > 24) return fail("bad_request", 400);
  let chars = 0;
  for (const t of turns) {
    if ((t?.role !== "user" && t?.role !== "assistant") || typeof t?.content !== "string" || !t.content.trim()) return fail("bad_request", 400);
    chars += t.content.length;
  }
  if (turns[0].role !== "user" || turns[turns.length - 1].role !== "user") return fail("bad_request", 400);
  if (chars > MAX_CHARS) return fail("too_large", 413);

  const image: Image = body?.image;
  if (image && (typeof image.data !== "string" || !IMAGE_TYPES.includes(image.mediaType) || image.data.length > MAX_IMAGE_B64)) {
    return fail("too_large", 413);
  }
  const maxTokens = Math.max(100, Math.min(2000, Number(body?.maxTokens) || 800));

  // La pregunta del alumno (sin el texto de la página que el sitio agrega al primer mensaje) busca en la base de conocimiento
  const ultima = turns[turns.length - 1].content;
  const pregunta = (ultima.split("Pregunta del alumno:").pop() || ultima).slice(-1500);
  const system = body?.json === true ? BASE : BASE + material(pregunta, typeof body?.pagina === "string" ? body.pagina : "");

  if (env.ANTHROPIC_API_KEY) {
    const r = await claude(env, turns, image, maxTokens, system);
    if (r) return r;
  }
  return workersAI(env, turns, image, maxTokens, system, body?.json === true);
};

export const onRequest: PagesFunction<Env> = async () => fail("method_not_allowed", 405);
