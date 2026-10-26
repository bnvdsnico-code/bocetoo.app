"""Ajustes del sitio publicado sobre las páginas convertidas: navegación real, Bocetador y textos honestos."""
import pathlib, sys

PUB = pathlib.Path(sys.argv[1])

def patch(rel, pairs):
    p = PUB / rel
    s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if old not in s:
            raise SystemExit(f"{rel}: no encontré el texto a reemplazar: {old[:70]!r}")
        s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")
    print("ok", rel)

patch("index.html", [
    ('<a href="#planes" style="text-decoration: none">Planes</a>',
     '<a href="#planes" style="text-decoration: none">Planes</a>\n<a href="/bocetador/" style="text-decoration: none">Bocetador</a>'),
    ('<a href="#planes">Planes</a>', '<a href="#planes">Planes</a>\n<a href="/bocetador/">Bocetador</a>'),
    ('href="https://claude.ai/artifact/XqrbYnrFXysxJpoN4aBfy5"', 'href="/bocetador/"'),
])

LISTOS = {"interiores", "industrial", "grafico", "indumentaria"}  # cursos con clases publicadas
CARRERA = {"interiores": "interiores", "industrial": "industrial", "grafico": "grafico", "indumentaria": "indumentaria"}
for slug in CARRERA:
    pairs = [
        ('<a href="/" style="text-decoration: none">Disciplinas</a>', '<a href="/#disciplinas" style="text-decoration: none">Disciplinas</a>'),
        ('<a href="/" style="text-decoration: none">Cursos</a>', '<a href="/#cursos" style="text-decoration: none">Cursos</a>'),
        ('<a href="/" style="text-decoration: none">Planes</a>', '<a href="/#planes" style="text-decoration: none">Planes</a>\n<a href="/bocetador/?carrera=' + slug + '" style="text-decoration: none">Bocetador</a>'),
        ('<a href="/" style="text-decoration: none; text-align: center;', '<a href="/#planes" style="text-decoration: none; text-align: center;'),
        ('<a href="/">Cursos</a><a href="/">Planes</a>', '<a href="/#cursos">Cursos</a><a href="/#planes">Planes</a><a href="/bocetador/">Bocetador</a>'),
    ]
    if slug not in LISTOS:
        pairs.append(('<a href="#comprar" style="font-size: 15px; font-weight: 600;', '<a href="/bocetador/?carrera=' + slug + '" style="font-size: 15px; font-weight: 600;'))
        pairs.append(('Probar la primera lección gratis →', 'Practicar gratis en el Bocetador →'))
    else:
        pairs.append(('href="https://boceto-escuela-diseno.netlify.app/cursos/' + slug + '/programa.html"', 'href="/cursos/' + slug + '/programa.html"'))
    if slug in LISTOS and slug != "interiores":
        pairs.append(('href="https://boceto-escuela-diseno.netlify.app/cursos/' + slug + '/semana-01/clase-1.html"', 'href="/cursos/' + slug + '/semana-01/clase-1.html"'))
    patch(f"cursos/{slug}.html", pairs)

patch("aprender/recorridos-y-pasos-libres.html", [
    ('<div style="display: flex; flex-direction: column; gap: 10px; font-size: 15px; line-height: 1.55">',
     '<div id="chat" style="display: flex; flex-direction: column; gap: 10px; font-size: 15px; line-height: 1.55">'),
])

patch("aprender/devolucion-diagrama-de-zonas.html", [
    ('<button type="button" style="font-size: 16px; font-weight: 600; padding: 14px 24px; min-height: 52px; border-radius: 999px; border: none; background: #FFFFFF; color: #111111; cursor: pointer">Subir versión corregida</button>',
     '<a href="/bocetador/?carrera=interiores" style="text-decoration: none; font-size: 16px; font-weight: 600; padding: 14px 24px; min-height: 52px; box-sizing: border-box; display: inline-flex; align-items: center; border-radius: 999px; background: #FFFFFF; color: #111111">Subir versión corregida</a>'),
    ('href="/panel.html" style="text-decoration: none; font-size: 16px; font-weight: 600; padding: 14px 24px; min-height: 52px; box-sizing: border-box; display: inline-flex; align-items: center; border-radius: 999px; border: 1.5px solid #FFFFFF; color: #FFFFFF">Agendar en Google Calendar',
     'href="/panel.html#semana" style="text-decoration: none; font-size: 16px; font-weight: 600; padding: 14px 24px; min-height: 52px; box-sizing: border-box; display: inline-flex; align-items: center; border-radius: 999px; border: 1.5px solid #FFFFFF; color: #FFFFFF">Agendar en Google Calendar'),
    ('Corregí los puntos 2 y 3 y volvé a subir tu planta. El asistente compara las dos versiones y te dice si quedó resuelto.',
     'Corregí los puntos 2 y 3 en papel o en el Bocetador, subí la foto y pedile la corrección al asistente.'),
])

patch("panel.html", [
    ('<a href="#semana" style="text-decoration: none; padding: 12px; min-height: 44px; box-sizing: border-box; display: flex; align-items: center; border-radius: 12px">Mi semana</a>',
     '<a href="#semana" style="text-decoration: none; padding: 12px; min-height: 44px; box-sizing: border-box; display: flex; align-items: center; border-radius: 12px">Mi semana</a>\n<a href="/bocetador/" style="text-decoration: none; padding: 12px; min-height: 44px; box-sizing: border-box; display: flex; align-items: center; border-radius: 12px">Bocetador</a>'),
    ('Conectar Google Calendar</button>', 'Agregar a Google Calendar</button>'),
    ('Sincronizado con Google Calendar</span>', 'Elegí qué agregar a tu calendario</span>'),
    ('text-decoration: underline; cursor: pointer">Desconectar</button>', 'text-decoration: underline; cursor: pointer">Ocultar</button>'),
    ('Al conectar tu cuenta, cada sesión y cada fecha de entrega se agregan a tu Google Calendar con un recordatorio y el enlace directo a la lección.',
     'Cada sesión y la fecha de entrega se pueden agregar a tu Google Calendar, con el enlace directo a la lección.'),
    ('<p style="margin: 0; font-size: 14px; line-height: 1.5; color: #1E3A8A">Las 5 actividades de esta semana ya están en tu calendario. Si movés una sesión allá, el plan se actualiza acá.</p>',
     '<div id="calLinks" style="display: flex; flex-wrap: wrap; gap: 8px"></div>'),
    ('<a href="#portfolio" style="font-size: 15px; font-weight: 600; min-height: 44px; display: inline-flex; align-items: center">Descargar en PDF</a>',
     '<a href="/bocetador/" style="font-size: 15px; font-weight: 600; min-height: 44px; display: inline-flex; align-items: center">Abrir el Bocetador</a>'),
    ('<form style="display: flex; gap: 10px" data-chat="form">',
     '<div id="chat" style="display: flex; flex-direction: column; gap: 10px; font-size: 15px; line-height: 1.55"></div>\n<form style="display: flex; gap: 10px" data-chat="form">'),
    ('El asistente armó este plan según tus horarios libres y tus entregas pendientes. Podés moverlo cuando quieras.',
     'Un plan sugerido según tus entregas pendientes. Agregá a tu calendario las sesiones que quieras.'),
])

# Clases para el encabezado adaptable (celular y tableta)
import re as _re
for rel in ["index.html", "cursos/interiores.html", "cursos/industrial.html", "cursos/grafico.html", "cursos/indumentaria.html"]:
    p = PUB / rel; s = p.read_text(encoding="utf-8")
    s, n = _re.subn(r'<header style="max-width: 1240px', '<header class="site-header" style="max-width: 1240px', s, count=1)
    if n != 1: raise SystemExit(f"{rel}: sin encabezado")
    p.write_text(s, encoding="utf-8")
for rel in ["aprender/recorridos-y-pasos-libres.html", "aprender/devolucion-diagrama-de-zonas.html"]:
    p = PUB / rel; s = p.read_text(encoding="utf-8")
    s, n = _re.subn(r'<header style="border-bottom: 1px solid #E2E2E2', '<header class="app-header" style="border-bottom: 1px solid #E2E2E2', s, count=1)
    if n != 1: raise SystemExit(f"{rel}: sin encabezado")
    p.write_text(s, encoding="utf-8")
print("ok encabezados")
