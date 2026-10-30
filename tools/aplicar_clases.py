"""Aplica una revisión de clases sobre content/<curso>/sNN.md.

La revisión (content/<curso>/revision/sNN.md) tiene, por clase:
## Clase N
### Intro / Cierre (opcional: texto que se agrega al principio o al final de la lectura)
### Lectura        (opcional: reemplaza la lectura; {{fig1}}, {{fig2}}… insertan las figuras de la versión anterior)
### Imagen         (![alt](/img/clases/<curso>/sNNdN.jpg "crédito") + lectura de la imagen)
### Autores
### Norma
### Referencias
Las secciones Práctica, Entrega y Repaso de la versión anterior se conservan.
Uso: python3 tools/aplicar_clases.py <curso> <semana>
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORDEN = ["lectura", "imagen", "autores", "práctica", "entrega", "repaso", "norma", "referencias"]
NOMBRE = {"lectura": "Lectura", "imagen": "Imagen", "autores": "Autores", "práctica": "Práctica", "entrega": "Entrega", "repaso": "Repaso", "norma": "Norma", "referencias": "Referencias"}

def partir(texto):
    cabeza, *resto = re.split(r"^## Clase (\d)\s*$", texto, flags=re.M)
    clases = {}
    for i in range(0, len(resto), 2):
        d, cuerpo = int(resto[i]), resto[i + 1]
        pre, *secs = re.split(r"^### (.+?)\s*$", cuerpo, flags=re.M)
        s = {secs[j].strip().lower(): secs[j + 1].strip("\n") for j in range(0, len(secs), 2)}
        clases[d] = {"pre": pre.strip("\n"), "s": s}
    return cabeza, clases

def aplicar(curso, n):
    base = ROOT / "content" / curso
    orig_f, rev_f = base / f"s{n:02d}.md", base / "revision" / f"s{n:02d}.md"
    cabeza, clases = partir(orig_f.read_text(encoding="utf-8"))
    _, revs = partir(rev_f.read_text(encoding="utf-8"))
    for d, rv in revs.items():
        if d not in clases: raise SystemExit(f"s{n:02d}: la clase {d} no existe")
        c = clases[d]
        if rv["pre"]: c["pre"] = rv["pre"]          # Objetivo / Tiempos nuevos
        extra = {k: rv["s"].pop(k) for k in ("intro", "cierre") if k in rv["s"]}
        for k, v in rv["s"].items():
            if k == "lectura":
                figs = re.findall(r"<figure>.*?</figure>", c["s"].get("lectura", ""), flags=re.S)
                def fig(m):
                    i = int(m.group(1)) - 1
                    if i >= len(figs): raise SystemExit(f"s{n:02d}d{d}: falta la figura {i + 1}")
                    return figs[i]
                v = re.sub(r"\{\{fig(\d+)\}\}", fig, v)
            c["s"][k] = v.strip("\n")
        if "intro" in extra: c["s"]["lectura"] = extra["intro"].strip("\n") + "\n\n" + c["s"]["lectura"]
        if "cierre" in extra: c["s"]["lectura"] = c["s"]["lectura"].rstrip("\n") + "\n\n" + extra["cierre"].strip("\n")
    out = [cabeza.rstrip("\n") + "\n"]
    for d in sorted(clases):
        c = clases[d]
        out.append(f"\n## Clase {d}\n{c['pre']}\n")
        for k in ORDEN + [k for k in c["s"] if k not in ORDEN]:
            if k in c["s"]:
                out.append(f"\n### {NOMBRE.get(k, k.capitalize())}\n{c['s'][k]}\n")
    orig_f.write_text("".join(out), encoding="utf-8")
    print(f"{curso} s{n:02d}: {len(revs)} clases revisadas")

if __name__ == "__main__":
    aplicar(sys.argv[1], int(sys.argv[2]))
