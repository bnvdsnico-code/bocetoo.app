"""Convierte los artboards .dc.html del lienzo de diseño en páginas estáticas del sitio."""
import re, sys, pathlib

SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])

PAGES = {
    "Main.dc.html": "index.html",
    "Ficha-Interiores.dc.html": "cursos/interiores.html",
    "Ficha-Industrial.dc.html": "cursos/industrial.html",
    "Ficha-Grafico.dc.html": "cursos/grafico.html",
    "Ficha-Indumentaria.dc.html": "cursos/indumentaria.html",
    "Leccion-Interiores.dc.html": "aprender/recorridos-y-pasos-libres.html",
    "Devolucion-Interiores.dc.html": "aprender/devolucion-diagrama-de-zonas.html",
    "Panel-Alumno.dc.html": "panel.html",
}
ROUTES = {k: "/" + v.replace("index.html", "") for k, v in PAGES.items()}
TITLES = {
    "index.html": "boceto · Escuela de diseño online",
    "cursos/interiores.html": "Tu primer living · boceto",
    "cursos/industrial.html": "Bocetado de producto · boceto",
    "cursos/grafico.html": "Identidad visual · boceto",
    "cursos/indumentaria.html": "Moldería base · boceto",
    "aprender/recorridos-y-pasos-libres.html": "Recorridos y pasos libres · boceto",
    "aprender/devolucion-diagrama-de-zonas.html": "Devolución · boceto",
    "panel.html": "Mi panel · boceto",
}
DESC = "Cursos online de Diseño de Interiores y Mobiliario, Industrial, Gráfico e Indumentaria, con un asistente de IA y un bocetador para practicar."

STATIC_OPTS = """<button type="button" class="q-opt" data-opt="a" aria-pressed="false" style="text-align: left; font-size: 16px; font-weight: 500; padding: 14px 18px; min-height: 52px; border-radius: 14px; border: 1.5px solid #CFCFCF; background: #FFFFFF; color: #111111; cursor: pointer">Unos 30 cm</button>
<button type="button" class="q-opt" data-opt="b" aria-pressed="false" style="text-align: left; font-size: 16px; font-weight: 500; padding: 14px 18px; min-height: 52px; border-radius: 14px; border: 1.5px solid #CFCFCF; background: #FFFFFF; color: #111111; cursor: pointer">Unos 90 cm</button>
<button type="button" class="q-opt" data-opt="c" aria-pressed="false" style="text-align: left; font-size: 16px; font-weight: 500; padding: 14px 18px; min-height: 52px; border-radius: 14px; border: 1.5px solid #CFCFCF; background: #FFFFFF; color: #111111; cursor: pointer">Más de 2 metros</button>"""

NOTES = [
    (1, "Bien resuelto", "#1D4ED8", "#1E3A8A", "El recorrido principal es claro", "Va de la puerta a la ventana rodeando la zona de estar, sin atravesarla. Es justo lo que buscamos en esta lección."),
    (2, "A corregir", "#C2410C", "#9A3412", "El paso junto a la biblioteca queda angosto", "Entre la biblioteca y el sillón quedan unos 55 cm, y por ahí pasa el recorrido principal. Correla o achicá el sillón para llegar a unos 90 cm."),
    (3, "A corregir", "#C2410C", "#9A3412", "La zona de lectura cruza el recorrido", "El camino hacia la ventana pasa por el medio del rincón de lectura. Probá llevar el sillón individual contra la pared derecha, más abajo."),
    (4, "Sugerencia", "#3A3A3A", "#3A3A3A", "Indicá la escala y el norte", "No es obligatorio en este ejercicio, pero te va a hacer falta en el proyecto final. Sumá una escala gráfica y una flecha de norte."),
]
def static_notes():
    out = []
    for n, kind, col, lab, title, body in NOTES:
        out.append(f"""<button type="button" class="note" data-pick="{n}" aria-pressed="{'true' if n == 1 else 'false'}" style="text-align: left; display: flex; gap: 14px; padding: 18px; border-radius: 18px; border: 1.5px solid #E2E2E2; background: #FFFFFF; color: #111111; cursor: pointer">
<span aria-hidden="true" style="width: 32px; height: 32px; border-radius: 50%; background: {col}; color: #FFFFFF; font-weight: 700; font-size: 15px; display: flex; align-items: center; justify-content: center; flex: none">{n}</span>
<span style="display: flex; flex-direction: column; gap: 6px"><span style="font-size: 13px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: {lab}">{kind}</span><span style="font-size: 16px; font-weight: 600; line-height: 1.35">{title}</span><span class="note-body" style="font-size: 15px; line-height: 1.55; color: #3A3A3A"{'' if n == 1 else ' hidden'}>{body}</span></span>
</button>""")
    return "\n".join(out)

def convert(name, html):
    title_out = PAGES[name]
    helmet = re.search(r"<helmet>(.*?)</helmet>", html, re.S).group(1)
    body = re.search(r"<x-dc>(.*)</x-dc>", html, re.S).group(1)
    body = re.sub(r"<helmet>.*?</helmet>", "", body, flags=re.S)

    # Repeticiones a contenido estático
    body = re.sub(r'<sc-for list="\{\{options\}\}".*?</sc-for>', STATIC_OPTS, body, flags=re.S)
    body = re.sub(r'<sc-for list="\{\{notes\}\}".*?</sc-for>', static_notes(), body, flags=re.S)

    # Condicionales: envoltorio neutro, visible u oculto según su estado inicial
    def sc_if(m):
        hidden = "" if m.group(2) == "true" else " hidden"
        return f'<div data-if="{m.group(1)}" style="display: contents"{hidden}>{m.group(3)}</div>'
    body = re.sub(r'<sc-if value="\{\{(\w+)\}\}" hint-placeholder-val="\{\{ (true|false) \}\}">(.*?)</sc-if>', sc_if, body, flags=re.S)

    # Eventos a ganchos de datos
    body = re.sub(r'onClick="\{\{pick(\d)\}\}"', r'data-pick="\1"', body)
    body = body.replace('onClick="{{check}}"', 'data-action="check"')
    body = body.replace('onClick="{{toggleCal}}"', 'data-action="toggle-cal"')
    body = body.replace('onSubmit="{{noSubmit}}"', 'data-chat="form"')
    body = body.replace("{{accent}}", "#111111")
    leftover = re.findall(r"\{\{[^}]*\}\}|onClick=|<sc-", body)
    if leftover:
        raise SystemExit(f"{name}: quedaron plantillas sin convertir: {leftover[:5]}")

    # Rutas
    for src, route in ROUTES.items():
        body = body.replace(f'href="{src}"', f'href="{route}"')
    return helmet, body, title_out

def page(helmet, body, out_name, extra_head=""):
    title = TITLES[out_name]
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{DESC}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{helmet.strip()}
<link rel="stylesheet" href="/assets/site.css">
{extra_head}</head>
<body>
{body.strip()}
<script src="/assets/site.js" defer></script>
</body>
</html>
"""

for name, out_name in PAGES.items():
    html = (SRC / name).read_text(encoding="utf-8")
    helmet, body, _ = convert(name, html)
    (OUT / out_name).parent.mkdir(parents=True, exist_ok=True)
    (OUT / out_name).write_text(page(helmet, body, out_name), encoding="utf-8")
    print("ok", out_name)
