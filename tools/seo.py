"""SEO del sitio: robots.txt, sitemap.xml y, en cada página, canonical, Open Graph, datos estructurados y noindex donde corresponde.
Es idempotente: reemplaza el bloque <!-- seo --> ... <!-- /seo --> de cada <head>.
Correrlo después de regenerar páginas (build_curso.py, legales.py, etc.):  python3 tools/seo.py
"""
import json, re, pathlib, datetime, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
SITE = "https://bocetoo.app"
HOY = datetime.date.today().isoformat()
esc = lambda s: html.escape(s, quote=True)

CARRERAS = {
    "interiores": "Diseño de Interiores y Mobiliario",
    "industrial": "Diseño Industrial",
    "grafico": "Diseño Gráfico",
    "indumentaria": "Diseño de Indumentaria",
}
NOINDEX = {"panel.html", "acceso.html", "inscripcion.html", "404.html", "bocetador/index.html"}
ORG = {"@type": "EducationalOrganization", "name": "boceto", "url": SITE + "/", "logo": SITE + "/assets/favicon.svg", "email": "hola@bocetoo.app",
       "description": "Escuela de diseño online con diplomaturas de Interiores y Mobiliario, Industrial, Gráfico e Indumentaria."}

def url_de(rel):
    rel = rel.replace("\\", "/")
    if rel == "index.html": return SITE + "/"
    if rel.endswith("/index.html"): return f"{SITE}/{rel[:-10]}"
    return f"{SITE}/{rel[:-5] if rel.endswith('.html') else rel}"  # Cloudflare sirve las páginas sin ".html"

def set_title(s, t):
    return re.sub(r"<title>.*?</title>", f"<title>{esc(t)}</title>", s, count=1, flags=re.S)

def set_desc(s, d):
    tag = f'<meta name="description" content="{esc(d)}">'
    if re.search(r'<meta name="description" content="[^"]*">', s): return re.sub(r'<meta name="description" content="[^"]*">', tag, s, count=1)
    return s.replace("</title>", "</title>\n" + tag, 1)

def get(s, pat):
    m = re.search(pat, s, re.S)
    return html.unescape(m.group(1)).strip() if m else ""

indexables, cambiadas = [], 0
for path in sorted(PUB.rglob("*.html")):
    rel = path.relative_to(PUB).as_posix()
    if rel.startswith("_"): continue
    s = orig = path.read_text(encoding="utf-8")
    s = re.sub(r"\n?<!-- seo -->.*?<!-- /seo -->", "", s, flags=re.S)
    ld, og_img, tipo = [], f"{SITE}/assets/og/boceto.jpg", "website"

    m_clase = re.match(r"cursos/([a-z]+)/semana-(\d\d)/clase-(\d)\.html$", rel)
    m_ficha = re.match(r"cursos/([a-z]+)\.html$", rel)
    m_rec = re.match(r"cursos/([a-z]+)/(programa|herramientas|proveedores)\.html$", rel)
    privada = rel in NOINDEX or rel.startswith("aprender/") or (m_clase and not (m_clase.group(2) == "01" and m_clase.group(3) == "1"))

    if rel == "index.html":
        s = set_title(s, "boceto · Diplomaturas de diseño online: Interiores, Industrial, Gráfico e Indumentaria")
        s = set_desc(s, "Escuela de diseño online en Argentina. Diplomaturas de 16 semanas en Interiores y Mobiliario, Industrial, Gráfico e Indumentaria, con asistente de IA y bocetador. Primera clase gratis.")
        ld.append({**ORG, "@context": "https://schema.org"})
        ld.append({"@context": "https://schema.org", "@type": "WebSite", "name": "boceto", "url": SITE + "/", "inLanguage": "es-AR"})
    elif m_ficha and m_ficha.group(1) in CARRERAS:
        c = m_ficha.group(1); nombre = CARRERAS[c]
        T = json.loads((ROOT / "content" / c / "temario.json").read_text(encoding="utf-8"))
        s = set_title(s, f"Diplomatura en {nombre} online · 16 semanas · boceto")
        desc = f"Curso online de {nombre}: {T['bajada'][0].lower() + T['bajada'][1:]} Primera clase gratis."
        s = set_desc(s, desc if len(desc) <= 300 else desc[:297] + "…")
        og_img = f"{SITE}/assets/og/{c}.jpg"
        ld.append({"@context": "https://schema.org", "@type": "Course", "name": f"Diplomatura en {nombre}", "description": T["bajada"],
                   "inLanguage": "es-AR", "url": url_de(rel), "image": og_img,
                   "provider": {"@type": "Organization", "name": "boceto", "sameAs": SITE + "/"},
                   "educationalCredentialAwarded": "Certificado de finalización (curso libre)",
                   "offers": [{"@type": "Offer", "category": "Subscription", "price": 63000, "priceCurrency": "ARS", "url": f"{SITE}/inscripcion.html?plan=diplomatura&carrera={c}", "availability": "https://schema.org/InStock"}],
                   "hasCourseInstance": [{"@type": "CourseInstance", "courseMode": "Online", "courseWorkload": "PT80H",
                                          "courseSchedule": {"@type": "Schedule", "duration": "PT1H", "repeatFrequency": "Daily", "repeatCount": 80}}]})
    elif m_rec or (m_clase and not privada):
        c = (m_rec or m_clase).group(1)
        if c in CARRERAS: og_img = f"{SITE}/assets/og/{c}.jpg"
        tipo = "article"

    titulo = get(s, r"<title>(.*?)</title>") or "boceto"
    desc = get(s, r'<meta name="description" content="([^"]*)"')
    bloque = ["<!-- seo -->"]
    if privada:
        if 'name="robots"' not in s: bloque.append('<meta name="robots" content="noindex">')
    else:
        u = url_de(rel); indexables.append(rel)
        bloque += [f'<link rel="canonical" href="{u}">',
                   '<meta property="og:site_name" content="boceto">', '<meta property="og:locale" content="es_AR">',
                   f'<meta property="og:type" content="{tipo}">', f'<meta property="og:url" content="{u}">',
                   f'<meta property="og:title" content="{esc(titulo)}">', f'<meta property="og:description" content="{esc(desc)}">',
                   f'<meta property="og:image" content="{og_img}">', '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
                   '<meta name="twitter:card" content="summary_large_image">', '<meta name="theme-color" content="#111111">']
        for d in ld: bloque.append('<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>")
    bloque.append("<!-- /seo -->")
    s = s.replace("</head>", "\n".join(bloque) + "\n</head>", 1)
    if s != orig:
        path.write_text(s, encoding="utf-8"); cambiadas += 1

def prioridad(rel):
    if rel == "index.html": return "1.0"
    if re.match(r"cursos/[a-z]+\.html$", rel): return "0.9"
    if rel.endswith("programa.html"): return "0.8"
    return "0.5"

(PUB / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{url_de(r)}</loc><lastmod>{HOY}</lastmod><priority>{prioridad(r)}</priority></url>\n" for r in indexables) + "</urlset>\n", encoding="utf-8")
(PUB / "robots.txt").write_text(
    "User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /auth/\nDisallow: /panel\nDisallow: /acceso\nDisallow: /bocetador/\n\n"
    f"Sitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
print(f"páginas modificadas: {cambiadas} · indexables en el sitemap: {len(indexables)}")
print("\n".join(indexables))
