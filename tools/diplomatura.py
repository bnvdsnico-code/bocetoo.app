"""Cambia "curso" por "diplomatura" en los textos visibles (con el género correcto).

No toca rutas (/cursos/…), identificadores, clases ni datos internos.
Uso: python3 tools/diplomatura.py archivo1 archivo2 …   (md, json, html, dc.html, mts)
"""
import re, sys, pathlib

# (patrón, reemplazo) en orden; se respetan mayúsculas iniciales.
REGLAS = [
    (r"\btodo el curso\b", "toda la diplomatura"),
    (r"\btodos los cursos\b", "todas las diplomaturas"),
    (r"\btodos tus cursos\b", "todas tus diplomaturas"),
    (r"\botros cursos\b", "otras diplomaturas"),
    (r"\blos cursos nuevos\b", "las diplomaturas nuevas"),
    (r"\bcursos nuevos\b", "diplomaturas nuevas"),
    (r"\bcada curso\b", "cada diplomatura"),
    (r"\bpor curso\b", "por diplomatura"),
    (r"\bdel curso\b", "de la diplomatura"),
    (r"\bal curso\b", "a la diplomatura"),
    (r"\bel curso\b", "la diplomatura"),
    (r"\beste curso\b", "esta diplomatura"),
    (r"\bese curso\b", "esa diplomatura"),
    (r"\bun curso\b", "una diplomatura"),
    (r"\bprimer curso\b", "primera diplomatura"),
    (r"\bnuevo curso\b", "nueva diplomatura"),
    (r"\blos cursos\b", "las diplomaturas"),
    (r"\blas cursos\b", "las diplomaturas"),
    (r"\bunos cursos\b", "unas diplomaturas"),
    (r"\b(tu|mi|su)s cursos\b", r"\1s diplomaturas"),
    (r"\b(tu|mi|su) curso\b", r"\1 diplomatura"),
    (r"\bcursos\b", "diplomaturas"),
    (r"\bcurso\b", "diplomatura"),
]
EXCEPCIONES = [r"\ben cursos\b", r"\ben curso\b", r"`[^`]*`", r"[\w./#:-]*/cursos?\b[\w./#?=-]*", r"\bcursos?/[\w./#?=-]*", r"\bcurso\.css\b"]  # "talleres que dan cursos", "en curso" = en marcha

def _caso(m, rep):
    s = m.expand(rep)
    return s[0].upper() + s[1:] if m.group(0)[0].isupper() else s

AJUSTES = [  # concordancias que las reglas no resuelven solas
    ("Diplomaturas destacados", "Diplomaturas destacadas"),
    ("Diplomaturas prácticos", "Diplomaturas prácticas"),
    ("la diplomatura queda tuyo", "la diplomatura queda tuya"),
    ("está armado la diplomatura", "está armada la diplomatura"),
    ("Acceso a las cuatro carreras y a las diplomaturas nuevas", "Acceso a las cuatro diplomaturas y a las nuevas que se sumen"),
]

def texto(s):
    guard = {}
    def prot(m):
        k = f"\x00{len(guard)}\x00"; guard[k] = m.group(0); return k
    for e in EXCEPCIONES:
        s = re.sub(e, prot, s, flags=re.I)
    for pat, rep in REGLAS:
        s = re.sub(pat, lambda m, rep=rep: _caso(m, rep), s, flags=re.I)
    for k, v in guard.items():
        s = s.replace(k, v)
    for a, b in AJUSTES:
        s = s.replace(a, b)
    return s

ATTRS = ("content", "alt", "aria-label", "placeholder", "title")

def html(s):
    # texto entre etiquetas, fuera de <script>/<style>
    partes = re.split(r"(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)", s, flags=re.S | re.I)
    out = []
    for p in partes:
        if not p:
            continue
        if p.startswith("<"):
            if not re.match(r"<(script|style)\b", p, re.I):
                p = re.sub(r'\b(%s)="([^"]*)"' % "|".join(ATTRS),
                           lambda m: f'{m.group(1)}="{texto(m.group(2))}"', p)
            out.append(p)
        else:
            out.append(texto(p))
    return "".join(out)

if __name__ == "__main__":
    for f in sys.argv[1:]:
        p = pathlib.Path(f); s = p.read_text(encoding="utf-8")
        n = html(s) if p.suffix == ".html" else texto(s)
        if n != s:
            p.write_text(n, encoding="utf-8"); print("ok", p)
