"""Gráficos adicionales del curso de Interiores y Mobiliario (uno por clase que no tenía)."""
from figlib import *

def _percentiles():
    b = []; pts = []
    for i in range(121):
        x = -3 + 6 * i / 120; pts.append((60 + 520 * i / 120, 170 - 130 * math.exp(-x * x / 2)))
    b.append(f'<path d="M{pts[0][0]} 170' + "".join(f'L{x:.1f} {y:.1f}' for x, y in pts) + f'L580 170Z" fill="{P["tint"]}" stroke="{P["acc"]}" stroke-width="2.5"/>')
    b.append(f'<path d="M40 170H600" stroke="{P["dark"]}" stroke-width="1.5"/>')
    for z, lab, sub in ((-1.645, "P5", "Alcance: que llegue el más bajo"), (0, "P50", "El promedio"), (1.645, "P95", "Paso: que entre el más grande")):
        x = 60 + 520 * (z + 3) / 6; y = 170 - 130 * math.exp(-z * z / 2)
        b.append(f'<path d="M{x:.1f} 170V{y:.1f}" stroke="{P["dark"]}" stroke-width="2" stroke-dasharray="{"" if z else "4 4"}"/>')
        b.append(text(x, 192, lab, 14, 700, P["acc"])); b.append(text(x, 212 + 7.5 * (len(wrap(sub, 16)) - 1), sub, 12.5, 600, P["ink"], n=16, lh=15))
    return raw(256, "".join(b), "Curva de distribución de la altura de las personas con los percentiles 5, 50 y 95: el 5 rige el alcance y el 95 los pasos")

def _livings():
    b = []; d, a, t = P["dark"], P["acc"], P["tint"]
    labs = ["En U o en C", "Enfrentada", "En L", "Lineal"]
    for i, lab in enumerate(labs):
        x = 20 + i * 155
        b.append(f'<rect x="{x}" y="14" width="140" height="150" rx="12" fill="#FFFFFF" stroke="{P["soft"]}" stroke-width="1.5"/>')
        b.append(text(x + 70, 188, lab, 13, 700))
    S = lambda x, y, w, h: f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{t}" stroke="{d}" stroke-width="2"/>'
    M = lambda x, y, w, h: f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{a}"/>'
    # U
    b.append(S(46, 32, 88, 26) + S(34, 66, 24, 44) + S(122, 66, 24, 44) + M(70, 74, 40, 26))
    # enfrentada
    b.append(S(201, 32, 88, 26) + S(201, 120, 88, 26) + M(225, 76, 40, 26))
    # L
    b.append(S(356, 32, 92, 26) + S(356, 58, 26, 64) + M(398, 76, 40, 26))
    # lineal
    b.append(f'<rect x="510" y="30" width="60" height="8" fill="{d}"/>' + S(500, 112, 80, 26) + M(520, 80, 40, 20))
    b.append(text(540, 26, "TV", 10, 700, P["dark"]))
    return raw(202, "".join(b), "Plantas esquemáticas de cuatro zonas de estar: en U alrededor de la mesa ratona, dos sillones enfrentados, sillón en L y todo mirando hacia la TV")

def _cocina():
    b = []; d, a, t = P["dark"], P["acc"], P["tint"]; k = 100  # px por m
    y0 = 250  # piso
    b.append(f'<path d="M40 {y0}H420" stroke="{d}" stroke-width="2.5"/>')
    b.append(f'<rect x="60" y="{y0 - 0.90 * k}" width="320" height="{0.90 * k - 0.12 * k:.0f}" fill="{t}" stroke="{d}" stroke-width="2"/>')
    b.append(f'<rect x="60" y="{y0 - 0.90 * k - 6}" width="320" height="6" fill="{a}"/>')
    b.append(f'<rect x="70" y="{y0 - 0.12 * k}" width="300" height="{0.12 * k}" fill="{P["soft"]}"/>')
    b.append(f'<rect x="60" y="{y0 - 2.15 * k}" width="320" height="{(2.15 - 1.50) * k:.0f}" fill="{t}" stroke="{d}" stroke-width="2"/>')
    for x in (140, 220, 300): b.append(f'<path d="M{x} {y0 - 0.90 * k}V{y0 - 0.12 * k}M{x} {y0 - 2.15 * k}V{y0 - 1.50 * k}" stroke="{d}" stroke-width="1.2"/>')
    def cota(x, ya, yb, lab):
        b.append(f'<path d="M{x} {ya}V{yb}M{x - 5} {ya}h10M{x - 5} {yb}h10" stroke="{a}" stroke-width="1.6"/>')
        b.append(text(x + 12, (ya + yb) / 2 + 4, lab, 12.5, 700, P["dark"], "start"))
    cota(400, y0, y0 - 0.90 * k, "Mesada: 0,90 m")
    cota(400, y0 - 0.96 * k, y0 - 1.50 * k, "Libre: 0,55 a 0,65 m")
    cota(400, y0 - 1.50 * k, y0 - 2.15 * k, "Alacena hasta 2,10 a 2,20 m")
    b.append(text(36, y0 + 20, "Zócalo 0,10 a 0,15 m", 12, 600, P["ink"], "start"))
    return raw(276, "".join(b), "Vista de una cocina con sus alturas de referencia: mesada a 0,90 metros, espacio libre de 0,55 a 0,65 metros hasta la alacena y alacena que llega a 2,10 a 2,20 metros")

def _cortina():
    b = []; d, a, t = P["dark"], P["acc"], P["tint"]
    b.append(f'<path d="M40 20H600M40 250H600" stroke="{d}" stroke-width="2"/>')
    b.append(text(44, 14, "Techo", 11.5, 600, P["ink"], "start")); b.append(text(44, 268, "Piso", 11.5, 600, P["ink"], "start"))
    b.append(f'<rect x="230" y="80" width="180" height="120" fill="#FFFFFF" stroke="{d}" stroke-width="2.5"/><path d="M320 80V200" stroke="{d}"/>')
    b.append(f'<path d="M180 36H460" stroke="{a}" stroke-width="5" stroke-linecap="round"/>')
    for x0 in (184, 412):
        b.append(f'<path d="M{x0} 40' + "".join(f'q6 105 {(-1) ** k * 0 + 8} 209' if False else '' for k in range(1)) + '"/>')
        for k in range(6):
            b.append(f'<path d="M{x0 + k * 8} 40V249" stroke="{P["soft"]}" stroke-width="3"/>')
    def cota_h(x1, x2, y, lab):
        b.append(f'<path d="M{x1} {y}H{x2}M{x1} {y - 5}v10M{x2} {y - 5}v10" stroke="{a}" stroke-width="1.6"/>')
        b.append(text((x1 + x2) / 2, y - 8, lab, 12, 700, P["dark"]))
    cota_h(180, 230, 70, "15 a 30 cm"); cota_h(410, 460, 70, "15 a 30 cm")
    b.append(text(520, 120, "Barral más arriba", 12.5, 700, P["dark"], "start")); b.append(text(520, 138, "del marco, cerca", 12.5, 400, P["ink"], "start")); b.append(text(520, 156, "del techo", 12.5, 400, P["ink"], "start"))
    b.append(text(520, 210, "Tela que roza", 12.5, 700, P["dark"], "start")); b.append(text(520, 228, "el piso", 12.5, 400, P["ink"], "start"))
    return raw(276, "".join(b), "Vista de una ventana con su cortina: el barral cerca del techo, sobrepasando la ventana de 15 a 30 centímetros por lado, y la tela llegando al piso")

def _kelvin():
    b = ['<defs><linearGradient id="gk" x1="0" x2="1"><stop offset="0" stop-color="#FFB25B"/><stop offset=".45" stop-color="#FFF1D6"/><stop offset="1" stop-color="#CFE3FF"/></linearGradient></defs>']
    b.append(f'<rect x="40" y="40" width="560" height="40" rx="10" fill="url(#gk)" stroke="{P["soft"]}"/>')
    for x, lab in ((40, "2.700 K"), (190, "3.500 K"), (290, "4.000 K"), (440, "5.000 K"), (600, "6.500 K")):
        b.append(f'<path d="M{x} 80v10" stroke="{P["dark"]}"/>' + text(x, 106, lab, 12, 700, P["dark"], "start" if x == 40 else "end" if x == 600 else "middle"))
    for x, t1, t2 in ((110, "Cálida", "Living, dormitorio, comedor"), (320, "Neutra", "Cocina, baño, trabajo"), (520, "Fría", "Talleres y oficinas")):
        b.append(text(x, 140, t1, 14, 700)); b.append(text(x, 160, t2, 12.5, 500, P["ink"]))
    b.append(text(320, 28, "Temperatura de color", 14, 700))
    return raw(176, "".join(b), "Escala de temperatura de color de 2.700 a 6.500 kelvin: cálida para living y dormitorio, neutra para cocina y baño, fría para talleres y oficinas")

def _fugas():
    b = []; d, a = P["dark"], P["acc"]
    b.append(f'<path d="M20 90H620" stroke="{P["soft"]}" stroke-width="1.5" stroke-dasharray="6 5"/>' + text(590, 78, "Horizonte: altura de los ojos", 12, 600, P["ink"], "end"))
    F1, F2 = (40, 90), (600, 90); top, bot = (300, 40), (300, 210)
    b.append(f'<circle cx="{F1[0]}" cy="90" r="5" fill="{a}"/><circle cx="{F2[0]}" cy="90" r="5" fill="{a}"/>')
    b.append(text(40, 112, "F1", 12, 700, P["acc"])); b.append(text(600, 112, "F2", 12, 700, P["acc"]))
    def on(p, F, t): return (p[0] + (F[0] - p[0]) * t, p[1] + (F[1] - p[1]) * t)
    tl, bl = on(top, F1, .42), on(bot, F1, .42); tr, br = on(top, F2, .38), on(bot, F2, .38)
    for p, F in ((top, F1), (bot, F1), (top, F2), (bot, F2)):
        b.append(f'<path d="M{p[0]} {p[1]}L{F[0]} {F[1]}" stroke="{P["soft"]}" stroke-width="1"/>')
    b.append(f'<path d="M{top[0]} {top[1]}L{tl[0]:.1f} {tl[1]:.1f}L{bl[0]:.1f} {bl[1]:.1f}L{bot[0]} {bot[1]}Z" fill="{P["tint"]}" stroke="{d}" stroke-width="2.5"/>')
    b.append(f'<path d="M{top[0]} {top[1]}L{tr[0]:.1f} {tr[1]:.1f}L{br[0]:.1f} {br[1]:.1f}L{bot[0]} {bot[1]}Z" fill="{P["soft"]}" opacity=".55" stroke="{d}" stroke-width="2.5"/>')
    b.append(f'<path d="M300 40V210" stroke="{d}" stroke-width="3.5"/>')
    b.append(text(300, 232, "Arista vertical más cercana", 12.5, 700))
    return raw(244, "".join(b), "Un volumen dibujado en perspectiva con dos puntos de fuga sobre la línea de horizonte; las aristas horizontales fugan hacia los dos puntos y las verticales se mantienen verticales")

FIGS = {
    "s01d1": (flujo(["Escuchar", "Relevar", "Proponer", "Documentar", "Presentar"]), "Las cinco etapas del trabajo de un interiorista."),
    "s01d4": (tarjetas([("Mové el brazo", "No la muñeca"), ("Mirá adónde vas", "No la punta del lápiz"), ("Pasadas en el aire", "Antes de apoyar"), ("Un solo trazo", "Líneas largas, sin repasar")], 2), "Cuatro hábitos para dibujar suelto y con proporción."),
    "s01d5": (lista_check(["Foto de frente, con buena luz", "Líneas que se distinguen", "Título y escala en cada dibujo"], ["Foto torcida o con sombras", "Todas las líneas iguales", "Dibujos sin escala"]), "Qué mira la primera corrección."),
    "s02d5": (tarjetas([("Coherencia de medidas", "Las cotas suman"), ("Jerarquía de líneas", "Muros gruesos, detalles finos"), ("Símbolos correctos", "Puertas y ventanas"), ("Cotas legibles", "Ordenadas por fuera"), ("Rótulo", "Completo, con escala 1:50")], 3), "Los cinco criterios de la planta acotada."),
    "s03d1": (_percentiles(), "Diseñar es decidir a quién dejás afuera: por eso se mira el percentil que corresponde."),
    "s03d5": (flujo(["Planta del ambiente", "Zonas por uso", "Recorrido principal", "Pasos libres", "Correcciones"]), "Cómo se arma el diagrama de zonas y recorridos."),
    "s04d3": (tarjetas([("Equilibrio", "Simétrico, asimétrico o radial"), ("Punto focal", "Cada ambiente necesita uno"), ("Ritmo", "Repetición con intención"), ("Jerarquía", "Qué se ve primero")], 2), "Los cuatro principios de composición aplicados a un ambiente."),
    "s04d4": (tarjetas([("Punto focal", "Cambiar hacia dónde mira"), ("Orientación", "Girar el eje del ambiente"), ("Agrupación", "Juntar o separar zonas"), ("Recorrido", "Cambiar por dónde se pasa")], 2), "Cuatro palancas para generar alternativas realmente distintas."),
    "s04d5": (matriz(["Alternativa A", "Alternativa B", "Alternativa C"], ["Recorridos", "Punto focal", "Luz natural", "Guardado"], [[2, 1, 2, 1], [1, 2, 2, 2], [2, 2, 1, 1]]), "Ejemplo de tabla de evaluación de tres distribuciones."),
    "s05d1": (_livings(), "Las cuatro tipologías de zona de estar. Para conversar, nadie a más de 2,50 a 3 m."),
    "s05d5": (lista_check(["Muebles en medida real", "Pasos libres", "Espacio para correrse de la mesa", "Zonas claras"], ["Muebles achicados para que entren", "Sillas contra la pared", "Recorridos que cruzan la zona de estar"]), "Qué mira la corrección del living-comedor."),
    "s06d2": (_cocina(), "Alturas de referencia de una cocina. Siempre verificá con la ficha técnica de cada artefacto."),
    "s06d4": (tarjetas([("Lavarropas", "Agua, desagüe y enchufe"), ("Pileta de lavar", "Con agua caliente"), ("Tender", "Lugar ventilado"), ("Guardado", "Productos y escobas"), ("Mesada", "Para doblar"), ("Ubicación", "Cerca de la cocina")], 3), "Lo que necesita un lavadero que funcione."),
    "s06d5": (comparar(("Cocina", ["Planta con módulos y artefactos", "Vistas acotadas de las mesadas", "Instalaciones ubicadas", "Medidas reales de los modelos"]), ("Baño", ["Planta con artefactos y pasos", "Vistas de los revestimientos", "Puerta que no choca", "Medidas reales de los modelos"])), "Las dos plantas de la entrega."),
    "s07d3": (tarjetas([("Dormitorios", "Tonos suaves que calman"), ("Cocina y comedor", "Cálidos que invitan"), ("Estudio", "Neutros que concentran"), ("Baño", "Claros y limpios"), ("Infantiles", "Base neutra, color en detalles"), ("Techo", "La quinta pared")], 3), "El color según el uso. Siempre se prueba en el lugar."),
    "s07d5": (barras([("Color dominante", 60), ("Color secundario", 30), ("Acento", 10)], "%"), "La regla 60-30-10: una guía para repartir la paleta en el ambiente."),
    "s08d1": (flujo(["¿Cuánto tránsito?", "¿Se moja?", "¿Quién lo usa?", "Formato y dirección", "Comprar todo junto"]), "Las preguntas para elegir un piso. Sumá el desperdicio al comprar."),
    "s08d2": (escala("Mate", "Brillante", [(0.1, "Mate: disimula imperfecciones"), (0.5, "Satinada: lavable, leve brillo"), (0.9, "Brillante: marca cada defecto")], titulo="Terminación de la pintura"), "Rendimiento de referencia: 8 a 12 m² por litro por mano, y en general dos manos."),
    "s08d3": (_cortina(), "Tres reglas que mejoran cualquier ventana. El ancho de tela, entre 1,5 y 2,5 veces el barral."),
    "s08d4": (comparar(("Moodboard de clima", ["Cómo se va a sentir", "Una palabra guía", "Pocas imágenes, con jerarquía", "La paleta visible"]), ("Muestrario de materiales", ["Con qué se va a construir", "Materiales reales", "Muestras en su proporción", "Etiquetadas con proveedor"])), "Dos piezas que trabajan juntas."),
    "s08d5": (tarjetas([("Coherencia", "Clima y materiales hablan igual"), ("Paleta", "Visible y acotada"), ("Muestrario", "Materiales reales"), ("Jerarquía", "Algo manda"), ("Uso", "Materiales adecuados")], 3), "Los criterios de la corrección del moodboard."),
    "s09d1": (_kelvin(), "En un mismo ambiente, no mezcles temperaturas de color."),
    "s09d3": (escala("Haz estrecho", "Haz abierto", [(0.12, "10° a 25°: acentuar un cuadro"), (0.5, "30° a 40°: bañar una zona"), (0.88, "Más de 60°: luz general")], titulo="Ángulo de apertura"), "El ángulo de apertura define si la luz acentúa o ilumina en general."),
    "s09d4": (barras([("Pasillos", 100), ("Living, general", 200), ("Comedor, sobre la mesa", 300), ("Lectura", 500), ("Mesada de cocina", 500), ("Espejo del baño", 500)], "lx", maxv=520), "Valores máximos de los rangos orientativos de iluminancia de cada lugar."),
    "s09d5": (tarjetas([("Capas", "General, de tarea y de acento"), ("Ubicación", "Luminarias bien ubicadas"), ("Interruptores", "Donde se entra"), ("Tabla de referencias", "Tipo, lúmenes y cantidad"), ("Temperatura", "Una por ambiente")], 3), "Lo que lleva el plano de iluminación."),
    "s10d1": (flujo(["Tablero", "Termomagnética", "Diferencial", "Puesta a tierra", "Circuitos y bocas"]), "Las partes básicas de una instalación eléctrica: la termomagnética protege la instalación; el diferencial, a las personas. La ejecuta siempre un electricista matriculado."),
    "s10d3": (comparar(("Agua", ["Llega a presión", "Se puede mover con más libertad", "Caliente: termotanque o calefón", "Cañerías finas"]), ("Desagüe", ["Funciona por gravedad", "Necesita pendiente", "Inodoro: caño de 110 mm", "En departamentos, las montantes no se mueven"])), "Por qué el agua se mueve fácil y el desagüe no. Gas y agua los ejecutan siempre matriculados."),
    "s10d4": (tarjetas([("Ventilación cruzada", "Aberturas enfrentadas"), ("Extractor y campana", "Baños y cocina"), ("Unidad interior", "Que no apunte a la cama"), ("Unidad exterior", "Con acceso y sin molestar"), ("Desagote", "Previsto desde el proyecto")], 3), "Ventilación y clima, pensados desde el plano."),
    "s10d5": (tarjetas([("Bocas", "Donde se usan"), ("Comandos", "En la entrada de cada ambiente"), ("Uso especial", "Horno, lavarropas, termotanque"), ("Aire acondicionado", "Boca y desagote"), ("Leyenda", "Símbolos explicados")], 3), "Lo que lleva el plano de instalaciones."),
    "s11d1": (flujo(["La necesidad", "El lugar", "La tipología", "El boceto", "La definición", "La documentación"]), "El proceso de un mueble a medida."),
    "s11d2": (barras([("Libros comunes", 30), ("Vinilos", 35), ("Rack de TV", 50), ("Ropa doblada", 60), ("Ropa colgada", 60)], "cm", maxv=62), "Profundidad útil de guardado, valores máximos de referencia."),
    "s11d3": (comparar(("Madera maciza", ["Pino, eucalipto, paraíso, guatambú, cedro", "Calidez y veta", "Se mueve con la humedad", "Más cara"]), ("Placas", ["Aglomerado y MDF", "Medidas estables", "Melamina o enchapado", "El MDF se puede laquear"])), "Madera maciza y placas: elegir según uso y presupuesto."),
    "s11d4": (tarjetas([("Tornillo para aglomerado", "Simple y económico"), ("Tarugo", "Alinea y refuerza"), ("Excéntrico (minifix)", "Se arma y desarma"), ("Encastre y espiga", "En madera maciza"), ("Cola de milano", "Cajones de calidad"), ("Bisagras de cazoleta", "Con cierre suave")], 3), "Uniones y herrajes: los que más se notan en el uso diario."),
    "s11d5": (tarjetas([("Necesidad", "Resuelta con cantidades"), ("Medidas ergonómicas", "Alturas y profundidades"), ("Materiales y espesores", "Especificados"), ("Herrajes", "Tipo y cantidad")], 2), "Lo que mira la corrección del mueble a medida."),
    "s12d2": (tarjetas([("Laterales", "Altura total"), ("Techo y base", "Entre laterales"), ("Estantes", "Con su descuento"), ("Divisiones", "Verticales internas"), ("Fondo", "Placa fina"), ("Frentes y cajones", "Con luz de apertura")], 3), "Las piezas de un despiece."),
    "s12d4": (flujo(["Planta de ubicación", "Vistas", "Cortes", "Detalles", "Despiece", "Especificaciones", "Notas"]), "El orden del legajo para el carpintero."),
    "s12d5": (lista_check(["Despiece coherente con las vistas", "Descuentos de espesores aplicados", "Placas optimizadas", "Especificaciones y notas completas"], ["Medidas que no suman", "Tapacantos sin indicar", "Herrajes sin especificar"]), "Qué mira la corrección del plano de taller."),
    "s13d3": (_fugas(), "Perspectiva con dos puntos de fuga: ideal para mostrar esquinas y muebles."),
    "s13d4": (piramide(["Título e imagen principal", "Planta, vistas y cortes", "Paleta, materiales, textos y rótulo"]), "La jerarquía de la lámina de presentación."),
    "s13d5": (comparar(("Perspectiva", ["Del living", "Con proporciones correctas", "Materiales y luz sugeridos"]), ("Lámina", ["Imagen principal clara", "Planta y paleta", "Textos breves", "Coherencia con el proyecto"])), "Las dos piezas de la entrega."),
    "s14d1": (tarjetas([("SketchUp", "Modelado 3D más usado"), ("Sweet Home 3D", "Gratuito, plantas y 3D"), ("Planner 5D", "Rápido, con funciones de IA")], 3), "Opciones para pasar del papel al 3D."),
    "s14d2": (lista_check(["Usar la propuesta como punto de partida", "Verificar medidas y pasos", "Corregir lo que no funciona"], ["Aceptar la distribución sin revisar", "Subir planos de clientes sin permiso", "Olvidar para quién es el proyecto"], tsi="Hacé", tno="Evitá"), "La IA propone; el criterio es tuyo."),
    "s14d3": (tarjetas([("Materiales", "Con textura y escala real"), ("Luz natural", "Hora y orientación creíbles"), ("Luces artificiales", "Las del plano"), ("Cámara", "A la altura de los ojos")], 2), "Los cuatro ajustes de un render creíble."),
    "s14d4": (flujo(["Contexto", "Tarea concreta", "Restricciones", "Formato"]), "La estructura de un buen pedido a la IA."),
    "s14d5": (tarjetas([("Modelo 3D", "Del living"), ("Render", "Una imagen realista"), ("Imagen con IA", "Una exploración"), ("Reflexión", "Qué aportó cada herramienta")], 2), "Lo que lleva la entrega."),
    "s15d2": (flujo(["Matriz de relaciones", "Diagrama de burbujas", "Recorridos", "Tres alternativas", "Tabla de evaluación"]), "De las relaciones entre ambientes a la distribución elegida."),
    "s15d3": (comparar(("Conviene comprar", ["Sillón, sillas, cama, colchón", "Mesa estándar", "Luminarias", "Electrodomésticos"]), ("Conviene diseñar a medida", ["Guardado de pared completa", "Nichos y medidas especiales", "Muebles con varias funciones", "Escritorio integrado a biblioteca"])), "Comprar, conservar o diseñar: una decisión de función, presupuesto y tiempo."),
    "s15d4": (tarjetas([("Paleta general", "Común a toda la casa"), ("Pisos", "El mismo piso da unidad"), ("Moodboard y muestrario", "Un solo clima"), ("Iluminación", "Capas en cada ambiente")], 2), "Un criterio común para todo el departamento."),
    "s15d5": (tarjetas([("Programa cumplido", "Todo lo que pidió el cliente"), ("Distribución", "Funciona y se recorre"), ("Mueble principal", "Diseñado y medido"), ("Coherencia", "Un solo proyecto"), ("Claridad", "Se entiende sin explicar")], 3), "Los criterios de la corrección del anteproyecto."),
    "s16d1": (flujo(["Listar correcciones", "Clasificar: errores, mejoras, criterio", "Evaluar el impacto", "Corregir en orden", "Registrar los cambios"]), "Cómo incorporar correcciones sin romper el proyecto."),
    "s16d2": (tarjetas([("Una idea por plano", "Sin mezclar"), ("Coherencia", "Lo mismo en todos los planos"), ("Rótulos completos", "En cada lámina"), ("Notas generales", "Lo que vale para todo")], 2), "Documentar: técnico, preciso y sin adornos. Lo que no está en el plano, no existe."),
    "s16d3": (flujo(["Paredes: 52 m²", "Sin aberturas: 44 m²", "÷ 10 m² por litro", "× 2 manos", "8,8 litros"], destacar=4), "Ejemplo de cómputo de pintura de un living de 6 × 4 m y 2,60 m de alto: 20 m de perímetro por 2,60 m dan 52 m² de paredes."),
    "s16d4": (flujo(["Contar una historia", "De lo general a lo particular", "Hablar su idioma", "Mostrar alternativas", "Escuchar", "Próximos pasos"]), "El orden de una presentación al cliente."),
    "s16d5": (tarjetas([("Programa cumplido", "Lo que pidió el cliente"), ("Documentación", "Completa y coherente"), ("Presupuesto", "Por rubros"), ("Presentación", "Clara y ordenada"), ("Calidad general", "Prolijidad en todo")], 3), "Lo que mira la entrega final."),
}
