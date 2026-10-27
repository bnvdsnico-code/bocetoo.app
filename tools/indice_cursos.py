"""Genera public/assets/cursos.json: título de cada diplomatura y de cada semana (lo usa el panel)."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
out = {}
for c in ["interiores", "industrial", "grafico", "indumentaria"]:
    T = json.loads((ROOT / "content" / c / "temario.json").read_text(encoding="utf-8"))
    out[c] = {"titulo": T["titulo"], "semanas": {str(s["n"]): s["titulo"] for u in T["unidades"] for s in u["semanas"]}}
(ROOT / "public" / "assets" / "cursos.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("ok", {c: len(v["semanas"]) for c, v in out.items()})
