"""Genera el programa y las clases de un curso a partir de content/<curso>/temario.json y sNN.md.

Formato de cada semana (sNN.md):
    ## Clase 1
    Objetivo: una oración.
    Tiempos: 15, 35, 10        (opcional: lectura, práctica, repaso en minutos)
    ### Lectura
    markdown...
    ### Práctica
    markdown...
    ### Entrega                 (opcional)
    markdown...
    ### Repaso
    ? Pregunta
    - opción
    + opción correcta
    > explicación
"""
import json, re, sys, html, pathlib
import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
CURSO = sys.argv[1] if len(sys.argv) > 1 else "interiores"
SRC = ROOT / "content" / CURSO
OUT = ROOT / "public" / "cursos" / CURSO
T = json.loads((SRC / "temario.json").read_text(encoding="utf-8"))
esc = html.escape

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&amp;family=Inter:wght@400;500;600;700&amp;display=swap" rel="stylesheet">'
SPARK = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FDBA8C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/></svg>'

def cid(s, d): return f"s{s:02d}d{d}"
def url(s, d): return f"/cursos/{CURSO}/semana-{s:02d}/clase-{d}.html"

# Orden lineal de clases
SEQ = []
for u in T["unidades"]:
    for w in u["semanas"]:
        for i, titulo in enumerate(w["clases"], 1):
            SEQ.append({"u": u, "w": w, "d": i, "titulo": titulo, "id": cid(w["n"], i)})
TOTAL = len(SEQ)

def md(text):
    out = markdown.markdown(text.strip(), extensions=["tables", "sane_lists", "md_in_html"], output_format="html")
    return out.replace("<table>", '<div class="tabla"><table>').replace("</table>", "</table></div>")

def parse_quiz(text):
    qs, cur = [], None
    for line in text.strip().splitlines():
        line = line.rstrip()
        if line.startswith("? "):
            cur = {"q": line[2:].strip(), "opts": [], "exp": ""}; qs.append(cur)
        elif cur and line.startswith(("- ", "+ ")):
            cur["opts"].append((line[2:].strip(), line.startswith("+ ")))
        elif cur and line.startswith("> "):
            cur["exp"] += (" " if cur["exp"] else "") + line[2:].strip()
    for q in qs:
        if sum(1 for _, ok in q["opts"] if ok) != 1 or len(q["opts"]) < 2:
            raise SystemExit(f"Pregunta mal armada: {q['q']}")
    return qs

def inline(t):  # negritas simples dentro de preguntas
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(t))

def render_quiz(qs):
    parts = []
    for i, q in enumerate(qs, 1):
        opts = "\n".join(f'<button type="button" class="opt" data-ok="{1 if ok else 0}">{inline(t)}</button>' for t, ok in q["opts"])
        parts.append(f'''<div class="quiz" data-quiz>
<p class="q">{i}. {inline(q["q"])}</p>
<div class="opts" role="group" aria-label="Opciones de la pregunta {i}">
{opts}
</div>
<p class="fb ok" role="status" hidden><strong>¡Bien!</strong> {inline(q["exp"])}</p>
<p class="fb no" role="status" hidden><strong>Todavía no.</strong> Probá otra opción.</p>
</div>''')
    return "\n".join(parts)

def parse_week(n):
    f = SRC / f"s{n:02d}.md"
    if not f.exists(): return None
    text = f.read_text(encoding="utf-8")
    clases = {}
    chunks = re.split(r"^## Clase (\d)\s*$", text, flags=re.M)
    for i in range(1, len(chunks), 2):
        d, body = int(chunks[i]), chunks[i + 1]
        c = {"objetivo": "", "tiempos": (15, 35, 10), "secciones": {}}
        m = re.search(r"^Objetivo:\s*(.+)$", body, flags=re.M)
        if m: c["objetivo"] = m.group(1).strip()
        m = re.search(r"^Tiempos:\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*$", body, flags=re.M)
        if m: c["tiempos"] = tuple(int(x) for x in m.groups())
        secs = re.split(r"^### (.+?)\s*$", body, flags=re.M)
        for j in range(1, len(secs), 2):
            c["secciones"][secs[j].strip().lower()] = secs[j + 1]
        for need in ("lectura", "práctica", "repaso"):
            if need not in c["secciones"]: raise SystemExit(f"s{n:02d} clase {d}: falta la sección {need}")
        clases[d] = c
    return clases

WEEKS = {w["n"]: parse_week(w["n"]) for u in T["unidades"] for w in u["semanas"]}

# Gráficos adicionales por clase (content/<curso>/figuras.py), insertados al final de la lectura
FIGS = {}
_fp = SRC / "figuras.py"
if _fp.exists():
    sys.path.insert(0, str(ROOT / "tools"))
    import figlib, importlib.util
    figlib.usar(CURSO)
    _spec = importlib.util.spec_from_file_location("figuras_" + CURSO, _fp)
    _mod = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_mod)
    FIGS = _mod.FIGS

def imagen_comentada(texto):
    """### Imagen: primera línea ![alt](src "crédito"); el resto es la lectura de la imagen."""
    texto = texto.strip()
    m = re.match(r'!\[([^\]]*)\]\((\S+)(?:\s+"([^"]*)")?\)\s*', texto)
    if not m: return md(texto)
    alt, src, credito = m.group(1), m.group(2), m.group(3) or ""
    resto = texto[m.end():]
    return f'''<figure class="foto">
<img src="{esc(src)}" alt="{esc(alt)}" loading="lazy" decoding="async">
<figcaption>{inline(credito)}</figcaption>
</figure>
<div class="lectura">{md(resto)}</div>'''

def secciones_nuevas(s):
    out = {}
    if "imagen" in s:
        out["imagen"] = f'''<section class="bloque imagen" aria-labelledby="imagen-t">
<h2 id="imagen-t">Mirar con atención</h2>
{imagen_comentada(s["imagen"])}
</section>'''
    if "autores" in s:
        out["autores"] = f'''<section class="bloque autores" aria-labelledby="autores-t">
<h2 id="autores-t">Referentes de la región</h2>
<div class="lectura">{md(s["autores"])}</div>
</section>'''
    if "norma" in s:
        out["norma"] = f'''<section class="bloque norma" aria-labelledby="norma-t">
<h2 id="norma-t">La norma</h2>
<div class="lectura">{md(s["norma"])}</div>
</section>'''
    if "referencias" in s:
        out["referencias"] = f'''<section class="refs" aria-labelledby="refs-t">
<h2 id="refs-t">Referencias</h2>
<div class="lectura">{md(s["referencias"])}</div>
</section>'''
    return out

def figura_extra(cid_):
    if cid_ not in FIGS: return ""
    svg_, cap = FIGS[cid_]
    return f'<figure>\n{svg_}\n<figcaption>{esc(cap)}</figcaption>\n</figure>'


def header(back_href, back_text, toc=False):
    boton = ('<button type="button" class="c-toc-btn" data-toc aria-expanded="false" aria-controls="c-side">'
             '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h10"/></svg>Contenido</button>') if toc else ""
    return f'''<header class="c-header">
<div class="left">
<a class="s-logo c-logo" href="/" aria-label="boceto, inicio"><span class="marks" aria-hidden="true"><i></i><i></i><i></i><i></i></span>boceto</a>
<a class="back" href="{back_href}">{esc(back_text)}</a>
</div>
<div class="right">
{boton}
<span class="c-progress"><span class="c-progress-l">Tu progreso</span> <span class="bar" aria-hidden="true"><span data-progress-bar></span></span><b data-progress-text>0%</b></span>
<a class="btn btn-s panel-link" href="/panel.html">Mi panel</a>
</div>
</header>'''

def page(title, desc, body, extra_attrs=""):
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="/assets/base.css">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/curso.css">
</head>
<body data-curso="{CURSO}" data-total="{TOTAL}"{extra_attrs}>
{body}
<script src="/assets/sync.js" defer></script>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''

def sidebar(cur):
    parts = ['<aside class="c-side" id="c-side" aria-label="Contenido de la diplomatura">', '<div class="c-side-h"><h2>Contenido</h2><button type="button" class="c-toc-x" data-toc-cerrar aria-label="Cerrar el contenido">×</button></div>']
    for u in T["unidades"]:
        here = any(w["n"] == cur["w"]["n"] for w in u["semanas"])
        if not here:
            parts.append(f'<div class="c-unit"><a href="/cursos/{CURSO}/programa.html#unidad-{u["n"]}"><span class="c-unit-n">{u["n"]}</span>{esc(u["titulo"])}</a></div>')
            continue
        parts.append(f'<div class="c-unit current"><span><span class="c-unit-n">{u["n"]}</span>{esc(u["titulo"])}</span>')
        for w in u["semanas"]:
            parts.append(f'<div class="c-week"><p>Semana {w["n"]}: {esc(w["titulo"])}</p>')
            for d, t in enumerate(w["clases"], 1):
                if WEEKS.get(w["n"]) and d in WEEKS[w["n"]]:
                    curr = ' aria-current="page"' if (w["n"] == cur["w"]["n"] and d == cur["d"]) else ""
                    parts.append(f'<a href="{url(w["n"], d)}" data-cid="{cid(w["n"], d)}"{curr}><span class="dot" aria-hidden="true"></span>{d}. {esc(t)}</a>')
                else:
                    parts.append(f'<span class="c-week-soon" style="padding:8px 10px;font-size:14px;color:#8A8A8A">{d}. {esc(t)}</span>')
            parts.append("</div>")
        parts.append("</div>")
    if T.get("recursos"):
        parts.append('<h2 class="c-side-rec">Recursos</h2><div class="c-week">')
        for r in T["recursos"]:
            parts.append(f'<a href="/cursos/{CURSO}/{r["slug"]}.html">{esc(r["titulo"])}</a>')
        parts.append("</div>")
    parts.append("</aside>")
    return "\n".join(parts)

def recurso(r):
    text = (SRC / f'{r["slug"]}.md').read_text(encoding="utf-8")
    m = re.match(r"^# (.+)\n+(.+?)\n", text)
    titulo, bajada = (m.group(1), m.group(2)) if m else (r["titulo"], "")
    body_md = text[m.end():] if m else text
    body = f'''<!--s-head--><!--/s-head-->
<main class="c-main c-main-sola">
<article class="c-article c-article-ancho">
<nav class="c-migas" aria-label="Ruta"><a href="/cursos/{CURSO}.html">{esc(T["carrera"])}</a><span aria-hidden="true">/</span><a href="/cursos/{CURSO}/programa.html">Programa</a><span aria-hidden="true">/</span><span>Recursos</span></nav>
<h1>{esc(titulo)}</h1>
<p class="objetivo">{esc(bajada)}</p>
<section class="lectura">{md(body_md)}</section>
<nav class="pager" aria-label="Volver"><a href="/cursos/{CURSO}/programa.html"><span>Volver</span><b>Programa de la diplomatura</b></a></nav>
</article>
</main>
<!--s-foot--><!--/s-foot-->'''
    return page(f'{titulo} · boceto', bajada, body)

def lesson(idx):
    it = SEQ[idx]; w, u, d = it["w"], it["u"], it["d"]
    c = WEEKS[w["n"]][d]
    s = c["secciones"]
    t1, t2, t3 = c["tiempos"]
    prev_ = SEQ[idx - 1] if idx > 0 else None
    next_ = SEQ[idx + 1] if idx + 1 < TOTAL else None
    def avail(x): return x and WEEKS.get(x["w"]["n"]) and x["d"] in WEEKS[x["w"]["n"]]
    entrega = ""
    if "entrega" in s:
        entrega = f'''<section class="bloque entrega" aria-labelledby="entrega-t">
<h2 id="entrega-t">Entrega de la semana</h2>
<p class="entrega-n">{esc(w["entrega"])}</p>
<div class="lectura">{md(s["entrega"])}</div>
<a class="cta" href="/bocetador/?carrera={CURSO}&amp;clase={it["id"]}">Hacer la entrega en el Bocetador</a>
<p class="entregado" data-entrega="{it["id"]}" hidden></p>
</section>'''
    nuevas = secciones_nuevas(s)
    pager = ['<nav class="pager" aria-label="Clases">']
    if avail(prev_):
        pager.append(f'<a href="{url(prev_["w"]["n"], prev_["d"])}"><span>Anterior</span><b>{esc(prev_["titulo"])}</b></a>')
    if avail(next_):
        pager.append(f'<a class="next" href="{url(next_["w"]["n"], next_["d"])}"><span>Siguiente</span><b>{esc(next_["titulo"])}</b></a>')
    elif next_:
        pager.append(f'<a class="next" href="/cursos/{CURSO}/programa.html"><span>Próxima clase en preparación</span><b>Ver el programa</b></a>')
    pager.append("</nav>")
    body = f'''{header(f"/cursos/{CURSO}/programa.html", T["carrera"], toc=True)}
<div class="c-velo" data-toc-cerrar hidden></div>
<div class="c-layout">
{sidebar(it)}
<main class="c-main" id="clase">
<article class="c-article">
<div class="c-ubic"><p class="eyebrow">Unidad {u["n"]}, semana {w["n"]}: {esc(w["titulo"])}</p>
<nav class="c-pasos" aria-label="Clases de esta semana">{"".join((f'<a href="{url(w["n"], k)}" data-cid="{cid(w["n"], k)}"' + (' aria-current="page"' if k == d else '') + f' title="Clase {k}: {esc(w["clases"][k-1])}"><span class="sr">Clase {k}: {esc(w["clases"][k-1])}</span></a>') if (WEEKS.get(w["n"]) and k in WEEKS[w["n"]]) else f'<span class="c-paso-off"></span>' for k in range(1, 6))}<span class="c-pasos-t">Clase {d} de 5</span></nav></div>
<h1>{esc(it["titulo"])}</h1>
<p class="objetivo">{esc(c["objetivo"])}</p>
<ul class="tiempos" aria-label="Tiempos de la clase"><li>Lectura <b>{t1} min</b></li><li>Práctica <b>{t2} min</b></li><li>Repaso <b>{t3} min</b></li></ul>
<section class="lectura" aria-label="Lectura">
{md(s["lectura"])}
{figura_extra(it["id"])}
</section>
{nuevas.get("imagen", "")}
{nuevas.get("autores", "")}
<section class="bloque practica" aria-labelledby="practica-t">
<h2 id="practica-t">Práctica <span class="min">{t2} min</span></h2>
<div class="lectura">{md(s["práctica"])}</div>
{"" if "entrega" in s else f'<a class="cta-suave" href="/bocetador/?carrera={CURSO}&amp;clase={it["id"]}">Hacer la práctica en el Bocetador</a><p class="entregado" data-entrega="{it["id"]}" hidden></p>'}
</section>
{entrega}
<section class="repaso" aria-labelledby="repaso-t">
<h2 id="repaso-t">Repaso <span class="min">{t3} min</span></h2>
{render_quiz(parse_quiz(s["repaso"]))}
</section>
{nuevas.get("norma", "")}
{nuevas.get("referencias", "")}
<section class="asistente" aria-labelledby="asistente-titulo">
<div class="head"><span class="ico" aria-hidden="true">{SPARK}</span><div><h2 id="asistente-titulo">Preguntale al asistente</h2><p class="sub">Conoce esta clase y toda la diplomatura. Responde a cualquier hora.</p></div></div>
<div id="chat" class="c-chat"></div>
<div class="chips"><button type="button">Explicámelo con otro ejemplo</button><button type="button">Haceme una pregunta de práctica</button><button type="button">{esc(T.get("chip", "¿Cómo aplico esto en mi living?"))}</button></div>
<form data-chat="form"><label class="sr" for="pregunta">Tu pregunta</label><button type="button" class="c-adj" aria-label="Adjuntar imagen"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-9 8"/></svg></button><input id="pregunta" type="text" placeholder="Escribí tu duda sobre esta clase" autocomplete="off"><button type="submit">Enviar</button></form>
<p class="nota">El asistente puede equivocarse. Ante una duda importante, contrastá con la lectura.</p>
</section>
<div class="cierre">
<button type="button" class="completar" data-complete="{it["id"]}" aria-pressed="false">Marcar clase como completada</button>
{"".join(pager)}
</div>
</article>
</main>
</div>'''
    title = f'{it["titulo"]} · Semana {w["n"]} · boceto'
    return page(title, c["objetivo"] or T["bajada"], body, f' data-clase="{it["id"]}"')

def programa():
    first = next((x for x in SEQ if WEEKS.get(x["w"]["n"]) and x["d"] in WEEKS[x["w"]["n"]]), None)
    units = []
    for u in T["unidades"]:
        weeks = []
        for w in u["semanas"]:
            items = []
            for d, t in enumerate(w["clases"], 1):
                if WEEKS.get(w["n"]) and d in WEEKS[w["n"]]:
                    items.append(f'<a href="{url(w["n"], d)}" data-cid="{cid(w["n"], d)}"><span class="dot" aria-hidden="true"></span>{d}. {esc(t)}</a>')
                else:
                    items.append(f'<span class="soon"><span class="dot dot-soon" aria-hidden="true"></span>{d}. {esc(t)} · próximamente</span>')
            weeks.append(f'''<div class="p-week"><h3><small>Semana {w["n"]}</small>{esc(w["titulo"])}</h3>
{"".join(items)}
<p class="entrega-tag">Entrega: {esc(w["entrega"])}</p></div>''')
        units.append(f'''<section class="p-unit" id="unidad-{u["n"]}"><h2><span>{u["n"]}</span>{esc(u["titulo"])}</h2>
<div class="p-weeks">{"".join(weeks)}</div></section>''')
    if T.get("recursos"):
        cards = "".join(f'<a class="p-week" href="/cursos/{CURSO}/{r["slug"]}.html" style="text-decoration:none"><h3><small>Recurso</small>{esc(r["titulo"])}</h3><span class="p-rec">Abrir el recurso</span></a>' for r in T["recursos"])
        units.append(f'<section class="p-unit" id="recursos"><h2><span>+</span>Recursos para toda la diplomatura</h2><div class="p-weeks">{cards}</div></section>')
    start = f'<a class="p-start" href="{url(first["w"]["n"], first["d"])}" data-continue>Empezar la diplomatura</a>' if first else ""
    body = f'''<!--s-head--><!--/s-head-->
<section class="p-hero"><div class="in">
<nav class="c-migas" aria-label="Ruta"><a href="/#diplomaturas">Diplomaturas</a><span aria-hidden="true">/</span><a href="/cursos/{CURSO}.html">{esc(T["carrera"])}</a><span aria-hidden="true">/</span><span aria-current="page">Programa</span></nav>
<h1>{esc(T["titulo"])}</h1>
<p>{esc(T["bajada"])}</p>
<dl class="p-meta"><div><dt>Duración</dt><dd>16 semanas</dd></div><div><dt>Clases</dt><dd>80 de 1 hora</dd></div><div><dt>Ritmo</dt><dd>5 días por semana</dd></div><div><dt>Entregas</dt><dd>16 con corrección</dd></div></dl>
{start}
</div></section>
<main class="p-body">
{"".join(units)}
</main>
<!--s-foot--><!--/s-foot-->'''
    return page(f'Programa · {T["titulo"]} · boceto', T["bajada"], body)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import layout
_orig_page = page
def page(*a, **k): return layout.aplicar(_orig_page(*a, **k))
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "programa.html").write_text(programa(), encoding="utf-8")
for r in T.get("recursos", []):
    if (SRC / f'{r["slug"]}.md').exists():
        (OUT / f'{r["slug"]}.html').write_text(recurso(r), encoding="utf-8")
n = 0
for i, it in enumerate(SEQ):
    if WEEKS.get(it["w"]["n"]) and it["d"] in WEEKS[it["w"]["n"]]:
        p = OUT / f'semana-{it["w"]["n"]:02d}' / f'clase-{it["d"]}.html'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(lesson(i), encoding="utf-8"); n += 1

# Consignas para el Bocetador: la práctica o la entrega de cada clase, en texto plano
def plano(t, limite=520):
    t = re.sub(r"^\s*\|.*$", "", t, flags=re.M)               # tablas
    t = re.sub(r"^#+\s*", "", t, flags=re.M)                    # títulos
    t = re.sub(r"^\s*>\s?", "", t, flags=re.M)                 # citas
    t = re.sub(r"\*\*|__|`", "", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"^\s*[-*]\s+", "• ", t, flags=re.M)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"\n{2,}", "\n", t).strip()
    if len(t) > limite:
        corte = t.rfind("\n", 0, limite)                         # mejor cortar entre pasos
        if corte < limite * 0.5: corte = t.rfind(". ", 0, limite) + 1
        t = t[: corte if corte > limite * 0.4 else limite].rstrip() + " …"
    return t
consignas = {}
for it in SEQ:
    c = WEEKS.get(it["w"]["n"], {}).get(it["d"])
    if not c: continue
    sec = c["secciones"]; es_entrega = "entrega" in sec
    consignas[it["id"]] = {"t": it["w"]["entrega"] if es_entrega else it["titulo"], "k": f'Semana {it["w"]["n"]} · Clase {it["d"]}',
                           "c": (plano(sec["práctica"], 420) + "\nPara entregar: " + plano(sec["entrega"], 300)) if es_entrega else plano(sec["práctica"]), "e": es_entrega, "u": url(it["w"]["n"], it["d"])}
(OUT / "consignas.json").write_text(json.dumps(consignas, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"ok programa + {n} clases de {TOTAL} · {len(consignas)} consignas")
