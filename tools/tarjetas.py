"""Coloca las fotos de las tarjetas "Diplomaturas destacadas" de la portada (public/index.html).

Cada foto lleva su crédito. Se puede volver a correr: solo reemplaza los recuadros que siguen vacíos.
"""
import pathlib, re, sys

PUB = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "public"

# diplomatura: (texto alternativo, crédito)
TARJETAS = {
    "interiores": ("Revista de diseño abierta y una taza sobre una mesa de cajón de madera, frente a un sillón claro con almohadones azules",
                   "Karolina Grabowska"),
    "industrial": ("Pantalla de computadora con un modelo 3D de muebles de madera, mesas de luz y un rack con patas, en un programa de modelado",
                   "cottonbro studio"),
    "grafico": ("Manos que eligen muestras de color impresas sobre una mesa blanca: tarjetas verde, terracota, violeta y beige",
                "Noemi Jimenez"),
    "indumentaria": ("Figurines dibujados a lápiz y coloreados en azul, junto a una cinta métrica, un alfiletero, una tijera y una caja de botones rojos",
                     "Jane Blaze"),
}

p = PUB / "index.html"
s = p.read_text(encoding="utf-8")
for curso, (alt, credito) in TARJETAS.items():
    # el recuadro vacío que precede al enlace de esa diplomatura
    pat = re.compile(r'<div style="aspect-ratio: 4 / 3;[^"]*">\[Foto o render de la diplomatura\]</div>(?=\s*<span[^>]*>[^<]*</span>\s*<h3[^>]*><a href="/cursos/%s\.html")' % curso)
    nuevo = (
        '<figure style="margin: 0; display: flex; flex-direction: column; gap: 6px">'
        f'<img src="assets/fotos/card-{curso}.webp" srcset="assets/fotos/card-{curso}-640.webp 640w, assets/fotos/card-{curso}.webp 1200w" '
        'sizes="(max-width: 700px) 100vw, 300px" width="1200" height="900" loading="lazy" '
        f'alt="{alt}" style="display: block; width: 100%; aspect-ratio: 4 / 3; height: auto; object-fit: cover; border-radius: 20px">'
        f'<figcaption style="font-size: 12px; color: #6B6B6B">Foto: {credito}</figcaption></figure>'
    )
    s, n = pat.subn(nuevo, s)
    print(curso, "ok" if n else "ya estaba o no se encontró")
p.write_text(s, encoding="utf-8")
