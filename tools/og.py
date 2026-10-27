"""Genera las imágenes para compartir (Open Graph, 1200x630) en public/assets/og/.
Uso: python3 tools/og.py <carpeta de @fontsource>   (necesita bricolage-grotesque e inter instalados con npm)
"""
import sys, pathlib, base64
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
OUT = PUB / "assets" / "og"; OUT.mkdir(parents=True, exist_ok=True)
FS = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "node_modules/@fontsource")

def font(pkg, fname):
    return base64.b64encode((FS / pkg / "files" / fname).read_bytes()).decode()

def img(p):
    return "data:image/webp;base64," + base64.b64encode((PUB / "assets" / "fotos" / p).read_bytes()).decode()

CSS = f"""
@font-face {{ font-family: B; font-weight: 800; src: url(data:font/woff2;base64,{font('bricolage-grotesque', 'bricolage-grotesque-latin-800-normal.woff2')}) format('woff2'); }}
@font-face {{ font-family: I; font-weight: 500; src: url(data:font/woff2;base64,{font('inter', 'inter-latin-500-normal.woff2')}) format('woff2'); }}
@font-face {{ font-family: I; font-weight: 700; src: url(data:font/woff2;base64,{font('inter', 'inter-latin-700-normal.woff2')}) format('woff2'); }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 1200px; height: 630px; display: flex; background: #FFFFFF; font-family: I, sans-serif; color: #111111; overflow: hidden; }}
.txt {{ width: 640px; padding: 56px 56px 52px 72px; display: flex; flex-direction: column; position: relative; }}
.txt::before {{ content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 18px; background: var(--c); }}
.brand {{ font-family: B; font-size: 34px; letter-spacing: -0.02em; display: flex; align-items: center; gap: 12px; }}
.marks {{ display: grid; grid-template-columns: repeat(2, 14px); gap: 4px; }}
.marks i {{ width: 14px; height: 14px; border-radius: 3px; display: block; }}
.marks i:nth-child(1) {{ background: #C2410C; }} .marks i:nth-child(2) {{ background: #1D4ED8; border-radius: 50%; }}
.marks i:nth-child(3) {{ background: #6D28D9; border-radius: 50%; }} .marks i:nth-child(4) {{ background: #BE185D; }}
.kick {{ margin-top: auto; font-weight: 700; font-size: 20px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--c); }}
h1 {{ font-family: B; font-size: 66px; line-height: 0.98; letter-spacing: -0.035em; margin-top: 14px; }}
.sub {{ margin-top: 22px; font-size: 25px; font-weight: 500; color: #3A3A3A; line-height: 1.35; }}
.pill {{ margin-top: 28px; align-self: flex-start; background: #111111; color: #FFFFFF; font-weight: 700; font-size: 21px; padding: 12px 22px; border-radius: 999px; }}
.foto {{ flex: 1; background-size: cover; background-position: center; }}
.grid {{ flex: 1; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 6px; }}
.grid div {{ background-size: cover; background-position: center; }}
"""

PAGES = {
    "interiores": ("#C2410C", "Diplomatura online", "Diseño de Interiores y Mobiliario", "Del plano al proyecto, en 16 semanas.", "interiores-800.webp"),
    "industrial": ("#1D4ED8", "Diplomatura online", "Diseño Industrial", "Del boceto al prototipo, en 16 semanas.", "industrial-800.webp"),
    "grafico": ("#6D28D9", "Diplomatura online", "Diseño Gráfico", "De la idea a la identidad, en 16 semanas.", "grafico-800.webp"),
    "indumentaria": ("#BE185D", "Diplomatura online", "Diseño de Indumentaria", "Del figurín a la colección, en 16 semanas.", "indumentaria-800.webp"),
}

def html(c, kick, title, sub, right):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="--c:{c}">
<div class="txt"><span class="brand"><span class="marks"><i></i><i></i><i></i><i></i></span>boceto</span>
<span class="kick">{kick}</span><h1>{title}</h1><p class="sub">{sub}</p><span class="pill">Primera clase gratis · bocetoo.app</span></div>{right}</body></html>"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    p = b.new_page(viewport={"width": 1200, "height": 630})
    for slug, (c, kick, title, sub, foto) in PAGES.items():
        p.set_content(html(c, kick, title, sub, f'<div class="foto" style="background-image:url({img(foto)})"></div>'))
        p.wait_for_timeout(200)
        p.screenshot(path=str(OUT / f"{slug}.jpg"), type="jpeg", quality=86)
        print("ok", slug)
    grid = '<div class="grid">' + "".join(f'<div style="background-image:url({img(PAGES[k][4])})"></div>' for k in PAGES) + "</div>"
    p.set_content(html("#111111", "Escuela de diseño online", "Aprendé diseño haciendo", "Interiores, Industrial, Gráfico e Indumentaria. Con asistente de IA.", grid))
    p.wait_for_timeout(200)
    p.screenshot(path=str(OUT / "boceto.jpg"), type="jpeg", quality=86)
    print("ok boceto")
    b.close()
