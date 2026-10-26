"""Arma /bocetador/index.html a partir del Bocetador publicado como artifact, con adaptadores para el sitio."""
import pathlib, sys

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2])

ADAPTERS = r'''/* ---------- Adaptadores: en el sitio, el asistente va por /api/asistente y las descargas son locales ---------- */
async function getDownloads() {
  if (window.claude && window.claude.use) { const d = await window.claude.use("downloads"); if (d) return d; }
  return {
    async save({ filename, data }) {
      const blob = data instanceof Blob ? data : new Blob([data]);
      const url = URL.createObjectURL(blob), a = document.createElement("a");
      a.href = url; a.download = filename; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 5000);
      return { status: "saved" };
    }
  };
}
async function getSample() {
  if (window.claude && window.claude.use) { const s = await window.claude.use("sample"); if (s) return s; }
  const toJpeg = async (blob) => {
    const bmp = await createImageBitmap(blob);
    const k = Math.min(1, 1568 / Math.max(bmp.width, bmp.height));
    const c = document.createElement("canvas"); c.width = Math.round(bmp.width * k); c.height = Math.round(bmp.height * k);
    const x = c.getContext("2d"); x.fillStyle = "#FFFFFF"; x.fillRect(0, 0, c.width, c.height); x.drawImage(bmp, 0, 0, c.width, c.height);
    return { mediaType: "image/jpeg", data: c.toDataURL("image/jpeg", 0.85).split(",")[1] };
  };
  const looseJson = (t) => {
    try { return JSON.parse(t); } catch (e) {}
    const f = /```(?:json)?\s*([\s\S]*?)```/.exec(t); if (f) { try { return JSON.parse(f[1]); } catch (e) {} }
    const a = t.search(/[\[{]/), b = Math.max(t.lastIndexOf("}"), t.lastIndexOf("]"));
    if (a >= 0 && b > a) { try { return JSON.parse(t.slice(a, b + 1)); } catch (e) {} }
    return undefined;
  };
  const call = async (input, opts = {}) => {
    const body = { messages: typeof input === "string" ? [{ role: "user", content: input }] : input, maxTokens: 900 };
    if (opts.images) {
      const img = Array.isArray(opts.images) ? opts.images[0] : (opts.images instanceof FileList ? opts.images[0] : opts.images);
      try { body.image = await toJpeg(img); } catch (e) { throw { code: "image_rejected", message: String(e) }; }
    }
    let res;
    try { res = await fetch("/api/asistente", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body), signal: opts.signal }); }
    catch (e) { throw { code: e && e.name === "AbortError" ? "cancelled" : "upstream_error", message: String(e) }; }
    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.text) throw { code: data.error || "upstream_error", message: "HTTP " + res.status };
    if (opts.onText) opts.onText({ text: data.text, delta: data.text });
    return { text: data.text, truncated: !!data.truncated, modelTierApplied: "default" };
  };
  call.json = async (input, opts = {}) => {
    const { text } = await call(input, Object.assign({}, opts, { onText: undefined }));
    const v = looseJson(text);
    if (v === undefined) throw { code: "invalid_json", message: "sin JSON", text };
    return v;
  };
  call.limits = async () => ({ maxPromptBytes: 65536, images: { maxCount: 1, maxInputBytes: 20000000, mediaTypes: ["image/jpeg", "image/png", "image/webp"] } });
  return call;
}

/* ---------- Capacidades: descargas y asistente ---------- */'''

def rep(s, old, new):
    if old not in s:
        raise SystemExit(f"no encontré: {old[:80]!r}")
    return s.replace(old, new, 1)

s = src
s = rep(s, '<div class="brand"><span class="marks" aria-hidden="true"><i></i><i></i><i></i><i></i></span><b>boceto</b><span>Bocetador</span></div>',
        '<a class="brand" href="/" aria-label="boceto, ir al inicio" style="text-decoration:none;color:inherit"><span class="marks" aria-hidden="true"><i></i><i></i><i></i><i></i></span><b>boceto</b><span>Bocetador</span></a>')
s = rep(s, "/* ---------- Capacidades: descargas y asistente ---------- */", ADAPTERS)
s = rep(s, 'const dl = window.claude && window.claude.use ? await window.claude.use("downloads") : null;', "const dl = await getDownloads();")
s = rep(s, 'const sample = window.claude && window.claude.use ? await window.claude.use("sample") : null;', "const sample = await getSample();")
s = rep(s, 'empty_completion: "No llegó respuesta. Probá de nuevo."',
        'empty_completion: "No llegó respuesta. Probá de nuevo.",\n    ai_unavailable: "El asistente todavía no está activo en este sitio.", too_large: "La imagen es muy pesada. Probá con una foto más chica."')

head_end = s.index("</style>") + len("</style>")
head_part, body_part = s[:head_end], s[head_end:]
head_part = head_part.replace("<title>Bocetador boceto</title>", "")

doc = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Bocetador · boceto</title>
<meta name="description" content="Programa de dibujo asistido para Interiores, Industrial, Gráfico e Indumentaria: grillas, perspectiva, cotas, simetría, figurín y corrección con IA de croquis en papel.">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<style>[hidden]{{display:none!important}} img{{max-width:100%}}</style>
{head_part.strip()}
</head>
<body>
{body_part.strip()}
</body>
</html>
"""
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(doc, encoding="utf-8")
print("ok", out)
