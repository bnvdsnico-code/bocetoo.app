"""Muestra objetivo y lectura de cada clase de una semana (figuras abreviadas), para revisarlas."""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import aplicar_clases as a
curso, n = sys.argv[1], int(sys.argv[2])
_, cl = a.partir((a.ROOT / "content" / curso / f"s{n:02d}.md").read_text(encoding="utf-8"))
for d, c in cl.items():
    lec = c["s"].get("lectura", "")
    k = [0]
    def f(m):
        k[0] += 1
        cap = re.search(r"<figcaption>(.*?)</figcaption>", m.group(0), re.S)
        return f"[FIG{k[0]}: {cap.group(1).strip() if cap else ''}]"
    lec = re.sub(r"<figure>.*?</figure>", f, lec, flags=re.S)
    print(f"===== CLASE {d}\n{c['pre']}\n{lec}\n----- práctica (resumen): {c['s'].get('práctica','')[:300]}\n")
