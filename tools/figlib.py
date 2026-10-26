"""Pequeña librería para dibujar esquemas SVG coherentes en las clases.

Cada función devuelve (svg, alt). El generador del curso los envuelve en <figure> con su epígrafe.
Todo se dibuja en un lienzo de 640 px de ancho, con la paleta de la carrera.
"""
import html, math

PALETAS = {
    "interiores":   {"acc": "#C2410C", "dark": "#7C2D12", "tint": "#FBE7DC", "soft": "#FDBA8C", "ink": "#3A2A22"},
    "industrial":   {"acc": "#1D4ED8", "dark": "#1E3A8A", "tint": "#E7F0FF", "soft": "#7EA2FF", "ink": "#1F2A44"},
    "grafico":      {"acc": "#6D28D9", "dark": "#4C1D95", "tint": "#EAE0FB", "soft": "#B392FF", "ink": "#2E2444"},
    "indumentaria": {"acc": "#BE185D", "dark": "#831843", "tint": "#FCE7F3", "soft": "#F27BB0", "ink": "#3F1F2E"},
}
P = dict(PALETAS["interiores"])
FONT = "Inter, system-ui, sans-serif"

def usar(curso):
    P.clear(); P.update(PALETAS[curso])

e = lambda s: html.escape(str(s), quote=True)

def wrap(s, n):
    words, lines, cur = str(s).split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return lines or [""]

def text(x, y, s, size=14, weight=600, fill=None, anchor="middle", n=None, lh=None):
    fill = fill or P["dark"]
    lines = wrap(s, n) if n else [str(s)]
    lh = lh or round(size * 1.3)
    y0 = y - (len(lines) - 1) * lh / 2
    t = "".join(f'<tspan x="{x}" y="{y0 + i * lh:.1f}">{e(l)}</tspan>' for i, l in enumerate(lines))
    return f'<text font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{t}</text>'

def svg(h, body, alt, w=640):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{e(alt)}">{body}</svg>'

def arrow(x1, y1, x2, y2, color=None, w=2):
    color = color or P["dark"]
    ang = math.atan2(y2 - y1, x2 - x1)
    a1 = (x2 - 9 * math.cos(ang - 0.45), y2 - 9 * math.sin(ang - 0.45))
    a2 = (x2 - 9 * math.cos(ang + 0.45), y2 - 9 * math.sin(ang + 0.45))
    return (f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="{color}" stroke-width="{w}" fill="none"/>'
            f'<path d="M{x2:.1f} {y2:.1f}L{a1[0]:.1f} {a1[1]:.1f}L{a2[0]:.1f} {a2[1]:.1f}Z" fill="{color}"/>')

# ---------- Plantillas ----------

def flujo(pasos, alt=None, destacar=None):
    """Pasos en fila (hasta 5) o en dos filas, con flechas."""
    n = len(pasos)
    nf = 1 if n <= 5 else 2 if n <= 10 else 3; k_ = math.ceil(n / nf)
    filas = [pasos[i:i + k_] for i in range(0, n, k_)]
    body, y, k = [], 20, 0
    for fila in filas:
        m = len(fila); gap = 26; w = (600 - gap * (m - 1)) / m; x = 20; nch = max(8, int(w / 7.6))
        lw = max(len(wd) for p in fila for wd in p.split()); fs = 13 if lw * 7.8 <= w - 10 else 11.5 if lw * 6.9 <= w - 8 else 10.5
        ml = max(len(wrap(p, nch)) for p in fila); h = 44 + 17 * ml
        for i, p in enumerate(fila):
            dest = destacar is not None and k == destacar
            body.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="16" fill="{P["acc"] if dest else P["tint"]}" stroke="{P["acc"]}" stroke-width="2"/>')
            body.append(text(x + w / 2, y + 22, f"{k + 1}", 12, 700, "#FFFFFF" if dest else P["acc"]))
            body.append(text(x + w / 2, y + 30 + (h - 30) / 2 + 4, p, fs, 600, "#FFFFFF" if dest else P["dark"], n=nch, lh=17))
            if i < m - 1: body.append(arrow(x + w + 3, y + h / 2, x + w + gap - 3, y + h / 2))
            x += w + gap; k += 1
        y += h + 26
    return svg(y - 10, "".join(body), alt or "Secuencia: " + ", ".join(pasos))

def tarjetas(items, cols=None, alt=None):
    """Tarjetas con título y texto breve. items = [(titulo, texto)]."""
    n = len(items); cols = cols or (3 if n in (3, 5, 6, 9) else 2 if n <= 4 else 4)
    rows = math.ceil(n / cols); gap = 14; w = (600 - gap * (cols - 1)) / cols
    tn = int((w - 26) / 8.4); largo = any(len(t) > tn for t, _ in items); h = 112 if largo else 96
    body = []
    for i, (t, d) in enumerate(items):
        r, c = divmod(i, cols); x = 20 + c * (w + gap); y = 16 + r * (h + gap)
        body.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="14" fill="#FFFFFF" stroke="{P["soft"]}" stroke-width="1.5"/>')
        body.append(f'<rect x="{x:.1f}" y="{y}" width="6" height="{h}" rx="3" fill="{P["acc"]}"/>')
        tl = wrap(t, tn) if len(t) > tn else [t]
        for k, l in enumerate(tl): body.append(text(x + 18, y + 26 + k * 18, l, 14, 700, P["dark"], "start"))
        dy = 18 * (len(tl) - 1)
        nl = len(wrap(d, max(14, int((w - 26) / 6.6))))
        body.append(text(x + 18, y + 50 + dy + (nl - 1) * 8, d, 12.5, 400, P["ink"], "start", n=max(14, int((w - 26) / 6.6)), lh=16))
    return svg(16 + rows * (h + gap) + 4, "".join(body), alt or "; ".join(f"{t}: {d}" for t, d in items))

def comparar(a, b, alt=None):
    """Dos columnas: a = (titulo, [puntos]), b = (titulo, [puntos])."""
    body = []
    for k, (t, pts) in enumerate((a, b)):
        x = 20 + k * 310
        body.append(f'<rect x="{x}" y="14" width="290" height="44" rx="12" fill="{P["acc"] if k == 0 else P["dark"]}"/>')
        body.append(text(x + 145, 42, t, 15, 700, "#FFFFFF"))
        y = 80
        for p in pts:
            lines = wrap(p, 36)
            body.append(f'<circle cx="{x + 14}" cy="{y - 4}" r="4" fill="{P["acc"]}"/>')
            body.append(text(x + 28, y + (len(lines) - 1) * 9, p, 13, 400, P["ink"], "start", n=36, lh=18))
            y += 18 * len(lines) + 12
        body.append(f'<rect x="{x}" y="64" width="290" height="{y - 64}" rx="12" fill="none" stroke="{P["soft"]}" stroke-width="1.2"/>')
    hmax = max(80 + sum(18 * len(wrap(p, 36)) + 12 for p in pts) for _, pts in (a, b))
    body2 = [s.replace(f'height="{0}"', '') for s in body]
    return svg(hmax + 10, "".join(body2), alt or f"Comparación entre {a[0]} y {b[0]}")

def barras(items, unidad="", alt=None, maxv=None):
    """Barras horizontales: items = [(etiqueta, valor)]."""
    maxv = maxv or max(v for _, v in items); body = []; y = 20
    for lab, v in items:
        w = 340 * v / maxv
        body.append(text(190, y + 19, lab, 13, 600, P["dark"], "end", n=26, lh=15))
        body.append(f'<rect x="200" y="{y + 4}" width="{w:.1f}" height="24" rx="6" fill="{P["acc"]}"/>')
        val = f"$ {v:,.0f}".replace(",", ".") if unidad == "$" else f"{v:g} {unidad}".strip()
        body.append(text(208 + w, y + 21, val, 13, 700, P["dark"], "start"))
        y += 40
    return svg(y + 6, "".join(body), alt or "; ".join(f"{l}: {v} {unidad}" for l, v in items))

def escala(izq, der, marcas, alt=None, titulo=None):
    """Un eje entre dos extremos con marcas: marcas = [(posicion 0..1, etiqueta)]."""
    body = []; y = 104 if titulo else 66
    if titulo: body.append(text(320, 28, titulo, 14, 700))
    body.append(f'<rect x="60" y="{y - 6}" width="520" height="12" rx="6" fill="{P["tint"]}" stroke="{P["soft"]}"/>')
    body.append(text(60, y + 34, izq, 13, 700, P["dark"], "start"))
    body.append(text(580, y + 34, der, 13, 700, P["dark"], "end"))
    for i, (pos, lab) in enumerate(marcas):
        x = 60 + 520 * pos; yy = y - 24 if i % 2 == 0 else y + 64
        body.append(f'<circle cx="{x:.1f}" cy="{y}" r="9" fill="{P["acc"]}" stroke="#FFFFFF" stroke-width="2"/>')
        body.append(text(x, yy, lab, 12.5, 600, P["ink"], n=20, lh=15))
    return svg(y + 96, "".join(body), alt or f"Escala de {izq} a {der}: " + ", ".join(l for _, l in marcas))

def ciclo(items, centro=None, alt=None):
    n = len(items); cx, cy, rx, ry = 320, 150, 220, 110; body = []
    body.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{P["soft"]}" stroke-width="2" stroke-dasharray="6 6"/>')
    if centro: body.append(text(cx, cy + 5, centro, 15, 700, P["acc"], n=14))
    for i, it in enumerate(items):
        a = -math.pi / 2 + 2 * math.pi * i / n; x = cx + rx * math.cos(a); y = cy + ry * math.sin(a)
        body.append(f'<rect x="{x - 70:.1f}" y="{y - 22:.1f}" width="140" height="44" rx="22" fill="{P["tint"]}" stroke="{P["acc"]}" stroke-width="2"/>')
        body.append(text(x, y + 5, it, 12.5, 700, P["dark"], n=18, lh=14))
    return svg(300, "".join(body), alt or "Ciclo: " + ", ".join(items))

def matriz(filas, cols, celdas, alt=None, leyenda=("Flojo", "Parcial", "Logrado")):
    """Tabla visual con celdas coloreadas: celdas[i][j] en 0..2 (nada, parcial, sí) o texto corto."""
    cw = (600 - 150) / len(cols); body = []
    for j, c in enumerate(cols):
        body.append(text(170 + cw * j + cw / 2, 30, c, 12.5, 700, P["dark"], n=12, lh=14))
    for i, f in enumerate(filas):
        y = 52 + i * 40
        body.append(text(160, y + 24, f, 13, 600, P["dark"], "end", n=22, lh=14))
        for j, v in enumerate(celdas[i]):
            x = 170 + cw * j
            if isinstance(v, (int, float)):
                fill = ["#FFFFFF", P["soft"], P["acc"]][int(v)]
                body.append(f'<rect x="{x + 4:.1f}" y="{y + 4}" width="{cw - 8:.1f}" height="32" rx="8" fill="{fill}" stroke="{P["soft"]}"/>')
            else:
                body.append(f'<rect x="{x + 4:.1f}" y="{y + 4}" width="{cw - 8:.1f}" height="32" rx="8" fill="#FFFFFF" stroke="{P["soft"]}"/>')
                body.append(text(x + cw / 2, y + 25, v, 12, 600, P["ink"]))
    h = 52 + len(filas) * 40 + 12
    if leyenda and any(isinstance(v, (int, float)) for f in celdas for v in f):
        x = 170
        for i, lab in enumerate(leyenda):
            body.append(f'<rect x="{x}" y="{h}" width="22" height="16" rx="4" fill="{["#FFFFFF", P["soft"], P["acc"]][i]}" stroke="{P["soft"]}"/>')
            body.append(text(x + 30, h + 13, lab, 12, 600, P["ink"], "start")); x += 40 + 8 * len(lab)
        h += 30
    return svg(h, "".join(body), alt or "Matriz de " + ", ".join(filas) + " por " + ", ".join(cols))

def lista_check(si, no, alt=None, tsi="Sí", tno="No"):
    """Dos listas: lo que conviene (tilde) y lo que no (cruz)."""
    body = []; h = 0
    for k, (tit, pts, mark) in enumerate(((tsi, si, "ok"), (tno, no, "no"))):
        x = 20 + k * 310; y = 24
        body.append(text(x + 6, y + 6, tit, 15, 700, P["acc"] if mark == "ok" else "#7A2E2E", "start"))
        y += 34
        for p in pts:
            lines = wrap(p, 34)
            if mark == "ok":
                body.append(f'<circle cx="{x + 14}" cy="{y - 5}" r="11" fill="{P["acc"]}"/><path d="M{x + 8} {y - 5}l4 4 7-8" stroke="#FFF" stroke-width="2.4" fill="none"/>')
            else:
                body.append(f'<circle cx="{x + 14}" cy="{y - 5}" r="11" fill="#E9D5D5"/><path d="M{x + 9} {y - 10}l10 10M{x + 19} {y - 10}l-10 10" stroke="#7A2E2E" stroke-width="2.2"/>')
            body.append(text(x + 34, y + (len(lines) - 1) * 9, p, 13, 400, P["ink"], "start", n=34, lh=18))
            y += 18 * len(lines) + 14
        h = max(h, y)
    return svg(h + 4, "".join(body), alt or f"{tsi}: " + "; ".join(si) + f". {tno}: " + "; ".join(no))

def piramide(niveles, alt=None):
    """Niveles de arriba (más chico) hacia abajo."""
    n = len(niveles); body = []; h = 50
    for i, t in enumerate(niveles):
        w = 200 + 380 * (i + 1) / n; x = 320 - w / 2; y = 16 + i * (h + 6)
        fill = [P["acc"], P["soft"], P["tint"], "#FFFFFF"][min(i, 3)]
        body.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="10" fill="{fill}" stroke="{P["acc"]}" stroke-width="1.5"/>')
        body.append(text(320, y + 31, t, 14, 700, "#FFFFFF" if i == 0 else P["dark"], n=int(w / 8)))
    return svg(16 + n * (h + 6) + 10, "".join(body), alt or "Niveles: " + ", ".join(niveles))

def linea_tiempo(hitos, alt=None):
    """hitos = [(etiqueta superior, texto)]."""
    n = len(hitos); body = [f'<path d="M30 90H610" stroke="{P["soft"]}" stroke-width="4"/>']
    for i, (a, b) in enumerate(hitos):
        x = 30 + 580 * (i + 0.5) / n
        body.append(f'<circle cx="{x:.1f}" cy="90" r="10" fill="{P["acc"]}" stroke="#FFF" stroke-width="3"/>')
        body.append(text(x, 58, a, 13, 700, P["acc"], n=14, lh=14))
        body.append(text(x, 128, b, 12, 400, P["ink"], n=max(12, int(560 / n / 6.5)), lh=15))
    return svg(176, "".join(body), alt or "Línea de tiempo: " + ", ".join(f"{a} {b}" for a, b in hitos))

def raw(h, body, alt):
    return svg(h, body, alt)
