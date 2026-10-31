"""Genera la base de conocimiento del asistente a partir de las clases.

Salida:
  src/conocimiento.json   índice compacto de las 320 clases (lo importa el asistente)
  content/fuentes/referentes.md   referentes de la región por diplomatura (para consulta)
Uso: python3 tools/kb.py
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from aplicar_clases import partir  # noqa: E402

CURSOS = ["interiores", "industrial", "grafico", "indumentaria"]


def limpio(md: str) -> str:
    t = re.sub(r"<figure>.*?</figure>", " ", md, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"^\s*\|?\s*-{3,}.*$", " ", t, flags=re.M)
    t = re.sub(r"[*_`#>|]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def corto(t: str, n: int) -> str:
    if len(t) <= n:
        return t
    cut = t[:n]
    p = cut.rfind(". ")
    return (cut[: p + 1] if p > n * 0.5 else cut.rstrip() + "…")


def main():
    data = {"cursos": {}, "clases": []}
    refs_md = ["# Referentes de la región por diplomatura", "",
               "Generado con tools/kb.py a partir de la sección «Referentes de la región» de cada clase.", ""]
    for curso in CURSOS:
        T = json.loads((ROOT / "content" / curso / "temario.json").read_text(encoding="utf-8"))
        semanas = []
        nombres = {}
        for n in range(1, 17):
            f = ROOT / "content" / curso / f"s{n:02d}.md"
            cabeza, clases = partir(f.read_text(encoding="utf-8"))
            m = re.search(r"Semana \d+ · (.+)", cabeza)
            titulo = m.group(1).strip() if m else f"Semana {n}"
            semanas.append(titulo)
            for d in sorted(clases):
                c = clases[d]
                s = c["s"]
                obj = re.search(r"Objetivo:\s*(.+)", c["pre"])
                lect = s.get("lectura", "")
                temas = [h.strip() for h in re.findall(r"^## (.+)$", lect, flags=re.M)][:6]
                autores = limpio(s.get("autores", ""))
                for nom in re.findall(r"\*\*([^*]{3,60})\*\*", s.get("autores", "")):
                    if nom[0].isupper() and len(nom.split()) <= 6:
                        nombres.setdefault(nom, (n, d))
                data["clases"].append({
                    "c": curso, "s": n, "d": d,
                    "t": titulo,
                    "o": obj.group(1).strip() if obj else "",
                    "u": f"/cursos/{curso}/semana-{n:02d}/clase-{d}.html",
                    "h": temas,
                    "l": corto(limpio(lect), 900),
                    "a": corto(autores, 500),
                    "n": corto(limpio(s.get("norma", "")), 450),
                })
        data["cursos"][curso] = {"nombre": T["carrera"], "semanas": semanas}
        refs_md += [f"## {T['carrera']}", ""]
        refs_md += [f"- **{nom}** (semana {sn}, clase {cd})" for nom, (sn, cd) in sorted(nombres.items())]
        refs_md.append("")
    out = ROOT / "src" / "conocimiento.json"
    out.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (ROOT / "content" / "fuentes" / "referentes.md").write_text("\n".join(refs_md), encoding="utf-8")
    print(f"{len(data['clases'])} clases · {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
