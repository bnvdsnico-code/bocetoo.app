"""Reemplaza el recuadro "[Imagen de un proyecto de alumno]" del proyecto final de cada ficha por un ícono de la disciplina.

Uso: python3 tools/iconos.py public/cursos  (o la carpeta del lienzo con las Ficha-*.dc.html)
"""
import pathlib, re, sys

BASE = 'fill="none" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"'

ICONOS = {
    # sillón con lámpara de pie
    "interiores": ("Ícono de un sillón con una lámpara de pie",
        '<path d="M44 92V70q0-10 10-10h52q10 0 10 10v22"/>'
        '<path d="M34 92q0-10 10-10t10 10v14H106V92q0-10 10-10t10 10v20H34z"/>'
        '<path d="M44 112v8M116 112v8"/>'
        '<path d="M150 120V54M140 120h20M138 54h24l-6-20h-12z"/>'),
    # lámpara de escritorio articulada
    "industrial": ("Ícono de una lámpara de escritorio articulada",
        '<path d="M70 120h60"/><path d="M100 120V112"/>'
        '<circle cx="100" cy="108" r="4"/>'
        '<path d="M100 108L76 72"/><circle cx="76" cy="70" r="4"/>'
        '<path d="M76 70L112 44"/>'
        '<path d="M104 34l26 18-10 14-26-18z"/><path d="M118 70q8 6 2 14"/>'),
    # pluma vectorial con curva y nodos
    "grafico": ("Ícono de una pluma vectorial dibujando una curva con nodos",
        '<path d="M34 112C60 60 92 132 116 98"/>'
        '<rect x="28" y="106" width="12" height="12" rx="2"/>'
        '<path d="M34 112L70 72"/><circle cx="70" cy="72" r="4"/>'
        '<g transform="translate(118 96) rotate(40)"><path d="M0 0L-15 -32L-11 -50H11L15 -32Z"/><path d="M0 0V-26"/>'
        '<circle cx="0" cy="-30" r="3.5"/><path d="M-11 -50V-60H11V-50"/></g>'),
    # vestido en una percha
    "indumentaria": ("Ícono de un vestido colgado en una percha",
        '<path d="M100 26q0-8 7-8t6 8q-1 6-13 12"/>'
        '<path d="M60 52l40-14 40 14"/>'
        '<path d="M86 44q14 10 28 0"/>'
        '<path d="M86 44l-6 26 6 6-22 50h72l-22-50 6-6-6-26"/>'
        '<path d="M80 76h40"/>'),
}

PAT = re.compile(r'<div style="flex: 1 1 260px; min-width: 0; aspect-ratio: 4 / 3; border-radius: 20px; background: (#[0-9A-Fa-f]{6}); display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600">\[Imagen de un proyecto de alumno\]</div>')

def nuevo(curso, bg):
    alt, dibujo = ICONOS[curso]
    return (f'<div style="flex: 1 1 260px; min-width: 0; aspect-ratio: 4 / 3; border-radius: 20px; background: {bg}; display: flex; align-items: center; justify-content: center">'
            f'<svg role="img" aria-label="{alt}" viewBox="0 0 200 150" width="58%" {BASE}>{dibujo}</svg></div>')

carpeta = pathlib.Path(sys.argv[1])
for curso in ICONOS:
    for nombre in (f"{curso}.html", f"Ficha-{curso.capitalize()}.dc.html", "Ficha-Grafico.dc.html" if curso == "grafico" else None):
        if not nombre: continue
        p = carpeta / nombre
        if not p.exists(): continue
        s = p.read_text(encoding="utf-8")
        s, n = PAT.subn(lambda m: nuevo(curso, m.group(1)), s)
        print(p.name, "ok" if n else "ya estaba o no se encontró")
        if n: p.write_text(s, encoding="utf-8")
