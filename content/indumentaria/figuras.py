"""Gráficos adicionales del curso de Indumentaria (uno por clase que no tenía)."""
from figlib import *

def _cabeza():
    b = []
    # cabeza con líneas de proporción
    b.append(f'<ellipse cx="150" cy="120" rx="62" ry="84" fill="#FFFFFF" stroke="#111" stroke-width="2.5"/>')
    for y, lab in ((120, "Ojos: mitad"), (162, "Nariz"), (184, "Boca")):
        b.append(f'<path d="M70 {y}H230" stroke="{P["soft"]}" stroke-dasharray="5 4"/>')
        b.append(text(244, y + 4, lab, 12.5, 600, P["dark"], "start"))
    b.append(f'<path d="M122 120q8-6 16 0M162 120q8-6 16 0M146 158q4 6 8 0M136 184q14 8 28 0" stroke="#111" stroke-width="2" fill="none"/>')
    # mano como mitón
    b.append(f'<path d="M420 60q30-6 44 14l14 60q4 22-14 30l-40 6q-20-2-22-24z" fill="{P["tint"]}" stroke="#111" stroke-width="2.2"/>')
    b.append(f'<path d="M418 92q-20 4-24 26q8 10 24 0" fill="{P["tint"]}" stroke="#111" stroke-width="2.2"/>')
    b.append(text(450, 200, "Mano: forma de mitón,", 12.5, 600, P["dark"]))
    b.append(text(450, 218, "mide como la cara", 12.5, 600, P["dark"]))
    # pie con taco
    b.append(f'<path d="M540 70l18 70l40 24h12v10h-56l-30-96z" fill="{P["tint"]}" stroke="#111" stroke-width="2.2"/>')
    b.append(text(575, 200, "Pie con taco:", 12.5, 600, P["dark"]))
    b.append(text(575, 218, "talón arriba", 12.5, 600, P["dark"]))
    return raw(234, "".join(b), "Cabeza con las líneas de ojos, nariz y boca; una mano dibujada como mitón y un pie con taco inclinado")

def _pliegues():
    b = []
    labs = ["De tensión", "Colgante", "De compresión", "De giro"]
    for i, lab in enumerate(labs):
        x = 20 + i * 155
        b.append(f'<rect x="{x}" y="14" width="140" height="150" rx="14" fill="{P["tint"]}"/>')
        b.append(text(x + 70, 190, lab, 13, 700))
    s = f'stroke="{P["dark"]}" stroke-width="2.4" fill="none" stroke-linecap="round"'
    b.append(f'<circle cx="60" cy="50" r="6" fill="{P["acc"]}"/><path d="M66 54L140 120M64 60L120 140M70 50L150 80" {s}/>')
    b.append(f'<path d="M225 30h40M228 30L200 150M245 30L245 150M262 30L290 150M200 150q22 10 45 0q22 10 45 0" {s}/>')
    b.append(f'<path d="M355 40h80M355 150h80M362 60l15 10l-15 10l15 10l-15 10l15 10l-15 10M410 60l15 10l-15 10l15 10l-15 10l15 10l-15 10" {s}/>')
    b.append(f'<path d="M530 40c55 20 55 40 0 60c-45 18-45 40 10 60M560 40c32 20 32 40 0 60" {s}/>')
    return raw(204, "".join(b), "Cuatro tipos de pliegues: de tensión que irradian desde un punto, colgantes que se abren hacia abajo, de compresión en zigzag y de giro en espiral")

def _prendas():
    b = []; s = 'fill="#FFFFFF" stroke="#111" stroke-width="2.2" stroke-linejoin="round"'
    b.append(f'<path d="M40 40l30-14h40l30 14l18 40l-22 8l-12-24v100h-88v-100l-12 24l-22-8z" {s}/>')
    b.append(f'<path d="M205 30h70l10 140h-38l-7-90l-7 90h-38z" {s}/>')
    b.append(f'<path d="M335 30h70v12h-70zM335 42h70l26 128h-122z" {s}/>')
    b.append(f'<path d="M485 30h50l18 12l20 30l-18 10l-12-18v20l20 86h-108l20-86v-20l-12 18l-18-10l20-30z" {s}/>')
    for x, lab in ((90, "Remera"), (240, "Pantalón"), (370, "Falda evasé"), (510, "Vestido")):
        b.append(text(x, 196, lab, 13, 700))
    return raw(210, "".join(b), "Geometrales simples de cuatro prendas básicas: remera, pantalón, falda evasé y vestido")

def _holgura():
    b = []
    b.append(f'<circle cx="160" cy="110" r="58" fill="{P["tint"]}" stroke="{P["dark"]}" stroke-width="2"/>')
    b.append(f'<circle cx="160" cy="110" r="72" fill="none" stroke="{P["acc"]}" stroke-width="3" stroke-dasharray="8 5"/>')
    b.append(text(160, 115, "Cuerpo", 13, 700))
    b.append(text(160, 208, "Prenda con holgura de confort", 13, 600))
    b.append(f'<circle cx="460" cy="110" r="58" fill="{P["tint"]}" stroke="{P["dark"]}" stroke-width="2"/>')
    b.append(f'<circle cx="460" cy="110" r="94" fill="none" stroke="{P["acc"]}" stroke-width="3" stroke-dasharray="8 5"/>')
    b.append(text(460, 115, "Cuerpo", 13, 700))
    b.append(text(460, 222, "Prenda amplia: holgura de diseño", 13, 600))
    return raw(232, "".join(b), "Corte horizontal esquemático del torso: una prenda con poca holgura de confort y otra amplia con mucha holgura de diseño")

def _plano_punto():
    b = [f'<rect x="20" y="14" width="280" height="170" rx="14" fill="{P["tint"]}"/>', f'<rect x="340" y="14" width="280" height="170" rx="14" fill="{P["tint"]}"/>']
    for i in range(8):
        y = 34 + i * 18
        b.append(f'<path d="M40 {y}H280" stroke="{P["dark"]}" stroke-width="5" stroke-linecap="round"/>')
    for j in range(12):
        x = 50 + j * 20
        d = "".join(f'{"M" if i == 0 else "L"}{x + (5 if (i + j) % 2 else -5)} {34 + i * 18}' for i in range(8))
        b.append(f'<path d="{d}" stroke="{P["acc"]}" stroke-width="4" fill="none"/>')
    for r in range(5):
        y = 40 + r * 28
        for c in range(9):
            x = 370 + c * 26
            b.append(f'<path d="M{x} {y + 22}c-6-14 2-26 13-26s19 12 13 26" stroke="{P["acc"] if r % 2 else P["dark"]}" stroke-width="3.5" fill="none"/>')
    b.append(text(160, 208, "Plano: urdimbre y trama se cruzan", 13, 700))
    b.append(text(480, 208, "Punto: bucles enlazados", 13, 700))
    return raw(220, "".join(b), "Esquema de un tejido plano con hilos cruzados en ángulo recto y de un tejido de punto con bucles enlazados")

def _base_cuerpo():
    b = []; s = f'fill="{P["tint"]}" stroke="#111" stroke-width="2.4" stroke-linejoin="round"'
    b.append(f'<path d="M90 64Q132 60 146 28L236 46Q222 84 232 124L226 222H90Z" {s}/>')
    b.append(f'<path d="M90 64V222" stroke="{P["dark"]}" stroke-width="3"/>')
    b.append(f'<path d="M229 138L172 128L228 152" fill="none" stroke="{P["acc"]}" stroke-width="2.4"/>')
    b.append(f'<path d="M140 222L150 158L160 222" fill="none" stroke="{P["acc"]}" stroke-width="2.4"/>')
    labels = ((300, 36, "Escote", 120, 52), (300, 62, "Línea de hombro", 196, 38), (300, 104, "Sisa", 230, 96), (300, 146, "Pinza de busto (se puede trasladar)", 200, 140), (300, 196, "Pinza de cintura", 156, 190))
    for x, y, t, px, py in labels:
        b.append(f'<path d="M{x - 6} {y - 4}L{px} {py}" stroke="{P["soft"]}"/>')
        b.append(text(x, y, t, 13, 600, P["dark"], "start"))
    b.append(text(60, 150, "Centro delantero", 12, 600, P["dark"]).replace("<text ", '<text transform="rotate(-90 60 150)" '))
    return raw(240, "".join(b), "Medio delantero de la base de cuerpo con centro delantero, escote, hombro, sisa, pinza de busto y pinza de cintura")

def _margenes():
    b = []
    b.append(f'<path d="M140 30H430Q470 30 478 110V250H140Z" fill="{P["tint"]}" stroke="#111" stroke-width="2.4"/>')
    b.append(f'<path d="M156 46H420Q452 46 462 112V234H156Z" fill="none" stroke="{P["dark"]}" stroke-width="1.6" stroke-dasharray="6 5"/>')
    for x, y in ((140, 130), (478, 130)):
        b.append(f'<path d="M{x - 6 if x == 140 else x} {y}h6" stroke="#111" stroke-width="3"/>')
    b.append(f'<path d="M478 150l-8 0" stroke="#111" stroke-width="3"/><path d="M478 158l-8 0" stroke="#111" stroke-width="3"/>')
    b.append(arrow(300, 210, 300, 80, P["acc"], 2.5)); b.append(text(316, 150, "Hilo", 13, 700, P["acc"], "start"))
    b.append(text(70, 60, "Línea de corte", 12.5, 600, P["dark"], "middle"))
    b.append(text(70, 100, "Línea de costura", 12.5, 600, P["dark"], "middle"))
    b.append(f'<path d="M112 60H140M112 100H156" stroke="{P["soft"]}"/>')
    b.append(text(560, 154, "Piquetes", 12.5, 600, P["dark"]))
    return raw(266, "".join(b), "Molde de falda con línea de corte continua, línea de costura punteada a un centímetro, piquetes en el costado y flecha del hilo")

def _tizada():
    b = [f'<rect x="20" y="20" width="600" height="160" fill="{P["tint"]}" stroke="{P["dark"]}" stroke-width="2"/>']
    b.append(text(320, 14, "Ancho de la tela: 1,50 m", 12, 600, P["dark"]))
    pcs = [(30, 30, 150, 140, "Delantero (doblez)"), (190, 30, 150, 140, "Espalda"), (350, 30, 150, 140, "Espalda"), (510, 30, 100, 40, "Pretina"), (510, 80, 50, 40, "Vista"), (565, 80, 45, 90, "Bolsillo")]
    for x, y, w, h, t in pcs:
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#FFFFFF" stroke="{P["acc"]}" stroke-width="2"/>')
        b.append(text(x + w / 2, y + h / 2 + 4, t, 11.5, 600, P["dark"], n=max(6, int(w / 7))))
    b.append(f'<path d="M20 196H620" stroke="{P["dark"]}" stroke-width="1.5"/>'); b.append(text(320, 214, "Largo usado = consumo por prenda", 12.5, 600, P["dark"]))
    return raw(222, "".join(b), "Tizada esquemática: piezas de falda ubicadas sobre el ancho de la tela para usar el menor largo posible")

def _dobladillos():
    b = []; s = f'stroke="{P["acc"]}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    b.append(f'<path d="M60 30V130Q60 140 70 140V112Q70 104 62 104" {s}/>')
    b.append(f'<path d="M230 30V130Q230 140 240 140V100" {s}/><path d="M240 92v8" stroke="{P["dark"]}" stroke-width="7"/>')
    b.append(f'<path d="M400 40Q380 60 380 100V140" {s}/><path d="M400 40Q440 60 440 120" stroke="{P["dark"]}" stroke-width="5" fill="none"/>')
    b.append(f'<path d="M560 30V140M548 150Q560 160 572 150M548 150V136M572 150V136" {s}/>')
    for x, t in ((65, "Doble doblez"), (235, "Overlock y un doblez"), (410, "Vista"), (560, "Ribete al bies")):
        b.append(text(x, 186, t, 13, 700))
    return raw(200, "".join(b), "Cortes esquemáticos de cuatro terminaciones: dobladillo doble, dobladillo con overlock, vista interior y ribete al bies")

def _simbolos():
    b = []; s = f'stroke="{P["dark"]}" stroke-width="2.6" fill="none" stroke-linejoin="round"'
    b.append(f'<path d="M40 40l8 40h52l8-40" {s}/><path d="M36 40q10 8 20 0t20 0t20 0t20 0" {s}/>'); b.append(text(78, 72, "30", 15, 700))
    b.append(f'<path d="M200 80l40-50l40 50z" {s}/><path d="M196 34l88 50M284 34l-88 50" stroke="{P["acc"]}" stroke-width="2.6"/>')
    b.append(f'<rect x="338" y="32" width="54" height="50" {s}/><circle cx="365" cy="57" r="17" {s}/>')
    b.append(f'<path d="M450 80h70q0-34-30-34h-20q-14 0-20 14z" {s}/><circle cx="478" cy="68" r="3" fill="{P["dark"]}"/><circle cx="492" cy="68" r="3" fill="{P["dark"]}"/>')
    b.append(f'<circle cx="584" cy="57" r="25" {s}/>'); b.append(text(584, 63, "P", 16, 700))
    for x, t in ((78, "Lavar a 30 °C"), (240, "No usar lavandina"), (365, "Secarropas"), (485, "Planchar a temperatura media"), (584, "Limpieza en seco")):
        b.append(text(x, 120, t, 12, 600, P["dark"], n=14, lh=14))
    return raw(150, "".join(b), "Símbolos de cuidado: batea de lavado a 30 grados, triángulo de blanqueo tachado, cuadrado con círculo de secarropas, plancha con dos puntos y círculo de limpieza en seco")

def _maquinas():
    return tarjetas([("Recta", "Una puntada recta. Costuras de tela plana, pespuntes, cierres."), ("Overlock", "Cose, corta y envuelve el borde. Terminaciones y tejido de punto."), ("Collareta", "Dos o tres agujas, puntada elástica. Ruedos de remeras.")], 3)

FIGS = {
    "s01d1": (flujo(["Investigar", "Concepto", "Diseñar", "Desarrollar", "Prototipar", "Producir", "Presentar y vender"], destacar=4), "El recorrido de una colección: el prototipo es el momento en que la idea se vuelve prenda."),
    "s01d4": (_cabeza(), "Simplificar no es descuidar: proporciones claras en cabeza, manos y pies."),
    "s01d5": (lista_check(["Nueve divisiones marcadas antes de dibujar", "Pie de apoyo bajo el hueco del cuello", "Hombros y cadera en sentidos opuestos", "Un mismo estilo de cabeza, manos y pies"], ["Figurín que parece caerse", "Piernas cortas o brazos que no llegan a la entrepierna", "Detalles realistas que compiten con la ropa"], tsi="Revisá que esté", tno="Evitá"), "Lista de control de la planilla de figurines."),
    "s02d1": (_pliegues(), "Cada pliegue cuenta dónde se apoya, cuelga, se junta o gira la tela."),
    "s02d2": (_prendas(), "Las prendas básicas: casi todo diseño es una variación de ellas."),
    "s02d3": (tarjetas([("Jean", "Pespuntes dobles y diagonal de sarga"), ("Cuero", "Pocos pliegues, brillos nítidos"), ("Seda o satén", "Brillos suaves que siguen los pliegues"), ("Gasa o tul", "Transparencia y bordes más oscuros"), ("Punto grueso", "Trenzas solo en bordes y zonas clave"), ("Pana", "Líneas finas paralelas que siguen la forma")], 3), "Recursos de dibujo para que se lea el material."),
    "s02d4": (flujo(["Color base plano", "Sombra del lado opuesto a la luz", "Brillo según el material", "Línea final", "Piel y pelo simples"]), "Los cinco pasos de un render rápido."),
    "s02d5": (matriz(["Look 1", "Look 2", "Look 3"], ["Proporción", "Caída", "Material", "Render"], [[2, 2, 1, 2], [2, 1, 2, 1], [1, 2, 2, 2]]), "Ejemplo de autoevaluación: marcá en qué criterio está más flojo cada look antes de entregar."),
    "s03d2": (barras([("S · cadera", 94), ("M · cadera", 98), ("L · cadera", 102), ("XL · cadera", 106)], "cm", maxv=110), "Ejemplo de progresión de una tabla de talles: unos 4 cm de contorno entre talles. Valores ilustrativos."),
    "s03d3": (_holgura(), "La diferencia entre la prenda y el cuerpo es la holgura: de confort o de diseño."),
    "s03d4": (tarjetas([("Pinzas", "Triángulos que se cosen y dan volumen"), ("Cortes", "Varias piezas cuya unión da la curva"), ("Fruncidos y pliegues", "Tela que se junta para dar volumen"), ("Elasticidad", "El punto se adapta solo al cuerpo"), ("Bies", "Tela en diagonal que acompaña el cuerpo"), ("Bases", "Moldes ajustados de los que salen los demás")], 3), "Los recursos de la moldería para que una tela plana envuelva un cuerpo curvo."),
    "s03d5": (flujo(["Medir dos cuerpos", "Medir tres prendas", "Calcular holgura", "Prueba de movimiento", "Lámina de análisis"]), "El recorrido de la entrega de la semana."),
    "s04d1": (tarjetas([("Vegetales", "Algodón, lino, cáñamo"), ("Animales", "Lana, alpaca, llama, seda"), ("Artificiales", "Viscosa, modal, lyocell"), ("Sintéticas", "Poliéster, poliamida, elastano")], 4), "Las cuatro grandes familias de fibras textiles."),
    "s04d2": (_plano_punto(), "Tejido plano y tejido de punto: dos construcciones, dos comportamientos."),
    "s04d3": (escala("Fluida", "Con cuerpo", [(0.08, "Gasa"), (0.22, "Viscosa"), (0.4, "Poplín"), (0.58, "Gabardina"), (0.76, "Jean"), (0.92, "Paño")], titulo="Caída de la tela"), "La caída define qué silueta permite cada tela."),
    "s04d4": (tarjetas([("Cierres", "Metálicos, inyectados, invisibles, separables"), ("Botones", "De agujeros, con pie, a presión"), ("Entretelas", "Dan cuerpo a cuellos, puños y pretinas"), ("Elásticos", "Cinturas, puños y ruedos"), ("Etiquetas", "Marca, composición y cuidado, talle"), ("Hilos", "Costura y pespunte")], 3), "Los avíos más usados y su función."),
    "s04d5": (flujo(["Conseguir muestras", "Probar: estirar, arrugar, contraluz", "Lavar una muestra", "Completar la ficha", "Fotografiar"]), "Cómo se arma el muestrario comentado."),
    "s05d1": (piramide(["Micro tendencia: semanas", "Tendencia de temporada: una o dos temporadas", "Macro tendencia: años"]), "Cuanto más profunda la tendencia, más dura y más útil es para una marca."),
    "s05d2": (tarjetas([("Su día", "Qué hace y cómo se mueve"), ("Qué valora", "Comodidad, duración, imagen, precio"), ("Su cuerpo", "Talles y necesidades de calce"), ("Su contexto", "Clima, ciudad, trabajo"), ("Lo que le molesta", "De la ropa que usa hoy"), ("Su ocasión", "Para qué momento es la colección")], 3), "Seis preguntas para describir al usuario de una colección."),
    "s05d3": (tarjetas([("Ropa de trabajo", "Funcionalidad y durabilidad"), ("Ropa deportiva", "Movilidad y materiales técnicos"), ("Indumentaria regional", "Textiles y técnicas con significado"), ("Décadas del siglo XX", "Siluetas reconocibles"), ("Diseñadores", "Formas de pensar la ropa"), ("Arte y naturaleza", "Formas, colores, texturas")], 3), "Fuentes de referentes: de cada una se toma un principio, no una copia."),
    "s05d4": (flujo(["Usuario y ocasión", "Investigación", "Concepto: título y frase", "Decisiones de diseño", "Moodboard"], destacar=2), "El concepto ordena la investigación y se traduce en decisiones concretas."),
    "s05d5": (lista_check(["Concepto claro en un título y dos frases", "De 15 a 25 imágenes con orden", "Decisiones de diseño que salen del concepto"], ["Collage de cien imágenes al azar", "Solo fotos de otras marcas", "Un concepto que no menciona al usuario"]), "Qué hace fuerte a una lámina de concepto."),
    "s06d1": (matriz(["Remera", "Camisa", "Buzo", "Campera"], ["Pantalón", "Falda", "Cargo", "Short"], [[2, 2, 2, 2], [2, 2, 1, 1], [2, 1, 2, 2], [2, 2, 2, 0]], leyenda=("No combina", "A veces", "Combina")), "Matriz de combinaciones de una cápsula: en una buena colección casi todo combina con todo."),
    "s06d2": (barras([("Neutros", 60), ("Colores de colección", 30), ("Acento", 10)], "%"), "Una proporción habitual de la paleta en una colección cápsula."),
    "s06d4": (flujo(["Bocetar 5 variantes", "Cambiar una variable por vez", "¿Concepto, usuario, combina, se produce?", "Elegir la mejor", "Armar los looks"]), "Explorar mucho antes de decidir."),
    "s06d5": (lista_check(["Misma pose y escala en los seis looks", "Ritmo de color a lo largo de la fila", "Variedad de siluetas y tipologías"], ["Todos los oscuros juntos", "Seis siluetas iguales", "Un look que no comparte la paleta"]), "Qué mira el line-up."),
    "s07d1": (tarjetas([("Papel de molde", "Firme y manejable"), ("Regla y escuadra", "Rectas y ángulos rectos"), ("Curvas francesas", "Escote, sisa, tiro"), ("Cinta métrica", "Medir curvas"), ("Ruleta y punzón", "Copiar y marcar"), ("Dos tijeras", "Una para papel, otra para tela")], 3), "El equipo básico de moldería."),
    "s07d3": (_base_cuerpo(), "La base de cuerpo resuelve más curvas que la falda: hombro, cuello, busto y sisa."),
    "s07d5": (flujo(["Tomar medidas", "Rectángulo base", "Línea de cadera", "Costado y pinzas", "Rotular"]), "Del cuerpo al molde base de falda."),
    "s08d1": (_margenes(), "El molde de corte: márgenes, piquetes y la flecha del hilo."),
    "s08d3": (_tizada(), "Una buena tizada respeta el hilo y aprovecha el ancho de la tela."),
    "s08d5": (tarjetas([("Encabezado", "Marca, código, temporada, talles"), ("Geometral", "Frente, espalda y detalles"), ("Medidas", "De la prenda, con tolerancia"), ("Materiales", "Tela, forrería, entretela"), ("Avíos", "Tipo, color y cantidad"), ("Confección", "Costuras, terminaciones y etiquetas")], 3), "Las partes de una ficha técnica."),
    "s09d1": (_maquinas(), "Con estas tres máquinas se resuelve la mayor parte de la ropa."),
    "s09d3": (_dobladillos(), "Cuatro maneras de terminar un borde."),
    "s09d4": (matriz(["Lino y algodón", "Lana", "Seda y viscosa", "Poliéster y poliamida"], ["Temperatura", "Vapor", "Paño"], [["Alta", "Sí", "Opcional"], ["Media", "Sí", "Húmedo"], ["Baja a media", "Poco", "Sí"], ["Baja", "Poco", "Sí"]]), "Temperatura de planchado según la fibra. Probá siempre en un retazo."),
    "s09d5": (flujo(["Coser muestras", "Planchar", "Montar derecho y revés", "Etiquetar", "Fotografiar"]), "El armado del muestrario de costuras."),
    "s10d1": (flujo(["Tela de prueba parecida", "Cortar con márgenes amplios", "Marcar líneas", "Coser con puntada larga", "Probar en el cuerpo"]), "La prueba es para equivocarse barato."),
    "s10d2": (comparar(("Arrugas tirantes", ["Señalan tensión", "Falta tela donde apuntan", "Se agrega en el molde"]), ("Arrugas flojas o bolsas", ["Señalan exceso", "Sobra tela en esa zona", "Se quita o se profundiza una pinza"])), "Leer las arrugas para corregir el molde."),
    "s10d3": (flujo(["Preparar piezas", "Coser lo plano", "Unir piezas", "Cierres", "Bordes y pretina", "Ruedo", "Botones y etiquetas", "Planchado final"]), "El orden de armado evita descoser."),
    "s10d4": (tarjetas([("Medidas", "Dentro de la tolerancia"), ("Simetría", "Ambos lados iguales"), ("Costuras", "Rectas, sin saltos"), ("Terminaciones", "Sin hilachas"), ("Avíos", "Cierre que corre, botones firmes"), ("Etiquetas", "Presentes y correctas")], 3), "Los puntos clave del control de calidad."),
    "s10d5": (flujo(["Molde corregido", "Corte en tela definitiva", "Confección", "Control de calidad", "Fotos puesta y detalles"], destacar=2), "Del molde corregido al prototipo terminado."),
    "s11d1": (flujo(["Fibra", "Hilado", "Tejido", "Tintura y acabado", "Diseño y desarrollo", "Corte y confección", "Venta"], destacar=4), "La cadena textil: una marca de diseño se ubica sobre todo en el desarrollo y la venta."),
    "s11d2": (lista_check(["Visitar el taller", "Verificar registro y condiciones", "Pedir una muestra antes de producir", "Documentar dónde se hace cada prenda"], ["Precios que no cubren un salario digno", "Talleres que no se dejan visitar", "Producir sin muestra aprobada"], tsi="Hacé", tno="Desconfiá de"), "Producir con responsabilidad empieza por conocer el taller."),
    "s11d3": (barras([("Tela", 9000), ("Confección", 8000), ("Moldería y muestras", 3000), ("Cierre, botón e hilo", 1500), ("Etiquetas y bolsa", 900), ("Entretela", 800)], "$"), "Composición del costo de la falda de ejemplo, serie de 50. Valores ficticios."),
    "s11d4": (_simbolos(), "Los símbolos de cuidado; una cruz encima significa no."),
    "s11d5": (flujo(["Cantidades por talle", "Tela y avíos", "Proveedores y taller", "Cronograma", "Costos y precio", "Etiquetas"]), "Las partes del plan de producción."),
    "s12d1": (tarjetas([("Agua", "Cultivo y teñido"), ("Químicos", "Tinturas y acabados"), ("Energía", "Fibras y procesos"), ("Microplásticos", "Lavado de sintéticos"), ("Residuos", "Retazos y descarte"), ("Trabajo", "Condiciones en la cadena")], 3), "Los principales impactos de la industria de la indumentaria."),
    "s12d2": (matriz(["Algodón convencional", "Algodón orgánico", "Lino", "Lana", "Poliéster reciclado"], ["Agua", "Químicos", "Fin de vida"], [[0, 0, 2], [1, 2, 2], [2, 2, 2], [1, 1, 2], [2, 1, 0]], leyenda=("Más impacto", "Intermedio", "Menos impacto")), "Una mirada matizada: ningún material es perfecto. Más color, mejor desempeño relativo en ese aspecto (orientativo)."),
    "s12d3": (ciclo(["Diseñar para durar", "Usar mucho", "Reparar", "Reutilizar", "Reciclar"], "Diseño circular"), "Mantener las prendas y los materiales en uso el mayor tiempo posible."),
    "s12d4": (comparar(("Lavado verde", ["\"Prenda sustentable\"", "\"Producción ética\"", "\"Eco\""]), ("Honesto y verificable", ["Tela de saldo de una tejeduría local", "Taller cooperativo que visitamos", "100% algodón, sin mezclas"])), "Cambiar palabras vagas por datos concretos."),
    "s12d5": (flujo(["Mapa de impactos", "Materiales", "Estrategias por prenda", "Retazos", "Cuidado y reparación", "Comunicación honesta"]), "Las partes del plan circular."),
    "s13d1": (tarjetas([("Línea y mancha", "Fibra y color plano"), ("Collage", "Tela, recortes y dibujo"), ("Digital", "Tableta con texturas reales"), ("Mixta", "Mano escaneada y color digital")], 4), "Técnicas de ilustración de presentación."),
    "s13d2": (tarjetas([("Producto", "Prenda sola, fondo neutro"), ("Look", "Puesta, cuerpo entero"), ("Detalle", "Tela, costura, avío"), ("Campaña", "Escenario e historia")], 4), "Cuatro tipos de foto, cuatro usos."),
    "s13d3": (tarjetas([("Desfile", "Impacto y prensa"), ("Presentación estática", "Más accesible"), ("Showroom", "Compradores mayoristas"), ("Feria de diseño", "Venta directa"), ("Video corto", "Redes y tienda")], 5 if False else 3), "Formatos para presentar una colección."),
    "s13d4": (flujo(["Fotos", "Nombre y descripción", "Composición y cuidado", "Tabla de talles y medidas", "Precio y stock", "Políticas"]), "La ficha de producto completa reduce cambios y devoluciones."),
    "s13d5": (flujo(["Portada", "Concepto", "Seis looks", "Detalles", "Line-up", "Créditos"]), "La estructura del lookbook."),
    "s14d1": (flujo(["Boceto", "Geometral y ficha", "Moldería digital", "Prenda en 3D", "Lookbook"]), "Una herramienta para cada etapa de la colección."),
    "s14d2": (lista_check(["Ordenar observaciones", "Investigar historia de prendas", "Revisar fichas y cuentas"], ["Ver la calle de tu ciudad", "Saber cómo calza una prenda", "Garantizar normas y datos"], tsi="La IA ayuda a", tno="La IA no puede"), "Usar la IA con criterio."),
    "s14d3": (comparar(("Usos razonables", ["Explorar climas y paletas", "Variar una estampa propia", "Editar fotos reales de tus prendas"]), ("Usos problemáticos", ["Vender prendas que no existen", "Mostrar un calce irreal", "Copiar estampas o estilos ajenos"])), "La imagen generada sirve para pensar, no para engañar."),
    "s14d4": (flujo(["Moldes en 2D", "Avatar con medidas", "Costuras virtuales", "Propiedades de la tela", "Simulación"]), "Cómo se simula una prenda en 3D."),
    "s14d5": (flujo(["Investigación", "Concepto", "Bocetos", "Moldería", "Prototipo", "Ficha", "Producción", "Lookbook"]), "Tu flujo de trabajo, etapa por etapa."),
    "s15d1": (matriz(["Falda", "Campera", "Poncho"], ["Concepto", "Usuario", "Combina", "Se produce", "Precio"], [[2, 2, 2, 2, 2], [2, 2, 2, 1, 1], [2, 1, 2, 2, 1]]), "La tabla de revisión del ejemplo: dónde hay que ajustar antes de cerrar."),
    "s15d2": (comparar(("Ficha completa", ["Prenda prototipada", "Moldes y medidas por talle", "Consumo y orden de armado"]), ("Ficha resumida", ["Resto de la colección", "Geometral, tela y avíos", "Medidas principales"])), "Dos niveles de ficha, con su nivel de desarrollo indicado."),
    "s15d3": (barras([("Falda", 960000), ("Remera", 960000), ("Campera", 1100000)], "$"), "Inversión por prenda en el ejemplo de la colección. Valores ficticios."),
    "s15d4": (linea_tiempo([("Antes", "Contar el proceso, lista de interesados"), ("Lanzamiento", "Lookbook, tienda, feria"), ("Después", "Escuchar, mostrar en uso, reponer")]), "El plan de lanzamiento en tres momentos."),
    "s15d5": (flujo(["Portada", "Concepto", "Line-up", "Materiales", "Fichas", "Moldes", "Costos", "Plan circular"]), "El índice de la carpeta técnica."),
    "s16d1": (flujo(["Portada", "Concepto", "Proceso", "Desarrollo técnico", "Prototipo", "Producción", "Presentación"]), "La estructura de un proyecto en el portfolio."),
    "s16d2": (linea_tiempo([("0 a 1 min", "Quién sos"), ("1 a 3", "Usuario y concepto"), ("3 a 5", "Proceso"), ("5 a 7", "Colección"), ("7 a 9", "Prototipo y viabilidad"), ("9 a 10", "Cierre")]), "Una presentación de diez minutos."),
    "s16d3": (linea_tiempo([("0:00", "Toma que enganche"), ("0:10", "Concepto"), ("0:30", "Proceso"), ("0:55", "Colección"), ("1:20", "Cierre")]), "El guion del video de un minuto y medio."),
    "s16d4": (matriz(["Dibujo", "Concepto", "Colección", "Moldería", "Prototipo", "Producción", "Presentación"], ["Inicial", "Logrado", "Destacado"], [[0, 2, 0], [0, 2, 0], [0, 0, 2], [0, 2, 0], [0, 2, 0], [2, 0, 0], [0, 2, 0]], leyenda=None), "Ejemplo de autoevaluación: marcá tu nivel en cada criterio y trabajá primero los más flojos."),
    "s16d5": (flujo(["Carpeta técnica", "Lookbook", "Portfolio", "Video", "Fotos del prototipo", "Figurines: antes y hoy"]), "Los seis elementos de la entrega final."),
}
