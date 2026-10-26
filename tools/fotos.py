"""Coloca la foto de portada en la ficha de cada curso (reemplaza el dibujo del encabezado).

Se puede volver a correr después de convert.py: si la foto ya está, no hace nada.
"""
import pathlib, re, sys

PUB = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "public"

FOTOS = {
    "interiores": "Living luminoso con sillón gris, mesa ratona redonda, alfombra, plantas y dos lámparas colgantes de fibra natural",
    "industrial": "Una persona boceta en una tableta la perspectiva de un objeto, con trazos de construcción y una mancha de color amarilla",
    "grafico": "Círculo cromático abierto sobre un cuaderno, junto a un pincel y un lápiz",
    "indumentaria": "Una diseñadora con cinta métrica al cuello dibuja un figurín a lápiz sobre la mesa de trabajo",
}

FIG = re.compile(r'<figure style="flex: 1 1 420px;[^"]*">.*?</figure>', re.S)

for curso, alt in FOTOS.items():
    p = PUB / "cursos" / f"{curso}.html"
    s = p.read_text(encoding="utf-8")
    if "../assets/fotos/" in s:
        print("ya estaba", p); continue
    nuevo = (
        '<figure style="flex: 1 1 420px; min-width: 0; margin: 0; border-radius: 28px; overflow: hidden; aspect-ratio: 4 / 3; background: #FFFFFF">\n'
        f'<img src="../assets/fotos/{curso}.webp" srcset="../assets/fotos/{curso}-800.webp 800w, ../assets/fotos/{curso}.webp 1600w" '
        'sizes="(max-width: 900px) 100vw, 560px" width="1600" height="1200" fetchpriority="high" '
        f'alt="{alt}" style="display: block; width: 100%; height: 100%; object-fit: cover">\n'
        '</figure>'
    )
    s, n = FIG.subn(nuevo, s, count=1)
    if n != 1:
        raise SystemExit(f"{p}: no encontré el dibujo del encabezado")
    p.write_text(s, encoding="utf-8")
    print("ok", p)
