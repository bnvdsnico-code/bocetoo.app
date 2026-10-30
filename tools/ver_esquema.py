"""Esquema breve de una semana: objetivo, subtítulos de la lectura y primeras líneas de la práctica."""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import aplicar_clases as a
curso = sys.argv[1]
for n in map(int, sys.argv[2:]):
    _, cl = a.partir((a.ROOT / "content" / curso / f"s{n:02d}.md").read_text(encoding="utf-8"))
    print(f"######## s{n:02d}")
    for d, c in cl.items():
        lec = c["s"].get("lectura", "")
        tit = [l[3:] for l in lec.splitlines() if l.startswith("## ")]
        datos = re.findall(r"\*\*([^*]{3,60})\*\*", lec)[:10]
        print(f"[d{d}] {c['pre'].splitlines()[0][10:]}\n   secciones: {' | '.join(tit)}\n   claves: {', '.join(datos)}\n   práctica: {c['s'].get('práctica','').strip().splitlines()[0][:140]}")
