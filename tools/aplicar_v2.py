"""Reemplaza Imagen y Autores de content/<curso>/sNN.md con content/<curso>/revision2/sNN.md.
En Referencias, quita las líneas de autores antiguos y antepone las nuevas."""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from aplicar_clases import partir, ORDEN, NOMBRE
ROOT = pathlib.Path(__file__).resolve().parent.parent
VIEJOS = re.compile(r"Vitruvio|Wharton|De Wolfe|Munsell|Litchfield|Storey|Edison|Robie|Schütte|Toof|Cooper Hewitt|Gutenberg|Wikimedia Commons\]\(https://commons.wikimedia.org/wiki/File:Frank")
def aplicar(curso, n):
    f = ROOT / "content" / curso / f"s{n:02d}.md"
    cabeza, clases = partir(f.read_text(encoding="utf-8"))
    _, revs = partir((ROOT / "content" / curso / "revision2" / f"s{n:02d}.md").read_text(encoding="utf-8"))
    for d, rv in revs.items():
        c = clases[d]["s"]
        for k in ("imagen", "autores"):
            if k in rv["s"]: c[k] = rv["s"][k].strip("\n")
        if "referencias" in rv["s"]:
            viejas = [l for l in c.get("referencias", "").split("\n") if l.strip() and not VIEJOS.search(l)]
            nuevas = [l for l in rv["s"]["referencias"].split("\n") if l.strip()]
            c["referencias"] = "\n".join(nuevas + viejas)
    out = [cabeza.rstrip("\n") + "\n"]
    for d in sorted(clases):
        c = clases[d]
        out.append(f"\n## Clase {d}\n{c['pre']}\n")
        for k in ORDEN + [k for k in c["s"] if k not in ORDEN]:
            if k in c["s"]: out.append(f"\n### {NOMBRE.get(k, k.capitalize())}\n{c['s'][k]}\n")
    f.write_text("".join(out), encoding="utf-8")
    print(f"{curso} s{n:02d}: v2 aplicada a {len(revs)} clases")
if __name__ == "__main__":
    for n in sys.argv[2:]: aplicar(sys.argv[1], int(n))
