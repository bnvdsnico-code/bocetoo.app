"""Encabezado y pie comunes del sitio.
Reemplaza en cada página los bloques <!--s-head-->…<!--/s-head--> y <!--s-foot-->…<!--/s-foot-->,
y asegura que estén base.css y nav.js. Idempotente. Uso: python3 tools/layout.py
(build_curso.py y paginas.py lo importan para usar los mismos bloques)."""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"

MARKS = '<span class="marks" aria-hidden="true"><i></i><i></i><i></i><i></i></span>'

def head(util=True):
    u = ('<div class="s-util"><div class="wrap"><a href="/arrepentimiento.html">Botón de arrepentimiento</a>'
         '<a href="/baja.html">Botón de baja de servicio</a></div></div>\n') if util else ""
    return ("<!--s-head-->\n" + u +
        '<header class="s-head"><div class="wrap s-head-in">\n'
        f'<a class="s-logo" href="/" aria-label="boceto, inicio">{MARKS}boceto</a>\n'
        '<nav class="s-nav" id="s-nav" aria-label="Principal">'
        '<a href="/#diplomaturas">Diplomaturas</a><a href="/#como-se-estudia">Cómo se estudia</a>'
        '<a href="/bocetador/">Bocetador</a><a href="/#planes">Planes</a></nav>\n'
        '<div class="s-acc"><a class="btn btn-quiet btn-s" href="/acceso.html?volver=/panel.html" data-anon>Ingresar</a>'
        '<a class="btn btn-ink btn-s" href="/#diplomaturas" data-anon>Probar gratis</a>'
        '<a class="s-me" href="/panel.html" data-user hidden><span class="s-av" aria-hidden="true"></span><span class="s-me-t">Mi panel</span></a></div>\n'
        '<button class="s-burger" type="button" aria-expanded="false" aria-controls="s-nav"><span></span><span class="sr">Menú</span></button>\n'
        "</div></header>\n<!--/s-head-->")

def foot():
    return ("<!--s-foot-->\n"
        '<footer class="s-foot"><div class="wrap">\n<div class="s-foot-in">\n'
        f'<div class="s-foot-brand"><a class="s-logo" href="/">{MARKS}boceto</a>'
        '<p>Escuela de diseño online. Diplomaturas de 16 semanas para aprender haciendo, con el Bocetador y un asistente que te corrige.</p></div>\n'
        '<div><h2>Diplomaturas</h2><ul>'
        '<li><a href="/cursos/interiores.html">Interiores y Mobiliario</a></li><li><a href="/cursos/industrial.html">Diseño Industrial</a></li>'
        '<li><a href="/cursos/grafico.html">Diseño Gráfico</a></li><li><a href="/cursos/indumentaria.html">Diseño de Indumentaria</a></li></ul></div>\n'
        '<div><h2>La escuela</h2><ul>'
        '<li><a href="/bocetador/">Bocetador</a></li><li><a href="/#planes">Planes y precios</a></li>'
        '<li><a href="/panel.html">Mi panel</a></li><li><a href="mailto:hola@bocetoo.app">hola@bocetoo.app</a></li></ul></div>\n'
        '<div><h2>Legales</h2><ul>'
        '<li><a href="/arrepentimiento.html">Botón de arrepentimiento</a></li><li><a href="/baja.html">Botón de baja de servicio</a></li>'
        '<li><a href="/terminos.html">Términos y condiciones</a></li><li><a href="/privacidad.html">Privacidad</a></li></ul></div>\n'
        '</div>\n<div class="s-foot-legal"><span>boceto · bocetoo.app</span><span>Cursos libres de formación: no otorgan título oficial.</span></div>\n'
        "</div></footer>\n<!--/s-foot-->")

FUENTES = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
           '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&amp;family=Inter:wght@400;500;600;700&amp;display=swap" rel="stylesheet">')
HEAD_LINKS = '<link rel="stylesheet" href="/assets/base.css">'
NAV_JS = '<script src="/assets/nav.js" defer></script>'

def migrar(s: str) -> str:
    """Pasa una página de trámite vieja (encabezado i-top) al encabezado y pie comunes."""
    s = re.sub(r'<div class="consumidor-bar".*?</div>\n?', "", s, flags=re.S)
    s = re.sub(r'<header class="i-top">.*?</header>', "<!--s-head--><!--/s-head-->", s, flags=re.S)
    s = re.sub(r'\s*<p class="i-kick">[^<]*</p>', "", s)
    s = s.replace('<link rel="stylesheet" href="/assets/site.css">\n', "")
    s = re.sub(r'<link rel="preconnect" href="https://fonts.googleapis.com">(<link rel="preconnect"[^>]*>)?\n?<link href="https://fonts.googleapis.com/css2[^>]*>', "", s)
    if "fonts.googleapis.com/css2" not in s: s = s.replace("</title>", "</title>\n" + FUENTES, 1)
    s = s.replace('<main class="i-main">', '<main class="i-main wrap">')
    if "<!--s-foot-->" not in s and "<!--s-head-->" in s: s = s.replace("</body>", "<!--s-foot--><!--/s-foot-->\n</body>", 1)
    return aplicar(s)

def aplicar(s: str) -> str:
    s = re.sub(r"<!--s-head-->.*?<!--/s-head-->", lambda m: head(), s, flags=re.S)
    s = re.sub(r"<!--s-foot-->.*?<!--/s-foot-->", lambda m: foot(), s, flags=re.S)
    if "<!--/s-head-->" in s:
        if HEAD_LINKS not in s: s = s.replace("</title>", "</title>\n" + HEAD_LINKS, 1)
        if NAV_JS not in s: s = s.replace("</body>", NAV_JS + "\n</body>", 1)
    return s

if __name__ == "__main__":
    n = 0
    for p in PUB.rglob("*.html"):
        s = p.read_text(encoding="utf-8")
        if "<!--s-head-->" not in s and "<!--s-foot-->" not in s: continue
        t = aplicar(s)
        if t != s: p.write_text(t, encoding="utf-8"); n += 1
    print("páginas con encabezado común actualizadas:", n)
