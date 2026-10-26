"""Gráficos adicionales del curso de Diseño Industrial (uno por clase que no tenía)."""
from figlib import *

def _trazos():
    b = []; d = P["dark"]
    for i, lab in enumerate(["Rectas largas", "Elipses", "Curvas en S"]):
        x = 20 + i * 205
        b.append(f'<rect x="{x}" y="14" width="190" height="150" rx="12" fill="#FFFFFF" stroke="{P["soft"]}" stroke-width="1.5"/>')
        b.append(text(x + 95, 188, lab, 13, 700))
    for k in range(6):
        y = 38 + k * 20
        b.append(f'<circle cx="40" cy="{y}" r="3" fill="{P["acc"]}"/><circle cx="190" cy="{y + 6}" r="3" fill="{P["acc"]}"/>')
        b.append(f'<path d="M40 {y}L190 {y + 6}" stroke="{d}" stroke-width="{1.4 + (k % 2)}" stroke-linecap="round"/>')
    for k in range(5):
        b.append(f'<ellipse cx="320" cy="{40 + k * 24}" rx="{30 + k * 10}" ry="{6 + k * 2}" fill="none" stroke="{d}" stroke-width="1.6"/>')
    b.append(f'<path d="M320 34V140" stroke="{P["acc"]}" stroke-dasharray="4 4"/>')
    for k in range(4):
        b.append(f'<path d="M{450 + k * 10} 140c0-40 60-30 60-70s-30-40-20-40" fill="none" stroke="{d}" stroke-width="1.8" stroke-linecap="round" opacity="{1 - k * .2}"/>')
    return raw(200, "".join(b), "Tres ejercicios de calentamiento: rectas largas entre dos puntos, elipses apiladas sobre un eje y curvas en S repetidas")

def _materiales():
    b = []; g1, g2, g3 = "#D7DAE0", "#A9AFBA", "#6B7280"
    labs = ["Plástico mate", "Plástico brillante", "Metal cromado", "Madera"]
    for i, lab in enumerate(labs):
        x = 20 + i * 155; cx = x + 70
        b.append(f'<rect x="{x}" y="14" width="140" height="150" rx="14" fill="{P["tint"]}"/>')
        b.append(text(cx, 188, lab, 13, 700))
    # mate: degradé suave
    b.append(f'<defs><linearGradient id="gm" x1="0" x2="1"><stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/></linearGradient>'
             f'<linearGradient id="gb" x1="0" x2="1"><stop offset="0" stop-color="{P["soft"]}"/><stop offset=".6" stop-color="{P["acc"]}"/><stop offset="1" stop-color="{P["dark"]}"/></linearGradient>'
             f'<linearGradient id="gc" x1="0" x2="1"><stop offset="0" stop-color="#FFF"/><stop offset=".25" stop-color="{g3}"/><stop offset=".45" stop-color="#F3F4F6"/><stop offset=".7" stop-color="#374151"/><stop offset="1" stop-color="{g2}"/></linearGradient></defs>')
    for i, gid in enumerate(("gm", "gb", "gc")):
        cx = 90 + i * 155
        b.append(f'<path d="M{cx - 34} 46v84a34 9 0 0 0 68 0v-84" fill="url(#{gid})"/><ellipse cx="{cx}" cy="46" rx="34" ry="9" fill="#F3F4F6" stroke="{g2}"/>')
    b.append(f'<rect x="74" y="60" width="6" height="64" rx="3" fill="#FFF" opacity=".95"/>'.replace('x="74"', 'x="235"'))
    cx = 555
    b.append(f'<path d="M{cx - 34} 46v84a34 9 0 0 0 68 0v-84" fill="#C99A6B"/><ellipse cx="{cx}" cy="46" rx="34" ry="9" fill="#E3C29B" stroke="#A97A4F"/>')
    for k in range(5):
        b.append(f'<path d="M{cx - 26 + k * 13} 58q{6 - k % 2 * 10} 36 0 76" stroke="#8B5E34" stroke-width="1.4" fill="none"/>')
    b.append(f'<ellipse cx="{cx}" cy="46" rx="18" ry="4.5" fill="none" stroke="#A97A4F"/>')
    return raw(202, "".join(b), "Un mismo cilindro en cuatro materiales: plástico mate con degradé suave, plástico brillante con un reflejo blanco, metal cromado con franjas de alto contraste y madera con vetas")

def _percentiles():
    b = []; pts = []
    for i in range(121):
        x = -3 + 6 * i / 120; pts.append((60 + 520 * i / 120, 170 - 130 * math.exp(-x * x / 2)))
    b.append(f'<path d="M{pts[0][0]} 170' + "".join(f'L{x:.1f} {y:.1f}' for x, y in pts) + f'L580 170Z" fill="{P["tint"]}" stroke="{P["acc"]}" stroke-width="2.5"/>')
    b.append(f'<path d="M40 170H600" stroke="{P["dark"]}" stroke-width="1.5"/>')
    for z, lab, sub in ((-1.645, "P5", "Alcance: que llegue"), (0, "P50", "El promedio: no sirve solo"), (1.645, "P95", "Holgura: que entre")):
        x = 60 + 520 * (z + 3) / 6; y = 170 - 130 * math.exp(-z * z / 2)
        b.append(f'<path d="M{x:.1f} 170V{y:.1f}" stroke="{P["dark"]}" stroke-width="2" stroke-dasharray="{"" if z else "4 4"}"/>')
        b.append(text(x, 192, lab, 14, 700, P["acc"])); b.append(text(x, 212 + 7.5 * (len(wrap(sub, 14)) - 1), sub, 12.5, 600, P["ink"], n=14, lh=15))
    return raw(256, "".join(b), "Curva de distribución de una medida del cuerpo con los percentiles 5, 50 y 95 marcados: el 5 rige el alcance y el 95 la holgura")

def _controles():
    b = []; s = 2.6; cy = 86  # px por mm
    b.append(f'<circle cx="90" cy="{cy}" r="{6 * s}" fill="{P["acc"]}"/><circle cx="{90 + 17 * s:.1f}" cy="{cy}" r="{6 * s}" fill="{P["acc"]}"/>')
    b.append(f'<path d="M{90 - 6 * s:.1f} {cy + 26}h{12 * s:.1f}" stroke="{P["dark"]}" stroke-width="1.5"/>' + text(90, cy + 44, "12 mm", 12.5, 700))
    b.append(f'<path d="M{90 + 6 * s:.1f} {cy - 26}h{5 * s:.1f}" stroke="{P["dark"]}" stroke-width="1.5"/>' + text(90 + 8.5 * s, cy - 34, "5 mm", 12.5, 700))
    b.append(text(112, 190, "Botones: 10 a 12 mm o más,", 12.5, 600, P["ink"])); b.append(text(112, 208, "separados al menos 5 mm", 12.5, 600, P["ink"]))
    for d, x in ((15, 330), (40, 470)):
        r = d * s / 2; n = 16 if d == 40 else 8
        b.append(f'<circle cx="{x}" cy="{cy}" r="{r}" fill="{P["tint"]}" stroke="{P["dark"]}" stroke-width="2"/>')
        for k in range(n):
            a = 2 * math.pi * k / n
            b.append(f'<path d="M{x + (r - 5) * math.cos(a):.1f} {cy + (r - 5) * math.sin(a):.1f}L{x + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}" stroke="{P["dark"]}" stroke-width="1.5"/>')
        b.append(f'<path d="M{x} {cy}V{cy - r + 7:.0f}" stroke="{P["acc"]}" stroke-width="3" stroke-linecap="round"/>')
        b.append(text(x, 158, f"{d} mm", 12.5, 700))
    b.append(text(400, 190, "Perillas: de 15 a 40 mm,", 12.5, 600, P["ink"])); b.append(text(400, 208, "según la fuerza que pidan", 12.5, 600, P["ink"]))
    return raw(222, "".join(b), "Botones y perillas dibujados en proporción: botón de 12 milímetros con 5 de separación, y perillas estriadas de 15 y 40 milímetros")

def _lineas():
    b = []; d = P["dark"]
    filas = [("Continua gruesa", "Aristas visibles", f'stroke-width="3.2"'), ("Continua fina", "Cotas y auxiliares", f'stroke-width="1.4"'),
             ("De trazos", "Aristas ocultas", f'stroke-width="1.8" stroke-dasharray="10 5"'), ("Trazo y punto fina", "Ejes", f'stroke-width="1.4" stroke-dasharray="18 4 2 4"')]
    for i, (lab, uso, st) in enumerate(filas):
        y = 34 + i * 40
        b.append(f'<path d="M30 {y}H230" stroke="{d}" {st}/>')
        b.append(text(250, y + 5, lab, 13, 700, P["dark"], "start")); b.append(text(430, y + 5, uso, 12.5, 500, P["ink"], "start"))
    y = 34 + 4 * 40
    b.append(f'<path d="M30 {y}H58" stroke="{d}" stroke-width="3.2"/><path d="M62 {y}H200" stroke="{d}" stroke-width="1.4" stroke-dasharray="18 4 2 4"/><path d="M202 {y}H230" stroke="{d}" stroke-width="3.2"/>')
    b.append(text(250, y + 5, "Trazo y punto, gruesa en extremos", 13, 700, P["dark"], "start")); b.append(text(500, y + 5, "Plano de corte", 12.5, 500, P["ink"], "start"))
    return raw(214, "".join(b), "Los cinco tipos de línea normalizados: continua gruesa, continua fina, de trazos, trazo y punto fina, y trazo y punto con extremos gruesos")

FIGS = {
    "s01d2": (_trazos(), "Calentamiento: mové el brazo, no la muñeca, y girá la hoja para trazar cómodo."),
    "s01d5": (tarjetas([("Calidad de línea", "Trazos seguros, sin repasar"), ("Jerarquía", "Contorno grueso, detalle fino"), ("Perspectiva", "Líneas que fugan al mismo punto"), ("Elipses", "Simétricas y sobre su eje"), ("Composición", "La hoja ordenada, con aire")], 3), "Los cinco criterios de la corrección de la planilla."),
    "s02d4": (_materiales(), "Con dos o tres grises y un blanco ya se distingue el material."),
    "s02d5": (tarjetas([("Vista principal", "Grande, en perspectiva"), ("Dos vistas secundarias", "Más chicas, que se superponen un poco"), ("Notas cortas", "Uso y detalles"), ("Título", "Qué es el objeto")], 2), "Las partes de la lámina de boceto."),
    "s03d1": (_percentiles(), "Diseñar para el promedio es un error clásico: cada medida tiene su percentil."),
    "s03d2": (tarjetas([("De fuerza", "Toda la mano rodea el mango: martillo, sartén"), ("De precisión", "Dedos y pulgar: lápiz, destornillador fino"), ("De pinza", "Punta de dedos: una perilla chica"), ("De gancho", "Dedos doblados: una manija de bolsa")], 2), "Los cuatro agarres básicos. Para un agarre de fuerza, un diámetro cómodo está entre 3 y 5 cm."),
    "s03d3": (_controles(), "Tamaños mínimos de referencia: más grandes si se usan con guantes o por personas mayores."),
    "s03d4": (tarjetas([("Adaptaciones caseras", "Lo que la gente agrega o arregla"), ("Errores repetidos", "Dónde se equivoca más de uno"), ("Esfuerzos y posturas", "Lo que incomoda o cansa"), ("Momentos de duda", "Cuándo se frena a pensar")], 2), "Qué buscar al observar: lo que la gente hace, no solo lo que dice."),
    "s03d5": (flujo(["El objeto", "Secuencia de uso", "Medidas clave", "Problemas detectados", "Oportunidades"], destacar=4), "El recorrido del análisis de uso."),
    "s04d1": (flujo(["Definir qué querés saber", "Elegir a quién", "Guía de preguntas", "Entrevistar y escuchar", "Anotar frases textuales"]), "Cómo preparar y hacer una entrevista."),
    "s04d3": (comparar(("Requisito", ["Lo que el producto debe hacer", "Ejemplo: no debe encandilar", "Sale de la investigación"]), ("Especificación", ["El mismo requisito, medible", "Ejemplo: la fuente de luz no se ve desde los ojos del usuario sentado", "Se puede verificar con una prueba"])), "De la necesidad a un número que se puede comprobar."),
    "s04d4": (flujo(["Contexto", "Usuario", "Problema", "Objetivos", "Requisitos", "Restricciones", "Criterios de éxito"]), "Las partes de un brief: describe el problema, no la solución."),
    "s04d5": (lista_check(["Una o dos páginas, claras", "Datos de tu investigación", "Cinco especificaciones medibles", "Restricciones y criterios de éxito"], ["Describir la solución", "Requisitos que no se pueden medir", "Un producto demasiado grande para la diplomatura"], tsi="Tiene que tener", tno="Evitá"), "Qué hace bueno a un brief."),
    "s05d2": (matriz(["Apoyarse", "Orientar la luz", "Encender", "Difundir"], ["Opción 1", "Opción 2", "Opción 3", "Opción 4"], [["Base pesada", "Pinza", "Colgada", "Ventosa"], ["Brazo", "Cuello flexible", "Cabezal", "Reflector"], ["Botón", "Perilla", "Táctil", "Cadena"], ["Pantalla", "Acrílico", "Rebote", "Papel"]]), "Matriz morfológica de la lámpara: una opción por fila da un concepto; cuatro por cuatro, 256 combinaciones."),
    "s05d4": (barras([("Idea 4", 31), ("Idea 11", 32), ("Idea 17", 31)], "puntos", maxv=36), "Resultado de la matriz de decisión del ejemplo: casi un empate. La matriz ayuda a conversar, no decide."),
    "s05d5": (flujo(["Las 30 ideas", "Primer filtro: sí, tal vez, no", "Matriz de decisión", "Las tres elegidas", "Boceto más grande"]), "El recorrido que muestra la lámina de exploración."),
    "s06d1": (tarjetas([("Qué es", "Se reconoce como lámpara"), ("Cómo se usa", "Dónde se agarra, qué se gira"), ("Qué valores transmite", "Cálido, técnico, lúdico, austero")], 3), "Las tres cosas que comunica la forma de un producto."),
    "s06d2": (tarjetas([("Geometría base", "Círculo, rectángulo, orgánica"), ("Radios", "Todos de una misma familia"), ("Proporciones", "Relaciones que se repiten"), ("Líneas de partición", "Dónde se unen las piezas"), ("Detalles", "Tornillos, ranuras, bordes")], 3), "Los componentes de un lenguaje formal coherente."),
    "s06d4": (tarjetas([("Color", "Neutros, saturados, tierra, acento"), ("Material", "Lo que se ve y se toca"), ("Terminación", "Brillante, satinada, texturada, natural")], 3), "CMF: color, material y terminación refuerzan el concepto."),
    "s06d5": (tarjetas([("Nombre y frase", "La idea en pocas palabras"), ("Vista principal", "Grande y clara"), ("Vista lateral", "Proporciones"), ("Secuencia de uso", "Cómo se usa, en pasos"), ("Tres palabras", "El carácter del concepto")], 3), "Lo que lleva cada uno de los tres conceptos. Tienen que ser distintos entre sí."),
    "s07d1": (tarjetas([("Resistencia", "¿Soporta la carga?"), ("Rigidez", "¿Se deforma?"), ("Densidad", "¿Cuánto pesa?"), ("Temperatura", "¿Se ablanda con calor?"), ("Conductividad", "¿Conduce calor o electricidad?"), ("Terminación", "¿Qué superficies logra?"), ("Costo", "¿Se consigue en Argentina?"), ("Impacto ambiental", "¿Se recicla, se repara?")], 4), "Las propiedades que se comparan al elegir un material."),
    "s07d2": (tarjetas([("PP", "Bisagras integradas, tapers"), ("PE", "Bidones, flexible"), ("ABS", "Carcasas rígidas"), ("PC", "Difusores, resiste impactos"), ("PMMA", "Transparente, se raya"), ("PET", "Botellas y envases"), ("PLA", "Prototipos 3D"), ("TPE / TPU", "Tacto de goma")], 4), "Los plásticos más usados en productos y un uso típico de cada uno."),
    "s07d3": (tarjetas([("Acero al carbono", "Resistente y económico; hay que protegerlo"), ("Acero inoxidable", "No se oxida; más caro"), ("Aluminio", "Un tercio del peso del acero"), ("Latón", "Dorado, fácil de mecanizar"), ("Zamak", "Se inyecta: piezas chicas con detalle")], 3), "Los metales más usados en productos."),
    "s07d4": (comparar(("Madera maciza", ["Pino, eucalipto, paraíso, guatambú", "Calidez y veta natural", "Se mueve con la humedad", "Hay que respetar la dirección de la veta"]), ("Tableros", ["Multilaminado, MDF, aglomerado", "Medidas estables y grandes", "Cantos que hay que terminar", "Más económicos en superficies grandes"])), "Maderas macizas y tableros: dos lógicas distintas."),
    "s07d5": (matriz(["Base", "Brazo", "Cabezal", "Difusor"], ["Exigencia", "Material", "¿Se consigue?"], [["Peso", "Chapa de acero", "Sí"], ["Rigidez", "Caño de aluminio", "Sí"], ["Calor", "Aluminio", "Sí"], ["Luz pareja", "Policarbonato", "Sí"]]), "Ejemplo de tabla de materiales: cada pieza parte de su exigencia principal."),
    "s08d4": (tarjetas([("Corte láser", "Placas: acrílico, MDF, chapa fina"), ("CNC de placas", "Fresado de madera y tableros"), ("Mecanizado y torno CNC", "Metal macizo con precisión"), ("Impresión 3D", "Formas complejas, pocas unidades")], 2), "Procesos sin molde: van directo del archivo a la pieza."),
    "s08d5": (lista_check(["Unir dos piezas en una", "Usar formatos estándar de material", "Repetir los mismos tornillos", "Procesos que hay en talleres cercanos"], ["Una pieza distinta para cada función", "Medidas que generan desperdicio", "Diez tipos de tornillo"], tsi="Simplificá", tno="Evitá"), "Diseño para la fabricación: simplificar baja costo y errores."),
    "s09d2": (_lineas(), "Tipos de línea según IRAM 4502: la gruesa suele ser el doble de la fina."),
    "s09d5": (tarjetas([("Vistas necesarias", "Ni una más"), ("Tipos de línea", "Según la norma"), ("Corte o sección", "Si hay interior"), ("Acotación completa", "Sin cotas repetidas"), ("Notas", "Material y terminación"), ("Rótulo", "Completo, abajo a la derecha")], 3), "Lo que revisás en el plano de pieza."),
    "s10d1": (comparar(("Fijas", ["Soldadura, remache, pegamento", "Más rígidas y limpias", "No se desarman", "Dificultan reparar y reciclar"]), ("Desmontables", ["Tornillos, encastres, clips", "Permiten cambiar piezas", "Reparar la fuente de luz", "Separar materiales al final"])), "Elegir la unión es decidir también cómo se repara y se recicla."),
    "s10d2": (tarjetas([("Clip", "Largo y fino para flexar"), ("Bisagra integrada", "En polipropileno"), ("Torres", "Alojan tornillos"), ("Encastres de ranura", "Guían y alinean")], 2), "Uniones que se forman en la misma pieza de plástico."),
    "s10d3": (tarjetas([("Medidas generales", "Alto, ancho, profundidad"), ("Piezas numeradas", "Globos alineados"), ("Lista de piezas", "Número, nombre, material, cantidad"), ("Comerciales", "Tornillos y componentes comprados")], 2), "Lo que lleva un plano de conjunto."),
    "s10d5": (flujo(["Plano de conjunto", "Vista explotada", "Uniones definidas", "Piezas comerciales", "Coherencia entre todo"]), "La documentación técnica básica del producto."),
    "s11d1": (tarjetas([("Paramétrico de sólidos", "Piezas que se fabrican"), ("Superficies (NURBS)", "Formas libres y suaves"), ("Mallas y escultura", "Formas orgánicas, render")], 3), "Los tres tipos de modelador. En la diplomatura trabajás con uno paramétrico."),
    "s11d2": (flujo(["Croquis en un plano", "Restricciones geométricas", "Cotas", "Totalmente definido", "Extrusión"], destacar=3), "Del croquis al sólido."),
    "s11d4": (flujo(["Piezas", "Ensamble", "Uniones: rígida o con movimiento", "Verificar que encajen", "Vista explotada y planos"]), "Del modelo de pieza al ensamble."),
    "s11d5": (lista_check(["Todas las piezas", "Medidas reales", "Ensambladas", "Materiales asignados"], ["Piezas sueltas sin ensamblar", "Medidas aproximadas", "Planos sin revisar"], tsi="El modelo tiene", tno="Evitá"), "El modelo completo genera los planos casi solo; igual hay que revisarlos."),
    "s12d1": (escala("Baja fidelidad", "Alta fidelidad", [(0.06, "Maqueta de volumen"), (0.28, "Modelo de uso"), (0.5, "Prototipo funcional"), (0.72, "Modelo de apariencia"), (0.94, "Preserie")], titulo="Tipos de modelo"), "Cada modelo responde una pregunta concreta: elegí el más simple que la responda."),
    "s12d2": (tarjetas([("Cartón corrugado", "Volúmenes rápidos"), ("Cartón pluma", "Planos limpios"), ("Plastilina o arcilla", "Formas de agarre"), ("Alambre y broches", "Brazos y articulaciones")], 2), "Materiales para maquetas rápidas: buscá la forma, no la terminación."),
    "s12d3": (tarjetas([("Altura de capa", "0,2 mm"), ("Relleno", "15% a 20%"), ("Paredes", "2 a 3 perímetros"), ("Soportes", "Solo donde hace falta"), ("Material", "PLA; PETG si pide más"), ("Encastres", "Juego de 0,2 a 0,4 mm")], 3), "Valores habituales para imprimir un prototipo en FDM."),
    "s12d4": (flujo(["Objetivo", "Participantes", "Tareas", "Qué vas a medir", "Preguntas finales"]), "El plan de una prueba de uso. Durante la prueba: no ayudes ni expliques."),
    "s12d5": (flujo(["Preguntas del prototipo", "Construir", "Probar con personas", "Registrar", "Cambios"], destacar=4), "Un problema encontrado en la prueba es una buena noticia: aparece antes de fabricar."),
    "s13d1": (tarjetas([("Luz", "Principal, de relleno y de contorno"), ("Materiales", "Color, rugosidad, textura"), ("Cámara", "Altura y lente naturales"), ("Fondo", "Neutro o en contexto")], 2), "Los cuatro ajustes que más cambian un render."),
    "s13d3": (piramide(["Imagen principal y nombre", "Frase, problema y usuario", "Uso, detalles, datos técnicos y variantes"]), "La jerarquía de una lámina: primero se ve el producto, después se entiende."),
    "s13d4": (flujo(["El personaje", "El problema", "El descubrimiento", "La solución", "El resultado"]), "El relato del producto. Contá beneficios, no solo características."),
    "s13d5": (lista_check(["Imagen principal grande", "Nombre y frase", "Problema y usuario", "Dos o tres detalles", "Grilla, aire y jerarquía"], ["Diez imágenes del mismo tamaño", "Texto largo", "Fondo que compite con el producto"]), "Qué mira la lámina de presentación."),
    "s14d1": (tarjetas([("Boceto", "Papel o tableta"), ("Investigación", "Notas y documentos"), ("Paramétrico", "Piezas y planos"), ("Superficies", "Formas complejas"), ("Render", "Imágenes del producto"), ("Fabricación digital", "Laminador, láser, CNC"), ("Presentación", "Láminas y video"), ("Con IA", "Asistentes y generación")], 4), "El mapa del software por etapa. Cada casillero tiene opciones pagas y gratuitas."),
    "s14d2": (comparar(("La IA ayuda a", ["Preparar entrevistas", "Ordenar notas", "Analizar productos existentes", "Idear variantes", "Revisar el brief"]), ("La IA no", ["Reemplaza hablar con personas reales", "Garantiza datos: puede inventarlos", "Verifica cálculos sola", "Decide por vos"])), "Usala para ampliar, y verificá todo lo que produce."),
    "s14d3": (flujo(["Tu boceto", "Del boceto al render con IA", "Elegir y corregir", "Modelo 3D real", "Render final"], destacar=0), "El boceto manda: la IA propone imágenes, pero el producto se define en el modelo."),
    "s14d4": (matriz(["Impresión 3D", "Corte láser", "CNC de placas", "Mecanizado", "Chapa"], ["Archivo", "Además"], [["STL o 3MF", "Material y color"], ["DXF o PDF", "Material y espesor"], ["DXF o STEP", "Placa y espesor"], ["STEP", "Plano en PDF"], ["STEP o DXF", "Plano de plegado"]]), "Qué archivo pide cada taller. Confirmalo siempre antes de enviar."),
    "s14d5": (flujo(["Investigación", "Brief", "Ideación", "Concepto", "Modelo 3D", "Planos", "Prototipo", "Presentación"]), "Un flujo de trabajo de producto: marcá en cada etapa qué herramienta usás y dónde entra la IA."),
    "s15d1": (tarjetas([("Ajustar el diseño", "Si el requisito importa y se puede cumplir"), ("Revisar la especificación", "Si estaba mal planteada, con justificación"), ("Aceptar el límite", "Si no se puede, decirlo con claridad")], 3), "Tres salidas cuando el concepto no cumple un requisito del brief."),
    "s15d2": (tarjetas([("Salida del cable", "Protegida y prolija"), ("Recorrido del cable", "Oculto o intencional"), ("Articulaciones", "Firmes, sin juego"), ("Encuentro entre materiales", "Con intención"), ("Apoyo", "Pies que no rayen"), ("Bordes", "Sin filos")], 3), "Los detalles que separan un prototipo de un producto."),
    "s15d3": (barras([("Módulo led, cable e interruptor", 12000), ("Cabezal torneado", 11000), ("Base de chapa", 9000), ("Brazo de aluminio", 4500), ("Armado y control", 4000), ("Caja e instructivo", 3500), ("Amortización de matriz", 2000), ("Difusor", 1800), ("Tornillos y pies", 1500)], "$"), "Costo por unidad de la lámpara de ejemplo, serie de 500: unos $ 51.272 con desperdicio. Valores ficticios."),
    "s15d5": (tarjetas([("Nombre y medidas", "Generales"), ("Materiales", "Con terminaciones"), ("Datos técnicos", "Luz, potencia, cable"), ("Variantes", "Colores y versiones"), ("Uso y cuidados", "Limpieza y mantenimiento"), ("Fabricación y costo", "Procesos y costo estimado")], 3), "Lo que lleva la ficha técnica."),
    "s16d1": (flujo(["Portada", "Resumen", "Investigación", "Brief", "Ideación", "Desarrollo", "Documentación técnica", "Prototipo y pruebas", "Producto final", "Flujo de trabajo", "Conclusiones"]), "Las once partes de la carpeta del proyecto, en orden."),
    "s16d2": (escala("Más simple", "Más fiel", [(0.08, "Solo render"), (0.36, "Maqueta de cartón y madera"), (0.64, "Impresión 3D lijada y pintada"), (0.92, "Piezas reales de taller")], titulo="Modelo de presentación"), "Elegí el modelo según tu tiempo y tu presupuesto: lo importante es que se entienda el producto."),
    "s16d3": (linea_tiempo([("0:00", "El producto en uso"), ("0:20", "Problema y usuario"), ("0:50", "La solución"), ("1:40", "Cómo se fabrica"), ("2:20", "Pruebas y cambios"), ("2:50", "Cierre")]), "El guion del video de tres minutos."),
    "s16d4": (tarjetas([("Investigación", "Uso y entrevistas"), ("Brief", "Especificaciones medibles"), ("Ideación", "Exploración amplia"), ("Desarrollo", "Forma, CMF, materiales"), ("Documentación técnica", "Planos completos"), ("Prototipo y pruebas", "Con cambios"), ("Comunicación", "Lámina y video")], 4), "Los siete criterios de la rúbrica final."),
    "s16d5": (tarjetas([("Carpeta", "Todo el proceso"), ("Lámina final", "Presentación"), ("Ficha técnica", "Datos y costo"), ("Video", "Tres minutos"), ("Fotos del modelo", "De presentación"), ("Planilla de hoy", "Para comparar con la semana 1")], 3), "Todo lo que entregás al cierre."),
}
