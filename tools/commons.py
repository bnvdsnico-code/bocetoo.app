"""Busca imágenes con licencia libre en Wikimedia Commons.
Uso: python3 tools/commons.py "consulta" [n]
Muestra título, licencia, autor y URL (miniatura de 1100 px) de cada resultado con licencia apta."""
import json, sys, urllib.parse, urllib.request, urllib.error, re, html
APTAS = re.compile(r"^(Public domain|PD|CC0|CC BY(-SA)? [0-9.]+)", re.I)
def buscar(q, n=8):
    p = {"action": "query", "generator": "search", "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": 25, "prop": "imageinfo",
         "iiprop": "url|extmetadata|size", "iiurlwidth": 1100, "format": "json"}
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"User-Agent": "boceto-cursos/1.0 (bocetoo.app; hola@bocetoo.app)"})
    import time
    for intento in range(5):
        try: d = json.load(urllib.request.urlopen(req, timeout=60)); break
        except urllib.error.HTTPError as e:
            if e.code != 429 or intento == 4: raise
            time.sleep(8 * (intento + 1))
    out = []
    for pg in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 0)):
        ii = (pg.get("imageinfo") or [{}])[0]; md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "")
        if not APTAS.search(lic) or not re.search(r"\.(jpe?g|png|tif)$", pg["title"], re.I): continue
        autor = re.sub("<[^>]+>", "", html.unescape(md.get("Artist", {}).get("value", "")))[:80].strip()
        desc = re.sub("<[^>]+>", "", html.unescape(md.get("ImageDescription", {}).get("value", "")))[:140].strip()
        out.append({"titulo": pg["title"], "licencia": lic, "autor": autor, "url": (ii.get("thumburl") or ii.get("url") or "").replace("https://thumb.wikimedia.org/", "https://upload.wikimedia.org/").split("?")[0], "pagina": ii.get("descriptionurl"), "desc": desc})
        if len(out) >= n: break
    return out
if __name__ == "__main__":
    for r in buscar(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 6):
        print(f"- {r['titulo']} | {r['licencia']} | {r['autor']}\n  {r['url']}\n  {r['pagina']}\n  {r['desc']}")
