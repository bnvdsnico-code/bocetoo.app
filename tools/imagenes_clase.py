"""Descarga y prepara las imágenes comentadas de las clases.

Lee content/<curso>/imagenes.json: { "s01d1": {"url": "...", "credito": "..."} }
y guarda public/img/clases/<curso>/<id>.jpg (máximo 1100 px, JPEG).
Uso: python3 tools/imagenes_clase.py <curso> [--hoja salida.png ids...]
"""
import io, json, pathlib, sys, time, urllib.request
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent

def preparar(curso):
    mapa = json.loads((ROOT / "content" / curso / "imagenes.json").read_text(encoding="utf-8"))
    out = ROOT / "public" / "img" / "clases" / curso
    out.mkdir(parents=True, exist_ok=True)
    for cid, it in sorted(mapa.items()):
        dest = out / f"{cid}.jpg"
        if dest.exists(): continue
        req = urllib.request.Request(it["url"], headers={"User-Agent": "boceto-cursos/1.0 (https://bocetoo.app; hola@bocetoo.app) python-urllib"})
        datos = None
        for intento in range(4):
            try: datos = urllib.request.urlopen(req, timeout=60).read(); break
            except Exception as e:
                print("reintento", cid, e); time.sleep(10 * (intento + 1))
        if datos is None: print("FALLÓ", cid); continue
        im = Image.open(io.BytesIO(datos))
        if im.mode in ("P", "LA", "RGBA"):
            fondo = Image.new("RGB", im.size, "white"); im = im.convert("RGBA"); fondo.paste(im, mask=im.split()[-1]); im = fondo
        im = im.convert("RGB")
        im.thumbnail((1100, 1100))
        im.save(dest, "JPEG", quality=80, optimize=True, progressive=True)
        print("ok", cid, im.size, dest.stat().st_size // 1024, "KB")

def hoja(curso, salida, ids):
    """Une varias imágenes en una sola hoja para revisarlas juntas."""
    ims = []
    for cid in ids:
        f = ROOT / "public" / "img" / "clases" / curso / f"{cid}.jpg"
        im = Image.open(f); im.thumbnail((520, 520)); ims.append((cid, im))
    W = 540 * min(3, len(ims)); filas = (len(ims) + 2) // 3
    H = 560 * filas
    lienzo = Image.new("RGB", (W, H), "#888")
    d = ImageDraw.Draw(lienzo)
    for i, (cid, im) in enumerate(ims):
        x, y = (i % 3) * 540 + 10, (i // 3) * 560 + 28
        lienzo.paste(im, (x, y)); d.text((x, y - 20), cid, fill="white")
    lienzo.save(salida)

if __name__ == "__main__":
    if "--hoja" in sys.argv:
        i = sys.argv.index("--hoja"); hoja(sys.argv[1], sys.argv[i + 1], sys.argv[i + 2:])
    else:
        preparar(sys.argv[1])
