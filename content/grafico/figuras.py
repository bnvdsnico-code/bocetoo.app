"""Gráficos adicionales del curso de Diseño Gráfico (uno por clase que no tenía)."""
import colorsys
from figlib import *

def _composiciones():
    b = []; labs = ["Orden", "Caos", "Crecimiento", "Tensión", "Calma", "Encuentro"]
    for i, lab in enumerate(labs):
        x = 20 + (i % 3) * 205; y = 14 + (i // 3) * 150
        b.append(f'<rect x="{x}" y="{y}" width="190" height="110" rx="12" fill="#FFFFFF" stroke="{P["soft"]}" stroke-width="1.5"/>')
        b.append(text(x + 95, y + 132, lab, 13, 700))
    k = f'fill="{P["dark"]}"'
    # orden
    b.append("".join(f'<rect x="{50 + c * 34}" y="{34 + r * 30}" width="20" height="20" {k}/>' for r in range(3) for c in range(4)))
    # caos
    for (x, y, r, w) in ((250, 40, 20, 18), (300, 70, -35, 26), (350, 36, 50, 14), (282, 100, 10, 12), (370, 92, -15, 22), (330, 48, 70, 10)):
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{w}" transform="rotate({r} {x + w / 2} {y + w / 2})" {k}/>')
    # crecimiento
    for i, r in enumerate((5, 9, 14, 20, 27)):
        b.append(f'<circle cx="{445 + i * 30 + r / 2:.0f}" cy="{106 - r}" r="{r}" {k}/>')
    # tensión
    b.append(f'<path d="M106 182L194 182L150 258Z" {k}/>')
    b.append(f'<path d="M60 260L200 260" stroke="{P["dark"]}" stroke-width="3"/>')
    # calma
    b.append(f'<rect x="250" y="226" width="130" height="10" rx="5" {k}/><rect x="270" y="246" width="90" height="6" rx="3" fill="{P["soft"]}"/>')
    # encuentro
    b.append(f'<circle cx="490" cy="220" r="22" {k}/><circle cx="532" cy="220" r="22" fill="{P["acc"]}" opacity=".85"/>')
    b.append(arrow(440, 220, 462, 220, P["soft"])); b.append(arrow(582, 220, 560, 220, P["soft"]))
    return raw(300, "".join(b), "Seis composiciones con formas simples: una grilla regular (orden), formas giradas al azar (caos), círculos que crecen, un triángulo apoyado en su punta (tensión), líneas horizontales (calma) y dos círculos que se tocan (encuentro)")

def _formatos():
    b = []; s = 0.62
    def r(x, y, w, h, lab, sub, fill, cy=None):
        b.append(f'<rect x="{x}" y="{y}" width="{w * s:.1f}" height="{h * s:.1f}" fill="{fill}" stroke="{P["acc"]}" stroke-width="2"/>')
        cx = x + w * s / 2 if cy is None else x + 315 * s; cy = y + h * s / 2 if cy is None else cy
        b.append(text(cx, cy - 4, lab, 16, 700)); b.append(text(cx, cy + 14, sub, 11.5, 500, P["ink"]))
    r(20, 14, 420, 297, "A5", "148 × 210 mm", "#FFFFFF", cy=14 + 222 * s)
    b.append(f'<path d="M20 {14 + 297 * s + 10:.0f}v8H{20 + 420 * s:.0f}v-8" fill="none" stroke="{P["dark"]}" stroke-width="1.5"/>')
    b.append(text(20 + 210 * s, 14 + 297 * s + 36, "Toda la hoja: A3, 297 × 420 mm", 13, 700))
    r(20, 14, 210, 297, "A4", "210 × 297 mm", P["tint"])
    r(20 + 210 * s, 14, 210, 148, "A5", "148 × 210 mm", P["soft"] + "66")
    b.append(text(470, 60, "Cada formato es la mitad", 13.5, 700, P["dark"], "start"))
    b.append(text(470, 80, "del anterior, con la", 13.5, 400, P["ink"], "start"))
    b.append(text(470, 100, "misma proporción 1 : 1,414", 13.5, 400, P["ink"], "start"))
    return raw(248, "".join(b), "Una hoja A3 dividida en dos A4, y un A4 dividido en dos A5: todos con la misma proporción")

def _jerarquia():
    b = [f'<rect x="200" y="14" width="200" height="270" rx="6" fill="#FFFFFF" stroke="{P["soft"]}" stroke-width="2"/>']
    b.append(f'<rect x="222" y="40" width="156" height="40" rx="4" fill="{P["dark"]}"/>')
    b.append(f'<rect x="222" y="94" width="110" height="14" rx="3" fill="{P["acc"]}"/>')
    b.append("".join(f'<rect x="222" y="{124 + i * 14}" width="{150 - (i % 2) * 30}" height="6" rx="3" fill="{P["soft"]}"/>' for i in range(6)))
    b.append(f'<rect x="222" y="236" width="70" height="22" rx="11" fill="{P["acc"]}"/>')
    for n, (y, lab) in enumerate(((60, "Qué: el título, grande"), (101, "Cuándo y dónde"), (150, "Detalles"), (247, "Llamado a la acción"))):
        b.append(f'<circle cx="430" cy="{y}" r="12" fill="{P["acc"]}"/>'); b.append(text(430, y + 4.5, n + 1, 12, 700, "#FFFFFF"))
        b.append(f'<path d="M384 {y}H416" stroke="{P["soft"]}" stroke-dasharray="3 3"/>')
        b.append(text(452, y + 5, lab, 13, 600, P["dark"], "start"))
    b.append(text(100, 140, "La mirada", 13, 700, P["dark"])); b.append(text(100, 158, "recorre en orden", 13, 400, P["ink"]))
    return raw(298, "".join(b), "Esquema de un afiche: título grande, luego fecha y lugar, luego detalles en texto chico y al final un botón; números del 1 al 4 marcan el orden de lectura")

def _familias():
    d = P["dark"]; b = []; labs = ["Con serif", "Sin serif", "Egipcia", "Manuscrita", "Display"]
    for i, lab in enumerate(labs):
        x = 20 + i * 122
        b.append(f'<rect x="{x}" y="14" width="110" height="120" rx="12" fill="{P["tint"]}"/>')
        b.append(text(x + 55, 158, lab, 13, 700))
    c = lambda i: 75 + i * 122
    # serif: asta con contraste y remates finos con transición
    x = c(0); b.append(f'<path d="M{x - 24} 34h48v4q-12 1-14 8v66q2 7 14 8v4h-48v-4q12-1 14-8v-66q-2-7-14-8z" fill="{d}"/>')
    # sin serif: asta pareja
    x = c(1); b.append(f'<rect x="{x - 10}" y="34" width="20" height="88" fill="{d}"/>')
    # egipcia: remates rectangulares gruesos
    x = c(2); b.append(f'<path d="M{x - 26} 34h52v12h-16v64h16v12h-52v-12h16v-64h-16z" fill="{d}"/>')
    # manuscrita: trazo continuo de pluma
    x = c(3); b.append(f'<path d="M{x - 30} 110c18 4 30-20 36-46c5-22-6-30-12-16c-8 20-6 50 2 58c8 8 22-2 32-12" fill="none" stroke="{d}" stroke-width="6" stroke-linecap="round"/>')
    # display: forma decorativa con línea interior y sombra
    x = c(4); b.append(f'<rect x="{x - 14}" y="38" width="32" height="88" fill="{P["soft"]}"/><rect x="{x - 18}" y="34" width="32" height="88" fill="{d}"/><path d="M{x - 2} 42V114" stroke="#FFF" stroke-width="3"/>')
    return raw(172, "".join(b), "Una letra I dibujada en cinco familias: con serif (remates finos y contraste), sin serif (asta pareja), egipcia (remates rectangulares gruesos), manuscrita (trazo continuo) y display (forma decorativa)")

def _pesos():
    b = []
    for i, w in enumerate((300, 400, 500, 600, 700, 800, 900)):
        x = 26 + i * 86
        b.append(f'<text x="{x + 36}" y="80" font-family="{FONT}" font-size="46" font-weight="{w}" fill="{P["dark"]}" text-anchor="middle">Aa</text>')
        b.append(text(x + 36, 110, w, 12, 600, P["ink"]))
    b.append(f'<text x="320" y="160" font-family="{FONT}" font-size="26" font-style="italic" fill="{P["acc"]}" text-anchor="middle">Itálica · <tspan font-variant="small-caps">Versalitas</tspan> · 0123</text>')
    return raw(180, "".join(b), "La misma familia en siete pesos, de 300 a 900, y una línea de ejemplo en itálica, versalitas y números")

def _armonias():
    b = []; esquemas = [("Monocromática", [0]), ("Análoga", [0, 1, 2]), ("Complementaria", [0, 6]), ("Compl. dividida", [0, 5, 7]), ("Tríada", [0, 4, 8])]
    for k, (lab, sel) in enumerate(esquemas):
        cx = 72 + k * 124; cy = 82
        for i in range(12):
            a = -math.pi / 2 + 2 * math.pi * i / 12; r, g, bb = colorsys.hls_to_rgb(((270 + i * 30) % 360) / 360, .5, .7)
            col = "#%02X%02X%02X" % (int(r * 255), int(g * 255), int(bb * 255))
            on = i in sel
            b.append(f'<circle cx="{cx + 44 * math.cos(a):.1f}" cy="{cy + 44 * math.sin(a):.1f}" r="{11 if on else 8}" fill="{col}" opacity="{1 if on else .22}" stroke="{"#111" if on else "none"}" stroke-width="2"/>')
        if lab == "Monocromática":
            for j, l in enumerate((.3, .5, .72)):
                r, g, bb = colorsys.hls_to_rgb(270 / 360, l, .7)
                b.append(f'<rect x="{cx - 27 + j * 18}" y="{cy - 8}" width="16" height="16" rx="3" fill="#%02X%02X%02X"/>' % (int(r * 255), int(g * 255), int(bb * 255)))
        b.append(text(cx, 156, lab, 12.5, 700))
    return raw(170, "".join(b), "Cinco círculos cromáticos con los colores elegidos en cada armonía: monocromática, análoga, complementaria, complementaria dividida y tríada")

def _lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]

def _contraste():
    pares = [("#111111", "#FFFFFF"), ("#FFFFFF", P["acc"]), ("#767676", "#FFFFFF"), ("#A3A3A3", "#FFFFFF"), ("#FFFFFF", "#FACC15")]
    b = []
    for i, (fg, bg) in enumerate(pares):
        l1, l2 = sorted((_lum(fg), _lum(bg)), reverse=True); r = (l1 + .05) / (l2 + .05)
        x = 20 + i * 122; ok = r >= 4.5
        b.append(f'<rect x="{x}" y="14" width="110" height="96" rx="12" fill="{bg}" stroke="{P["soft"]}" stroke-width="1.5"/>')
        b.append(f'<text x="{x + 55}" y="72" font-family="{FONT}" font-size="30" font-weight="700" fill="{fg}" text-anchor="middle">Texto</text>')
        b.append(text(x + 55, 134, f"{r:.1f} : 1".replace(".", ","), 14, 700, P["dark"]))
        b.append(text(x + 55, 154, "Cumple para texto" if ok else "No alcanza", 12, 600, P["acc"] if ok else "#7A2E2E"))
    b.append(text(320, 186, "Mínimo para texto común: 4,5 : 1. Texto grande y elementos gráficos: 3 : 1.", 12.5, 500, P["ink"]))
    return raw(200, "".join(b), "Cinco ejemplos de texto sobre fondo con su relación de contraste: negro sobre blanco, blanco sobre violeta y gris medio sobre blanco cumplen; gris claro sobre blanco y blanco sobre amarillo no alcanzan")

def _vector_bitmap():
    b = [f'<rect x="20" y="14" width="290" height="200" rx="14" fill="{P["tint"]}"/>', f'<rect x="330" y="14" width="290" height="200" rx="14" fill="{P["tint"]}"/>']
    b.append(f'<circle cx="165" cy="114" r="70" fill="{P["acc"]}"/>')
    for (x, y) in ((95, 114), (165, 44), (235, 114), (165, 184)):
        b.append(f'<rect x="{x - 5}" y="{y - 5}" width="10" height="10" fill="#FFF" stroke="{P["dark"]}" stroke-width="2"/>')
    cx, cy, r, px = 475, 114, 70, 14
    for gx in range(-5, 5):
        for gy in range(-5, 5):
            mx, my = (gx + .5) * px, (gy + .5) * px
            if mx * mx + my * my <= r * r:
                b.append(f'<rect x="{cx + gx * px}" y="{cy + gy * px}" width="{px}" height="{px}" fill="{P["acc"]}"/>')
    b.append(text(165, 240, "Vectorial: curvas y nodos", 13, 700)); b.append(text(475, 240, "Mapa de bits ampliado: píxeles", 13, 700))
    return raw(254, "".join(b), "Un mismo círculo: en vectores mantiene el borde liso con cuatro nodos; en mapa de bits ampliado se ven los píxeles escalonados")

def _tipos_marca():
    b = []; labs = ["Logotipo", "Isotipo", "Imagotipo", "Isologo", "Monograma", "Emblema"]
    d, a = P["dark"], P["acc"]
    for i, lab in enumerate(labs):
        x = 20 + (i % 3) * 205; y = 14 + (i // 3) * 140
        b.append(f'<rect x="{x}" y="{y}" width="190" height="100" rx="12" fill="{P["tint"]}"/>')
        b.append(text(x + 95, y + 122, lab, 13, 700))
    W = lambda x, y, s=20, anc="middle": f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{s}" font-weight="800" letter-spacing="1" fill="{d}" text-anchor="{anc}">MOLIENDA</text>'
    b.append(W(115, 72, 24))
    b.append(f'<circle cx="320" cy="64" r="30" fill="{a}"/><path d="M308 64q12-22 24 0q-12 22-24 0" fill="#FFF"/>')
    b.append(f'<circle cx="460" cy="64" r="20" fill="{a}"/><path d="M452 64q8-14 16 0q-8 14-16 0" fill="#FFF"/>' + W(486, 71, 17, "start"))
    b.append(f'<circle cx="115" cy="190" r="40" fill="{a}"/>' + f'<text x="115" y="194" font-family="{FONT}" font-size="11" font-weight="800" fill="#FFF" text-anchor="middle">MOLIENDA</text>')
    b.append(f'<text x="320" y="208" font-family="Georgia, serif" font-size="52" font-weight="700" fill="{d}" text-anchor="middle">M<tspan fill="{a}" dx="-2">c</tspan></text>')
    b.append(f'<path d="M490 162h60v34q0 22-30 30q-30-8-30-30z" fill="{d}"/>' + f'<text x="520" y="200" font-family="{FONT}" font-size="22" font-weight="800" fill="#FFF" text-anchor="middle">M</text>')
    return raw(292, "".join(b), "Seis tipos de marca para un café ficticio: solo el nombre (logotipo), solo un símbolo (isotipo), símbolo y nombre separables (imagotipo), símbolo y nombre fundidos (isologo), iniciales (monograma) y escudo (emblema)")

def _pagina():
    b = [f'<rect x="80" y="20" width="230" height="240" fill="#FFFFFF" stroke="{P["dark"]}" stroke-width="2"/>', f'<rect x="310" y="20" width="230" height="240" fill="#FFFFFF" stroke="{P["dark"]}" stroke-width="2"/>']
    b.append(f'<path d="M310 20V260" stroke="{P["dark"]}" stroke-width="3"/>')
    for x in (108, 330):
        b.append(f'<rect x="{x}" y="56" width="182" height="168" fill="{P["tint"]}" stroke="{P["soft"]}" stroke-dasharray="4 3"/>')
        b.append(f'<rect x="{x}" y="36" width="80" height="6" rx="3" fill="{P["soft"]}"/>')
    b.append(f'<rect x="114" y="238" width="16" height="8" fill="{P["acc"]}"/><rect x="506" y="238" width="16" height="8" fill="{P["acc"]}"/>')
    for (x1, y1, x2, y2) in ((150, 38, 150, 18), (122, 246, 70, 288), (310, 20, 310, 6), (320, 200, 384, 288), (470, 150, 546, 150), (94, 150, 30, 150)):
        b.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{P["acc"]}" stroke-width="1.4"/>')
    out = [text(158, 16, "Cornisa", 12.5, 700, P["acc"], "start"), text(70, 302, "Folio", 12.5, 700, P["acc"]),
           text(318, 14, "Lomo", 12.5, 700, P["acc"], "start"), text(388, 300, "Medianil de lomo", 12.5, 700, P["acc"], "start"),
           text(552, 155, "Caja de", 12.5, 700, P["acc"], "start"), text(552, 171, "texto", 12.5, 700, P["acc"], "start"),
           text(30, 142, "Margen", 12.5, 700, P["acc"], "start")]
    return raw(312, "".join(b + out), "Una doble página abierta con sus partes: cornisa arriba, folio abajo, lomo en el centro, medianil junto al lomo, caja de texto y márgenes")

def _historia():
    b = []; x, y, w, h = 240, 12, 160, 284; z = 250 * h / 1920
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{P["tint"]}" stroke="{P["dark"]}" stroke-width="2"/>')
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{z:.1f}" fill="{P["soft"]}" opacity=".7"/><rect x="{x}" y="{y + h - z:.1f}" width="{w}" height="{z:.1f}" fill="{P["soft"]}" opacity=".7"/>')
    b.append(text(x + w / 2, y + h / 2 - 6, "Zona segura", 13, 700)); b.append(text(x + w / 2, y + h / 2 + 12, "lo importante va acá", 11.5, 500, P["ink"]))
    b.append(text(x + w + 18, y + z / 2 + 4, "≈ 250 px: nombre de la cuenta", 12.5, 600, P["dark"], "start"))
    b.append(text(x + w + 18, y + h - z / 2 + 4, "≈ 250 px: botones y respuesta", 12.5, 600, P["dark"], "start"))
    b.append(text(x - 18, y + h / 2, "1080 × 1920 px", 13, 700, P["dark"], "end"))
    return raw(310, "".join(b), "Una historia vertical de 1080 por 1920 píxeles con unos 250 píxeles reservados arriba y abajo, donde la interfaz de la red tapa el contenido")

def _papeleria():
    b = []; d, a, t = P["dark"], P["acc"], P["tint"]
    b.append(f'<rect x="20" y="40" width="150" height="212" fill="#FFF" stroke="{P["soft"]}" stroke-width="1.5"/><circle cx="40" cy="60" r="8" fill="{a}"/>' + "".join(f'<rect x="36" y="{96 + i * 12}" width="{110 - (i % 3) * 14}" height="5" rx="2" fill="{t}"/>' for i in range(8)))
    b.append(f'<rect x="200" y="70" width="140" height="78" rx="4" fill="{d}"/><circle cx="222" cy="92" r="9" fill="{a}"/><rect x="216" y="122" width="70" height="5" fill="{P["soft"]}"/>')
    b.append(f'<rect x="200" y="166" width="140" height="78" rx="4" fill="#FFF" stroke="{P["soft"]}" stroke-width="1.5"/><rect x="216" y="186" width="80" height="6" fill="{d}"/><rect x="216" y="200" width="60" height="4" fill="{P["soft"]}"/>')
    b.append(f'<rect x="370" y="90" width="220" height="110" fill="#FFF" stroke="{P["soft"]}" stroke-width="1.5"/><path d="M370 90l110 60l110-60" fill="none" stroke="{P["soft"]}" stroke-width="1.5"/><circle cx="390" cy="180" r="8" fill="{a}"/>')
    b.append(f'<circle cx="480" cy="244" r="26" fill="none" stroke="{a}" stroke-width="3"/><circle cx="480" cy="244" r="18" fill="none" stroke="{a}" stroke-width="1.5"/>')
    for (x, y, l) in ((95, 272, "Hoja membretada"), (270, 60, "Tarjeta: frente y dorso"), (480, 80, "Sobre"), (540, 250, "Sello")):
        b.append(text(x, y, l, 12.5, 700))
    return raw(286, "".join(b), "Papelería de una marca como sistema: hoja membretada, tarjeta personal de frente y dorso, sobre y sello, con los mismos colores y la misma ubicación del isotipo")

FIGS = {
    "s01d1": (tarjetas([("Identidad visual", "Marcas y sus sistemas"), ("Editorial", "Libros, revistas, folletos"), ("Packaging", "Envases y etiquetas"), ("Digital", "Redes, sitios, interfaces"), ("Gráfica en el espacio", "Carteles y señalética"), ("Ilustración e imagen", "Dibujo, foto, íconos")], 3), "Los grandes campos del diseño gráfico. En esta diplomatura los recorrés todos con un mismo proyecto."),
    "s01d5": (_composiciones(), "Con formas simples ya se pueden comunicar ideas opuestas."),
    "s02d1": (_formatos(), "La serie A: al cortar un formato a la mitad se obtiene el siguiente, sin deformarse."),
    "s02d3": (_jerarquia(), "La jerarquía decide en qué orden se lee: primero qué, después cuándo y dónde."),
    "s02d5": (tarjetas([("Institucional", "Ordenada, alineada, márgenes generosos"), ("Dinámica", "Asimétrica, con tensión y diagonales controladas"), ("Experimental", "Rompe la retícula a propósito, una sola vez")], 3), "Una misma información y una misma retícula, tres caracteres distintos."),
    "s03d2": (_familias(), "Lo que distingue a cada familia se ve ya en una sola letra: los remates y el trazo."),
    "s03d3": (_pesos(), "Una familia completa da variedad sin perder coherencia."),
    "s03d4": (flujo(["¿Dónde se va a leer?", "¿Cuánto texto?", "¿Qué tiene que transmitir?", "¿Qué licencia tiene?"]), "Cuatro preguntas antes de elegir una tipografía."),
    "s03d5": (tarjetas([("Nombre", "Y su grupo o familia"), ("Abecedario", "Mayúsculas, minúsculas y números"), ("Pesos o variantes", "Los que tiene la familia"), ("Frase de ejemplo", "En tamaño de lectura y de título"), ("Diseñador", "Quién la creó"), ("Licencia", "Dónde y cómo se puede usar")], 3), "Qué lleva cada espécimen de la lámina."),
    "s04d1": (escala("Línea corta", "Línea larga", [(0.12, "30 caracteres: corta el ritmo"), (0.35, "45: mínimo cómodo"), (0.55, "65: ideal"), (0.75, "75: máximo cómodo"), (0.93, "100: el ojo se pierde")], titulo="Caracteres por línea"), "El largo de línea cómodo está entre 45 y 75 caracteres, con espacios incluidos."),
    "s04d3": (tarjetas([("Una sola familia", "Variedad con pesos y tamaños"), ("Serif + sin serif", "Contraste clásico y seguro"), ("Display + neutra", "Carácter en títulos, calma en textos"), ("Misma época o autor", "Armonía de origen")], 2), "Cuatro maneras de combinar tipografías. Si se combinan, que sean claramente distintas."),
    "s04d4": (barras([("Título", 48), ("Subtítulo", 24), ("Destacado", 16), ("Texto", 11), ("Epígrafe", 8)], "pt", maxv=50), "Ejemplo de escala tipográfica para un impreso: saltos notorios y coherentes entre niveles. Valores de referencia."),
    "s04d5": (piramide(["Nivel 1: el nombre del evento", "Nivel 2: fecha, hora y lugar", "Nivel 3: detalles, organizadores, contacto"]), "Los tres niveles de información del afiche tipográfico."),
    "s05d3": (_armonias(), "Las armonías se eligen en el círculo cromático y se reparten en proporción, por ejemplo 60, 30 y 10."),
    "s05d4": (_contraste(), "La relación de contraste se calcula: no confíes en el ojo. Probá siempre con un verificador."),
    "s05d5": (flujo(["Tres marcas distintas", "Paleta de 4 a 5 colores", "Códigos HEX y CMYK", "Verificar contraste", "Aplicar a la misma pieza"]), "El recorrido de la entrega de color."),
    "s06d1": (tarjetas([("Mensaje", "¿Dice lo que la pieza necesita?"), ("Calidad técnica", "Foco, luz, resolución"), ("Espacio", "¿Deja lugar para el texto?"), ("Dirección", "Hacia dónde mira o se mueve"), ("Coherencia", "Mismo estilo que el resto"), ("Representación", "¿A quién muestra y cómo?")], 3), "Seis preguntas para elegir una fotografía."),
    "s06d3": (_vector_bitmap(), "Un logo siempre se diseña en vectores: se puede ampliar sin perder calidad."),
    "s06d4": (escala("Más seguro", "Más riesgoso", [(0.08, "Fotos propias o encargadas"), (0.3, "Bancos pagos con licencia"), (0.52, "Bancos gratuitos y Creative Commons"), (0.74, "Imágenes generadas con IA"), (0.94, "Imágenes de internet sin permiso")], titulo="Origen de las imágenes"), "Cuanto más claro el origen y la licencia, menos riesgo para vos y para el cliente. Con personas, además, hace falta su permiso."),
    "s06d5": (lista_check(["Mismo grosor de trazo y mismas esquinas", "Misma grilla y mismo tamaño óptico", "Foto con zona limpia para el texto", "Origen y licencia anotados"], ["Íconos de distintos sets mezclados", "Texto sobre una zona cargada de la foto", "Imágenes sin licencia"]), "Qué mira la entrega de íconos y fotografía."),
    "s07d1": (piramide(["Isologo: el signo principal", "Identidad visual: el sistema de signos", "Marca: lo que la gente piensa y siente"]), "La marca es más grande que el logo: el logo es la punta visible de un sistema."),
    "s07d2": (tarjetas([("El negocio", "Qué hace y por qué"), ("El público", "Quién compra y cómo es"), ("La competencia", "Quién más está"), ("La personalidad", "Cómo es y cómo habla"), ("Usos", "Dónde va a aparecer la marca"), ("Límites", "Presupuesto, plazos, lo que no se toca")], 3), "Las seis áreas del brief de identidad."),
    "s07d3": (matriz(["Café A", "Café B", "Café C", "Molienda"], ["Isologo", "Tipografía", "Color", "Imagen", "Tono"], [["Taza", "Script", "Marrón", "Granos", "Formal"], ["Grano", "Serif", "Marrón", "Granos", "Cálido"], ["Taza", "Script", "Negro", "Latte", "Cálido"], ["?", "?", "?", "?", "?"]]), "Tablero de competencia ficticio: cuando todos repiten lo mismo, ahí aparece el lugar para diferenciarse."),
    "s07d4": (flujo(["Tres palabras clave", "Buscar imágenes", "Elegir de 15 a 25", "Ordenar por clima", "Validar con el cliente"]), "Del concepto en palabras al moodboard."),
    "s07d5": (comparar(("Brief", ["Cliente, negocio y objetivo", "Público y competencia", "Personalidad y palabras clave", "Lista de aplicaciones concretas"]), ("Moodboard", ["Entre 15 y 25 imágenes", "Ordenado por clima visual", "Coherente con las palabras clave", "Sin logos de otras marcas como modelo"])), "Las dos partes de la entrega que guían toda la identidad."),
    "s08d1": (_tipos_marca(), "Los tipos de marca gráfica, dibujados para un café ficticio."),
    "s08d2": (tarjetas([("El nombre", "Escrito de muchas formas"), ("La inicial", "Una letra con carácter"), ("El rubro sin cliché", "Evitar la taza obvia"), ("El lugar", "Barrio, calle, historia"), ("La personalidad", "Cómo se siente la marca"), ("Combinaciones", "Mezclar dos caminos")], 3), "Seis caminos para llegar a treinta bocetos."),
    "s08d4": (tarjetas([("Principal", "Versión completa y a color"), ("Secundaria", "Horizontal o vertical, según el espacio"), ("Isotipo solo", "Para perfil, sello, favicon"), ("Una tinta", "Negro o un color plano"), ("Negativo", "Blanco sobre fondo oscuro"), ("Tamaño mínimo", "Hasta dónde se lee")], 3), "Un sistema de versiones para cada uso."),
    "s08d5": (flujo(["Proceso", "Construcción", "Versiones", "Pruebas de tamaño", "Área de resguardo"]), "El orden de la lámina de presentación del isologo."),
    "s09d1": (tarjetas([("Principal o de títulos", "Da el carácter"), ("Secundaria o de texto", "Se lee cómoda en largo"), ("Alternativa del sistema", "Para documentos de oficina")], 3), "Los roles del sistema tipográfico. La principal y la secundaria pueden ser la misma familia."),
    "s09d2": (barras([("Neutros", 55), ("Primario", 25), ("Secundarios", 15), ("Acento", 5)], "%"), "Ejemplo de proporción de uso de la paleta: el acento funciona porque aparece poco."),
    "s09d4": (comparar(("Estilo fotográfico", ["Luz: natural, de mañana", "Color: cálido, sin saturar", "Encuadre: de cerca, con aire", "Personas: reales, del barrio"]), ("Tono de voz", ["Cercano, de vos", "Frases cortas", "Con humor suave", "Sin tecnicismos"])), "Ejemplo para Molienda: la marca también se reconoce por cómo se ve y cómo habla."),
    "s09d5": (tarjetas([("Isologo", "Principal y versiones"), ("Paleta", "Con códigos"), ("Tipografías", "Con sus roles"), ("Elementos gráficos", "Patrones y recursos"), ("Estilo fotográfico", "Con ejemplos"), ("Tono de voz", "Cómo habla"), ("Aplicación de prueba", "Todo junto en una pieza")], 4), "Lo que reúne la hoja de sistema."),
    "s10d1": (_papeleria(), "La papelería funciona como sistema: mismos colores, mismas posiciones."),
    "s10d2": (flujo(["Destacar en la góndola", "Decir qué es", "Transmitir la marca", "Informar", "Funcionar"]), "Lo que tiene que lograr un packaging en pocos segundos, en orden de lectura."),
    "s10d3": (barras([("A 3 metros", 3), ("A 10 metros", 10), ("A 30 metros", 30)], "cm"), "Altura de mayúscula para lectura cómoda, con la regla prudente de 1 cm por metro. El mínimo legible es alrededor de un tercio."),
    "s10d4": (lista_check(["Mockups realistas para la marca", "Escala creíble", "Colores y materiales fieles", "Mockups con licencia", "Aclarar que es una simulación"], ["Un logo enorme en una taza", "Materiales que la marca no va a usar", "Mockups sin licencia"], tsi="Hacé", tno="Evitá"), "Presentar con honestidad."),
    "s10d5": (tarjetas([("Papelería", "Tarjeta y hoja"), ("Packaging", "Envase o etiqueta"), ("Espacio", "Cartel o vidriera"), ("Objetos y uniforme", "Taza, delantal, bolsa"), ("Digital", "Perfil y posteo")], 3), "Las cinco aplicaciones de la entrega, una de cada mundo."),
    "s11d1": (_pagina(), "Las partes de una doble página."),
    "s11d2": (comparar(("Estilo de párrafo", ["Afecta al párrafo entero", "Tipografía, tamaño, interlineado", "Sangría y espacio antes y después", "Ejemplo: Texto, Título, Epígrafe"]), ("Estilo de carácter", ["Afecta a unas palabras", "Negrita, itálica o color", "Se aplica dentro de un párrafo", "Ejemplo: Destacado, Precio"])), "Con estilos, cambiar un valor cambia todos los textos que lo usan."),
    "s11d3": (escala("Calma", "Impacto", [(0.1, "Página de texto"), (0.35, "Texto con imagen chica"), (0.62, "Imagen a media página"), (0.9, "Imagen a página completa")], titulo="Ritmo en las páginas interiores"), "Alternar páginas de distinto peso da ritmo a la publicación."),
    "s11d4": (comparar(("Impreso", ["Doble página", "Columnas y retícula fija", "Alta resolución", "Se hojea"]), ("Pantalla", ["Una columna que se desliza", "Texto más grande", "Vínculos y menú por categorías", "Archivo liviano"])), "Adaptar no es achicar: es rearmar el contenido para el celular."),
    "s11d5": (linea_tiempo([("Pág. 1", "Tapa"), ("Págs. 2 y 3", "Interiores: doble página"), ("Pág. 4", "Contratapa y contacto")]), "El díptico de cuatro páginas A5."),
    "s12d2": (escala("Liviano", "Con cuerpo", [(0.08, "Obra 80 g"), (0.32, "Ilustración 150 g"), (0.58, "Ilustración 250 g"), (0.84, "Cartulina 300 g")], titulo="Gramaje"), "Más gramaje, más cuerpo y más costo. Valores de referencia: consultá los de tu imprenta."),
    "s12d3": (escala("Pocas copias", "Muchas copias", [(0.1, "Digital"), (0.4, "Serigrafía"), (0.68, "Offset"), (0.92, "Flexografía")], titulo="La cantidad define el sistema"), "Cada sistema tiene su escala. Gran formato, sublimación y sellos se eligen más por el soporte que por la cantidad."),
    "s12d4": (flujo(["Pedir presupuesto con datos completos", "Comparar dos o tres imprentas", "Prueba de color", "Aprobar", "Controlar la entrega"]), "Del pedido a la pieza impresa."),
    "s12d5": (tarjetas([("PDF de impresión", "Con sangrado y marcas"), ("Ficha de especificaciones", "Formato, papel, tintas"), ("Lista de control", "Revisada antes de enviar"), ("Pedido de presupuesto", "Con todos los datos"), ("Foto de una prueba", "Impresa en papel real")], 3), "El paquete de producción del folleto."),
    "s13d1": (_historia(), "Zonas seguras de una historia vertical: confirmá las medidas en la guía de cada red."),
    "s13d2": (comparar(("Celular primero", ["Una columna", "Botones grandes para el dedo", "Menú plegado", "Lo esencial arriba"]), ("Computadora", ["Varias columnas", "Menú visible", "Más aire a los costados", "El mismo contenido, otro orden"])), "Un sitio adaptable se diseña primero para el celular."),
    "s13d3": (tarjetas([("Contraste", "4,5 : 1 para texto"), ("Texto real", "No texto dentro de imágenes"), ("Texto alternativo", "Describe cada imagen"), ("Tamaño y espaciado", "Áreas táctiles cómodas"), ("No depender del color", "Sumar íconos o texto")], 3), "Lo accesible funciona mejor para todos."),
    "s13d4": (tarjetas([("Duración", "Corta: menos de un segundo en interfaces"), ("Aceleración", "Arranca y frena suave"), ("Propósito", "Mover para explicar algo"), ("Jerarquía", "Primero lo principal"), ("Coherencia", "Mismo ritmo en toda la marca")], 3), "Criterios básicos para animar la marca."),
    "s13d5": (tarjetas([("Cuatro plantillas", "De publicación"), ("Una historia", "Con zonas seguras"), ("Foto de perfil", "Con el isotipo"), ("Una pieza animada", "Corta y con propósito"), ("Simulación de grilla", "Cómo se ve el perfil"), ("Texto alternativo", "Para cada pieza")], 3), "Lo que lleva el kit de redes."),
    "s14d1": (tarjetas([("Vectores", "Logos, íconos, ilustración"), ("Fotos", "Mapa de bits y retoque"), ("Maquetación", "Editorial de varias páginas"), ("Interfaces", "Pantallas y prototipos"), ("Piezas rápidas", "Plantillas para redes"), ("Movimiento", "Animación y video"), ("Boceto", "Papel o tableta"), ("Con IA", "Asistentes y generación")], 4), "El mapa del software por tipo de tarea. Cada casillero tiene opciones pagas y gratuitas."),
    "s14d2": (comparar(("La IA ayuda a", ["Preparar la entrevista", "Ordenar el brief", "Generar listas de nombres", "Probar textos y tono", "Escribir textos alternativos"]), ("La IA no", ["Conoce al cliente", "Verifica sus datos: inventa con seguridad", "Reemplaza tu criterio", "Decide qué es lo bueno"])), "Usala para ampliar opciones; la decisión y la verificación son tuyas."),
    "s14d3": (escala("Le va bien", "Le va mal", [(0.08, "Moodboards"), (0.28, "Edición de fotos"), (0.5, "Variaciones y maquetas"), (0.72, "Texto dentro de imágenes"), (0.92, "Vectores limpios para un logo")], titulo="La IA de imágenes en el diseño gráfico"), "Una orientación general: las herramientas cambian rápido, probalas en cada caso."),
    "s14d4": (lista_check(["Contale al cliente si usaste IA", "Leé las condiciones de uso", "Verificá todo lo que produce"], ["Usar IA para el isologo", "Subir información confidencial", "Presentar lo generado como propio sin revisar"], tsi="Hacé", tno="Evitá"), "Pautas de uso responsable mientras las reglas se siguen discutiendo."),
    "s14d5": (flujo(["Brief", "Investigación", "Bocetos", "Vectorización", "Sistema", "Aplicaciones", "Producción", "Entrega"]), "Un flujo de trabajo de identidad: marcá en cada etapa qué herramienta usás y dónde entra la IA."),
    "s15d1": (tarjetas([("1. Introducción", "Personalidad y concepto"), ("2. Isologo", "Construcción y versiones"), ("3. Usos incorrectos", "Lo que no se hace"), ("4. Color", "Códigos y proporciones"), ("5. Tipografía", "Familias y roles"), ("6. Elementos gráficos", "Patrones y recursos"), ("7. Foto y tono", "Ejemplos sí y no"), ("8. Aplicaciones", "Piezas con medidas"), ("9. Archivos", "Lista y contacto")], 3), "La estructura de un manual de marca."),
    "s15d3": (barras([("Reunión e investigación", 6), ("Moodboard y exploración", 8), ("Isologo y versiones", 16), ("Sistema", 8), ("Cinco aplicaciones", 12), ("Manual de marca", 10), ("Correcciones", 8)], "h", maxv=16), "Horas estimadas por etapa: 68 horas en total. Con un valor hora ficticio de $ 20.000, el presupuesto da $ 1.360.000."),
    "s15d4": (flujo(["Buscar el nombre en el INPI", "Elegir la clase de Niza", "Diseñar sin elementos ajenos", "Consultar a un agente", "Presentar la solicitud"], destacar=0), "Verificar antes de diseñar: si el nombre ya está registrado, todo el trabajo se pierde."),
    "s15d5": (matriz(["Completitud", "Claridad", "Coherencia", "Datos técnicos"], ["Isologo", "Color", "Tipografía", "Aplicaciones"], [[2, 2, 1, 2], [2, 1, 2, 2], [2, 2, 2, 1], [1, 2, 2, 2]]), "Ejemplo de autoevaluación del manual antes de entregar."),
    "s16d1": (flujo(["Punto de partida", "Proceso en breve", "Concepto", "La marca, sola", "El sistema", "Aplicaciones", "Próximos pasos"], destacar=3), "El orden de la presentación al cliente."),
    "s16d2": (flujo(["Portada", "El desafío", "El proceso", "La solución", "Las aplicaciones", "El resultado", "Créditos"]), "La estructura de un caso de portfolio."),
    "s16d3": (linea_tiempo([("0:00", "Comienzo que engancha"), ("0:10", "El desafío"), ("0:30", "El proceso"), ("0:55", "La solución"), ("1:35", "El cierre"), ("1:55", "Nombre y contacto")]), "El guion del video de dos minutos."),
    "s16d4": (tarjetas([("Investigación y brief", "Hallazgos que guían"), ("Isologo", "Construido y versátil"), ("Sistema", "Reconocible sin logo"), ("Aplicaciones", "Producibles"), ("Editorial e impresión", "Listo para imprenta"), ("Digital", "Coherente y accesible"), ("Manual y presentación", "Claro y convincente")], 4), "Los siete criterios de la rúbrica final."),
    "s16d5": (tarjetas([("Manual de marca", "PDF"), ("Presentación", "PDF"), ("Caso de portfolio", "Publicado o PDF"), ("Video", "Dos minutos"), ("Archivos de marca", "SVG, PDF, PNG"), ("Folleto", "Listo para imprenta"), ("Comparación", "Semana 1 y hoy")], 4), "Todo lo que entregás al cierre."),
}
