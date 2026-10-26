"""Copia public/ a una vista previa con rutas relativas, para publicarla como página privada."""
import pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "public"
OUT = pathlib.Path(sys.argv[1])
if OUT.exists(): shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)

def fix_url(url, rel):
    path, q, frag = url, "", ""
    if "#" in path: path, frag = path.split("#", 1); frag = "#" + frag
    if "?" in path: path, q = path.split("?", 1); q = "?" + q
    path = path.lstrip("/")
    if path == "" or path.endswith("/"): path += "index.html"
    return rel + path + q + frag

files = []
for f in OUT.rglob("*"):
    if f.is_file(): files.append(f)
    if f.suffix != ".html": continue
    depth = len(f.relative_to(OUT).parts) - 1
    rel = "../" * depth
    s = f.read_text(encoding="utf-8")
    s = re.sub(r'(href|src)="(/[^"/][^"]*|/)"', lambda m: f'{m.group(1)}="{fix_url(m.group(2), rel)}"', s)
    f.write_text(s, encoding="utf-8")

js = OUT / "assets" / "site.js"
s = js.read_text(encoding="utf-8")
s = s.replace('location.href = "/bocetador/?carrera=" + (document.body.dataset.curso || "interiores");',
              'location.href = document.querySelector(\'link[href$="assets/site.css"]\').getAttribute("href").replace("assets/site.css", "") + "bocetador/index.html?carrera=" + (document.body.dataset.curso || "interiores");')
s = s.replace('const BOC = "/bocetador/";',
              'const BOC = (document.querySelector(\'link[href*="assets/"][href$=".css"]\') || { getAttribute: () => "assets/" }).getAttribute("href").replace(/assets\\/.*$/, "") + "bocetador/index.html";')
js.write_text(s, encoding="utf-8")

# Página de entrada de la vista previa (sin doctype: el publicador la envuelve)
(OUT / "vista-previa.html").write_text('''<title>Vista previa boceto</title>
<style>
:root{--bg:#FFFFFF;--fg:#111111;--muted:#555555;--line:#E2E2E2;--card:#F7F6F4;--acc:#C2410C}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#141414;--fg:#F2F2F2;--muted:#B5B5B5;--line:#333;--card:#1E1E1E;--acc:#F08A5B;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#141414;--fg:#F2F2F2;--muted:#B5B5B5;--line:#333;--card:#1E1E1E;--acc:#F08A5B;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:Inter,system-ui,sans-serif}
main{max-width:760px;margin:0 auto;padding:40px max(16px,env(safe-area-inset-left,0px));display:flex;flex-direction:column;gap:22px}
h1{margin:0;font-size:clamp(30px,5vw,44px);letter-spacing:-.03em;line-height:1.05}
p{margin:0;font-size:17px;line-height:1.55;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
a.card{display:flex;flex-direction:column;gap:6px;padding:18px;border-radius:18px;background:var(--card);border:1px solid var(--line);color:var(--fg);text-decoration:none}
a.card b{font-size:17px}a.card span{font-size:14px;color:var(--muted)}
a.card:hover{border-color:var(--acc)}
.note{font-size:14px}
</style>
<main>
<h1>boceto · vista previa del sitio</h1>
<p>Esta es la versión completa del sitio, navegable, para revisar antes de publicarla en Netlify. El asistente intenta responder con tu cuenta de Claude (la primera vez te pide permiso); si en alguna página no responde, es porque ahí necesita el sitio publicado.</p>
<div class="grid">
<a class="card" href="index.html"><b>Inicio</b><span>La landing de la escuela</span></a>
<a class="card" href="cursos/interiores/programa.html"><b>Programa de Interiores</b><span>16 semanas · 80 clases</span></a>
<a class="card" href="cursos/interiores/semana-01/clase-1.html"><b>Primera clase de Interiores</b><span>Bienvenida: cómo trabaja un interiorista</span></a>
<a class="card" href="cursos/interiores.html"><b>Ficha de Interiores</b><span>Lo que ve quien todavía no se anotó</span></a>
<a class="card" href="cursos/interiores/herramientas.html"><b>Caja de herramientas · Interiores</b><span>Software e IA por etapa</span></a>
<a class="card" href="cursos/interiores/proveedores.html"><b>Proveedores · Interiores</b><span>Ejemplos por rubro y criterios</span></a>
<a class="card" href="cursos/industrial/programa.html"><b>Programa de Industrial</b><span>16 semanas · 80 clases</span></a>
<a class="card" href="cursos/industrial/semana-01/clase-1.html"><b>Primera clase de Industrial</b><span>Cómo trabaja un diseñador industrial</span></a>
<a class="card" href="cursos/industrial.html"><b>Ficha de Industrial</b><span>Lo que ve quien todavía no se anotó</span></a>
<a class="card" href="cursos/industrial/herramientas.html"><b>Software con IA · Industrial</b><span>Programas y precios por etapa</span></a>
<a class="card" href="cursos/industrial/proveedores.html"><b>Proveedores y talleres · Industrial</b><span>Materiales, fabricación y certificación</span></a>
<a class="card" href="cursos/grafico/programa.html"><b>Programa de Gráfico</b><span>16 semanas · 80 clases</span></a>
<a class="card" href="cursos/grafico/semana-01/clase-1.html"><b>Primera clase de Gráfico</b><span>Qué hace un diseñador gráfico</span></a>
<a class="card" href="cursos/grafico.html"><b>Ficha de Gráfico</b><span>Lo que ve quien todavía no se anotó</span></a>
<a class="card" href="cursos/grafico/herramientas.html"><b>Software con IA · Gráfico</b><span>Programas y precios por tarea</span></a>
<a class="card" href="cursos/grafico/proveedores.html"><b>Imprentas y recursos · Gráfico</b><span>Papel, tipografías, bancos y registro</span></a>
<a class="card" href="cursos/indumentaria/programa.html"><b>Programa de Indumentaria</b><span>16 semanas · 80 clases · nuevo</span></a>
<a class="card" href="cursos/indumentaria/semana-01/clase-1.html"><b>Primera clase de Indumentaria</b><span>Cómo trabaja un diseñador de indumentaria</span></a>
<a class="card" href="cursos/indumentaria.html"><b>Ficha de Indumentaria</b><span>Lo que ve quien todavía no se anotó</span></a>
<a class="card" href="cursos/indumentaria/herramientas.html"><b>Software con IA · Indumentaria</b><span>Dibujo, moldería digital y 3D</span></a>
<a class="card" href="cursos/indumentaria/proveedores.html"><b>Textiles y talleres · Indumentaria</b><span>Telas, avíos, producción responsable</span></a>
<a class="card" href="panel.html"><b>Panel del alumno</b><span>Progreso, entregas y semana de estudio</span></a>
<a class="card" href="bocetador/index.html"><b>Bocetador</b><span>Dibujo asistido y corrección de croquis</span></a>
</div>
<p class="note">El progreso de las clases se guarda solo en este navegador. Los botones de compra todavía no cobran.</p>
</main>
''', encoding="utf-8")
print(len(files) + 1, "archivos")

# El índice del artefacto es la página de entrada: la home del sitio pasa a inicio.html
(OUT / "index.html").rename(OUT / "inicio.html")
for f in OUT.rglob("*.html"):
    s = f.read_text(encoding="utf-8")
    s2 = re.sub(r'(href|src)="((?:\.\./)*)index\.html', r'\1="\2inicio.html', s)
    if s2 != s: f.write_text(s2, encoding="utf-8")
