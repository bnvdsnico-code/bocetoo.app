"""Genera la portada (index.html) y las fichas de las 4 diplomaturas con el sistema visual común.
Datos: este archivo + content/<carrera>/temario.json. Uso: python3 tools/paginas.py  (después: seo.py)"""
import json, pathlib, html
import layout

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
esc = lambda s: html.escape(s, quote=True)

FUENTES = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
           '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&amp;family=Inter:wght@400;500;600;700&amp;display=swap" rel="stylesheet">')

CHECK = '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M4 10.5l4 4 8-9" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

D = {
 "interiores": {
  "nombre": "Interiores y Mobiliario", "corto": "Interiores", "titulo": "Diseño de Interiores y Mobiliario",
  "foto": "card-interiores", "alt": "Revista de diseño abierta y una taza sobre una mesa de cajón de madera, frente a un sillón claro con almohadones azules", "credito": "Karolina Grabowska",
  "resumen": "Planos, recorridos, iluminación, materiales y muebles a medida, con tu propio living como hilo conductor.",
  "aprender": ["Relevar y dibujar planos acotados en escala.", "Distribuir ambientes con medidas, recorridos y zonas.", "Diseñar cocina, baño, dormitorios y guardado.", "Elegir color, materiales e iluminación con criterio técnico.", "Diseñar y documentar muebles a medida.", "Presentar el proyecto con perspectivas, 3D, IA y presupuesto."],
  "proyecto": ("El proyecto completo de un departamento", "Proyectás el interior de un departamento de dos ambientes para un cliente: distribución, cocina y baño, color, materiales, iluminación, un mueble a medida, documentación y presupuesto. Queda listo para tu portfolio."),
  "materiales": ["Lápiz, goma y escalímetro", "Papel A3 o cuaderno de croquis", "Cinta métrica"],
  "pregunta": ("¿Cuánto espacio dejo entre el sillón y la mesa ratona?", "Como referencia, entre 40 y 45 cm. Lo vemos en la clase «Recorridos y pasos libres», con un ejercicio sobre tu propio living."),
  "faq": [("¿Necesito experiencia previa?", "No. La diplomatura es de nivel inicial y arranca desde cómo leer una planta."),
          ("¿Necesito algún programa?", "No para empezar: las primeras unidades se trabajan a mano o en el Bocetador. En la semana 14 usamos SketchUp o Sweet Home 3D, que es gratis.")],
  "bocetador": "Cuadrícula a escala, muros, aberturas y muebles en medidas reales, y cotas que se miden solas.",
 },
 "industrial": {
  "nombre": "Diseño Industrial", "corto": "Industrial", "titulo": "Diseño Industrial",
  "foto": "card-industrial", "alt": "Pantalla de computadora con un modelo 3D de muebles de madera, mesas de luz y un rack con patas, en un programa de modelado", "credito": "cottonbro studio",
  "resumen": "Bocetado, usuarios, materiales y procesos, modelado y prototipo, con una lámpara de escritorio como hilo conductor.",
  "aprender": ["Bocetar productos en perspectiva con luz, sombra y materiales.", "Investigar usuarios y escribir un brief con especificaciones.", "Generar, evaluar y desarrollar conceptos de producto.", "Elegir materiales y procesos de fabricación con criterio.", "Dibujar planos normalizados y modelar en 3D paramétrico.", "Prototipar, probar con personas y presentar con render e IA."],
  "proyecto": ("Una lámpara de escritorio, del boceto al prototipo", "Investigás a quien estudia en casa, ideás, elegís materiales y procesos, dibujás los planos, modelás, construís un prototipo, lo probás con personas y presentás el producto con carpeta, lámina y video."),
  "materiales": ["Lápiz, fibras finas y hojas A3", "Cartón, cúter y plasticola para maquetas", "Marcadores grises (opcional)", "Computadora desde la semana 11"],
  "pregunta": ("¿Cómo hago para que la elipse del cilindro no se vea torcida?", "Alineá el eje menor de la elipse con el eje del cilindro. Subí tu boceto al Bocetador y te marco dónde se desvía."),
  "faq": [("¿Tengo que saber dibujar?", "No. El bocetado es una técnica que se entrena: la diplomatura arranca desde el trazo más simple."),
          ("¿Puedo bocetar en tableta?", "Sí. Los ejercicios funcionan igual en papel o en una tableta con lápiz."),
          ("¿Necesito algún programa?", "No para empezar: las primeras diez semanas son a mano o en el Bocetador. Desde la semana 11 modelamos en 3D con programas con licencia gratuita para estudiantes, como Fusion u Onshape.")],
  "bocetador": "Perspectiva con dos puntos de fuga que guía cada línea, y correcciones sobre el boceto.",
 },
 "grafico": {
  "nombre": "Diseño Gráfico", "corto": "Gráfico", "titulo": "Diseño Gráfico",
  "foto": "card-grafico", "alt": "Manos que eligen muestras de color impresas sobre una mesa blanca: tarjetas verde, terracota, violeta y beige", "credito": "Noemi Jimenez",
  "resumen": "Composición, tipografía, color e imagen, hasta la identidad visual completa de un emprendimiento.",
  "aprender": ["Componer con retículas, jerarquía y recorrido visual.", "Elegir, combinar y componer tipografía con oficio.", "Usar el color con criterio, para papel y pantalla, y accesible.", "Investigar una marca y construir su isologo y su sistema visual.", "Diseñar aplicaciones, folletos y piezas listas para imprenta.", "Diseñar para redes y web, con IA, y armar el manual de marca."],
  "proyecto": ("La identidad completa de un emprendimiento", "Construís la identidad de un emprendimiento real o del brief de práctica: investigación, isologo, sistema visual, aplicaciones, folleto para imprenta, kit de redes y manual de marca."),
  "materiales": ["Cuaderno, lápiz y fibra para bocetar", "Papeles de colores y tijera para las primeras semanas", "Computadora desde la semana 3 (hay programas gratuitos)"],
  "pregunta": ("¿Mi isologo funciona en tamaño chico?", "Subilo y lo probamos juntos: a 16 px, en una sola tinta y en negativo. Si pierde detalle, vemos una versión reducida."),
  "faq": [("¿Qué programa necesito?", "Para empezar, ninguno: las dos primeras semanas son a mano o en el Bocetador. Después podés usar Adobe o alternativas gratuitas como Affinity, Inkscape y Figma."),
          ("¿Puedo trabajar con una marca propia?", "Sí, es lo ideal. Si no tenés una, trabajás con el brief de práctica de la diplomatura: Molienda, un café de barrio.")],
  "bocetador": "Hoja A4 con retícula de 12 columnas y simetría para construir marcas.",
 },
 "indumentaria": {
  "nombre": "Diseño de Indumentaria", "corto": "Indumentaria", "titulo": "Diseño de Indumentaria",
  "foto": "card-indumentaria", "alt": "Figurines dibujados a lápiz y coloreados en azul, junto a una cinta métrica, un alfiletero, una tijera y una caja de botones rojos", "credito": "Jane Blaze",
  "resumen": "Figurín, cuerpo y textiles, moldería y confección, hasta una colección cápsula con su prototipo.",
  "aprender": ["Dibujar figurines, prendas, materiales y geometrales.", "Tomar medidas, entender talles, holgura y calce.", "Conocer fibras, telas y avíos y elegir con criterio.", "Investigar, conceptualizar y diseñar una colección cápsula.", "Hacer moldería base, transformaciones y fichas técnicas.", "Coser un prototipo, costear, producir de forma responsable y presentar."],
  "proyecto": ("Una colección cápsula con su prototipo", "Diseñás una colección de seis looks para una marca real o el brief de práctica, moldeás y cosés una prenda, la costeás y la presentás con carpeta técnica, lookbook y portfolio."),
  "materiales": ["Lápiz, fibras y lápices de colores", "Cinta métrica, regla, escuadra y papel madera", "Tela de prueba, tijera y alfileres", "Acceso a una máquina de coser desde la semana 9"],
  "pregunta": ("¿Dónde marco los piquetes de la falda?", "En los costados, a la altura de la cadera. En la espalda se marcan dos, para no confundirla con el delantero."),
  "faq": [("¿Necesito máquina de coser?", "Hasta la semana 8, no. Desde la semana 9 cosés tu prototipo: si no tenés máquina, te sugerimos espacios, escuelas de oficios y cooperativas donde usar una."),
          ("¿Sirve para cualquier talle?", "Sí. Las bases se trazan con tus propias medidas o con las de una tabla de talles.")],
  "bocetador": "Figurín de 9 cabezas para trabajar proporciones, y correcciones sobre tus geometrales.",
 },
}
ORDEN = ["interiores", "industrial", "grafico", "indumentaria"]
FAQ_COMUN = [
  ("¿Recibo un certificado?", "Sí. Al completar las 80 clases obtenés un certificado de finalización con un enlace para que cualquiera lo verifique. Es un curso libre: no otorga título oficial."),
  ("¿Cómo me doy de baja?", "Desde tu página de inscripción, con un clic, o con el Botón de baja de servicio. Desde la baja no se cobran nuevas cuotas."),
]

def temario(c): return json.loads((ROOT / "content" / c / "temario.json").read_text(encoding="utf-8"))

def foto(c, sizes, eager=False):
    d = D[c]
    return (f'<img src="/assets/fotos/{d["foto"]}.webp" srcset="/assets/fotos/{d["foto"]}-640.webp 640w, /assets/fotos/{d["foto"]}.webp 1200w" '
            f'sizes="{sizes}" width="1200" height="900" {"fetchpriority=\"high\"" if eager else "loading=\"lazy\""} alt="{esc(d["alt"])}">')

def pagina(titulo, desc, body, css, extra_js=""):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{FUENTES}
<link rel="stylesheet" href="/assets/base.css">
<link rel="stylesheet" href="/assets/{css}">
</head>
<body>
<!--s-head--><!--/s-head-->
<main id="contenido">
{body}
</main>
<!--s-foot--><!--/s-foot-->
<script src="/assets/nav.js" defer></script>{extra_js}
</body>
</html>
"""

# ---------------------------------------------------------------- Portada
LAMINA = """<figure class="lamina" aria-labelledby="lamina-cap">
<div class="lamina-tabs" role="tablist" aria-label="Elegí una disciplina">
<button role="tab" class="d-interiores" aria-selected="true" data-lamina="interiores">Interiores</button><button role="tab" class="d-industrial" aria-selected="false" data-lamina="industrial">Industrial</button><button role="tab" class="d-grafico" aria-selected="false" data-lamina="grafico">Gráfico</button><button role="tab" class="d-indumentaria" aria-selected="false" data-lamina="indumentaria">Indumentaria</button>
</div>
<div class="lamina-hoja grilla">
<svg class="dib d-interiores" data-dib="interiores" viewBox="0 0 560 420" role="group" aria-label="Planta de un living de 4 por 3,20 metros. Arrastrá la mesa ratona para dejar 90 centímetros de paso hasta la butaca.">
<g class="trazo" stroke="var(--grafito)" fill="none" stroke-linecap="round" stroke-linejoin="round">
<path pathLength="1" stroke-width="9" d="M150 372H96V64H470V372H210"/>
<path pathLength="1" stroke-width="2" d="M210 372V318"/><path pathLength="1" stroke-width="1.6" d="M210 318A54 54 0 0 0 156 372"/>
<path pathLength="1" stroke-width="2.4" d="M234 296h184v54H234z M234 338h184 M295 296v42 M357 296v42"/>
<path pathLength="1" stroke-width="2.4" d="M404 196h58v62h-58z M404 210h58"/>
</g>
<g class="cota" stroke="var(--grafito-2)" stroke-width="1.2" fill="none"><path pathLength="1" d="M96 34H470 M90 40l12-12 M464 40l12-12 M96 26v16 M470 26v16"/><path pathLength="1" d="M58 64V372 M52 70l12-12 M52 378l12-12 M50 64h16 M50 372h16"/></g>
<text class="cota-t" x="283" y="24" text-anchor="middle">4,00 m</text><text class="cota-t" x="48" y="222" text-anchor="middle" transform="rotate(-90 48 222)">3,20 m</text>
<g class="medida" data-medida><path data-medida-l d="" stroke="var(--interiores)" stroke-width="1.6" fill="none"/><text data-medida-t x="0" y="232" text-anchor="middle" class="medida-t"></text></g>
<g class="arr" data-arr tabindex="0" role="slider" aria-label="Posición de la mesa ratona" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><rect class="arr-zona" x="244" y="206" width="124" height="68" rx="8"/><rect class="trazo-1" pathLength="1" x="250" y="214" width="112" height="52" fill="var(--hoja)" stroke="var(--grafito)" stroke-width="2.4"/></g>
<g data-marca><g class="marca"><circle class="marca-a" r="22" fill="none" stroke-width="2"/><circle class="marca-c" r="13"/><text y="5" text-anchor="middle" class="marca-n" data-marca-n>1</text></g></g>
</svg>
<svg class="dib d-industrial" data-dib="industrial" viewBox="0 0 560 420" role="group" aria-label="Caja en perspectiva con dos puntos de fuga. Arrastrá la esquina marcada hasta la línea que va al punto de fuga." hidden>
<path class="guia" pathLength="1" d="M20 120H540" stroke="var(--industrial)" stroke-width="1.4" opacity=".55" fill="none"/>
<text class="guia-t" x="34" y="110">Línea de horizonte</text>
<g class="guia" stroke="var(--industrial)" stroke-width="1" opacity=".4" fill="none"><path pathLength="1" d="M280 172L20 120M280 172L540 120M280 330L20 120M280 330L540 120"/></g>
<circle cx="20" cy="120" r="6" fill="#FFF" stroke="var(--industrial)" stroke-width="2"/><circle cx="540" cy="120" r="6" fill="#FFF" stroke="var(--industrial)" stroke-width="2"/>
<g class="trazo" stroke="var(--grafito)" stroke-linecap="round" fill="none"><path pathLength="1" stroke-width="3" d="M280 172V330 M164 151V236"/><path pathLength="1" stroke-width="3" d="M280 172L164 151 M280 172L410 146 M280 330L164 236"/><path pathLength="1" stroke-width="2" d="M164 151L298 132 M410 146L298 132"/></g>
<path data-esq-l d="" stroke="var(--grafito)" stroke-width="3" stroke-linecap="round" fill="none"/>
<g class="arr" data-arr tabindex="0" role="slider" aria-label="Altura de la esquina de la caja" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><circle class="arr-zona" cx="410" cy="276" r="20"/><circle data-esq cx="410" cy="276" r="7" fill="var(--hoja)" stroke="var(--industrial)" stroke-width="2.5"/></g>
<g data-marca><g class="marca"><circle class="marca-a" r="22" fill="none" stroke-width="2"/><circle class="marca-c" r="13"/><text y="5" text-anchor="middle" class="marca-n" data-marca-n>1</text></g></g>
</svg>
<svg class="dib d-grafico" data-dib="grafico" viewBox="0 0 560 420" role="group" aria-label="Afiche con retícula de columnas. Arrastrá el titular hasta alinearlo con la columna." hidden>
<rect x="160" y="28" width="240" height="364" fill="#FFF" stroke="var(--grafito-2)" stroke-width="1.2"/>
<g class="guia" stroke="var(--grafico)" stroke-width="1" opacity=".35" fill="none"><path pathLength="1" d="M184 28V392M224 28V392M264 28V392M296 28V392M336 28V392M376 28V392M160 52H400M160 368H400"/></g>
<path class="col-ok" d="M184 28V392" stroke="var(--grafico)" stroke-width="2" opacity="0"/>
<g class="trazo" stroke="var(--grafito)" fill="none" stroke-linecap="round"><ellipse pathLength="1" cx="280" cy="128" rx="30" ry="42" transform="rotate(-28 280 128)" stroke-width="3"/><path pathLength="1" stroke-width="3" d="M291 90c-24 14 4 42-22 76"/></g>
<g class="guia" stroke="var(--grafico)" stroke-width="1" stroke-dasharray="4 4" fill="none" opacity=".6"><circle pathLength="1" cx="280" cy="128" r="62"/></g>
<g class="arr" data-arr tabindex="0" role="slider" aria-label="Posición del titular" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><rect class="arr-zona" x="176" y="190" width="200" height="50" rx="6"/><text class="t-cafe" x="184" y="228">Molienda</text></g>
<g fill="var(--grafito)" opacity=".2"><rect x="184" y="262" width="192" height="8" rx="2"/><rect x="184" y="280" width="176" height="8" rx="2"/><rect x="184" y="298" width="184" height="8" rx="2"/><rect x="184" y="330" width="72" height="8" rx="2"/></g>
<g data-marca><g class="marca"><circle class="marca-a" r="22" fill="none" stroke-width="2"/><circle class="marca-c" r="13"/><text y="5" text-anchor="middle" class="marca-n" data-marca-n>1</text></g></g>
</svg>
<svg class="dib d-indumentaria" data-dib="indumentaria" viewBox="0 0 560 420" role="group" aria-label="Figurín de nueve cabezas con un vestido. Arrastrá el cinturón hasta el final de la cabeza 3." hidden>
<g class="guia" stroke="var(--indumentaria)" stroke-width="1" opacity=".35" fill="none"><path pathLength="1" d="M180 24H380M180 66H380M180 108H380M180 150H380M180 192H380M180 234H380M180 276H380M180 318H380M180 360H380M180 402H380"/></g>
<rect class="cab-ok" x="180" y="108" width="200" height="42" fill="var(--indumentaria)" opacity="0"/>
<g class="nums"><text x="168" y="50">1</text><text x="168" y="92">2</text><text x="168" y="134">3</text><text x="168" y="176">4</text><text x="168" y="218">5</text><text x="168" y="260">6</text><text x="168" y="302">7</text><text x="168" y="344">8</text><text x="168" y="386">9</text></g>
<g class="trazo" stroke="var(--grafito)" fill="none" stroke-linecap="round" stroke-linejoin="round"><ellipse pathLength="1" cx="280" cy="45" rx="15" ry="20" stroke-width="2.6"/><path pathLength="1" stroke-width="2.6" d="M274 64v12 M286 64v12 M246 84c10-6 58-6 68 0 M246 84l-12 70 M314 84l12 70"/><path pathLength="1" stroke-width="2.6" d="M262 300l-6 96 M298 300l6 96"/></g>
<path data-vestido d="" stroke="var(--grafito)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<g class="arr" data-arr tabindex="0" role="slider" aria-label="Altura de la cintura" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><rect class="arr-zona" x="236" y="0" width="88" height="28" rx="6" data-cint-z/><rect data-cint x="248" y="0" width="64" height="7" rx="3.5" fill="var(--indumentaria)"/></g>
<g data-marca><g class="marca"><circle class="marca-a" r="22" fill="none" stroke-width="2"/><circle class="marca-c" r="13"/><text y="5" text-anchor="middle" class="marca-n" data-marca-n>1</text></g></g>
</svg>
<p class="nota" aria-live="polite"><b data-nota-n>1</b><span data-nota-t></span><a class="nota-a" data-nota-a href="/bocetador/" hidden>Seguí en el Bocetador</a></p>
</div>
<figcaption id="lamina-cap">Corregí el dibujo como lo marca el asistente: arrastrá la pieza señalada, con el mouse, el dedo o las flechas del teclado.</figcaption>
</figure>"""

def portada():
    tarjetas = []
    for c in ORDEN:
        d, T = D[c], temario(c)
        tarjetas.append(f"""<article class="dip d-{c}">
<a class="dip-foto" href="/cursos/{c}.html" tabindex="-1" aria-hidden="true">{foto(c, "(max-width: 760px) 100vw, 560px")}</a>
<div class="dip-txt">
<span class="d-chip">{d["corto"]}</span>
<h3 class="t-h3"><a href="/cursos/{c}.html">{esc(T["titulo"])}</a></h3>
<p>{esc(d["resumen"])}</p>
<p class="dip-proy"><span>Proyecto final</span> {esc(d["proyecto"][0])}</p>
<div class="dip-acc"><a class="btn btn-ink btn-s" href="/cursos/{c}/semana-01/clase-1.html">Probar la clase 1</a><a class="btn btn-s" href="/cursos/{c}.html">Ver la diplomatura</a></div>
</div>
<p class="credito">Foto: {esc(d["credito"])}</p>
</article>""")
    faq = [("¿Necesito saber dibujar?", "No. Todas las diplomaturas son de nivel inicial: el dibujo se entrena desde el primer trazo, a mano o en el Bocetador."),
           ("¿Cuánto tiempo por semana lleva?", "Una hora por día, cinco días por semana, durante 16 semanas. Cada clase tiene lectura, práctica y repaso, y la hacés cuando quieras."),
           ("¿Hay profesor?", "No hay clases en vivo. En cada clase tenés un asistente de IA que conoce todo el contenido, responde tus dudas a cualquier hora y corrige tus dibujos con marcas sobre el trabajo."),
           ("¿Cómo pruebo antes de pagar?", "La primera clase de cada diplomatura es gratis y no pide tarjeta. Podés usar el Bocetador sin registrarte."),
           ("¿Cómo se paga?", "Con una suscripción mensual de Mercado Pago, con tarjeta de crédito o débito. Al inscribirte por primera vez se abona además una matrícula única."),
           ("¿Qué pasa si quiero darme de baja?", "Te das de baja desde tu página de inscripción o con el Botón de baja de servicio, y no se cobran más cuotas. Tenés 10 días para arrepentirte de la compra.")]
    body = f"""<section class="hero">
<div class="wrap hero-in">
<div class="hero-txt">
<h1 class="t-display">Aprendé a diseñar espacios, objetos, marcas y ropa.</h1>
<p class="t-lead">Diplomaturas online de Interiores y Mobiliario, Industrial, Gráfico e Indumentaria. Una hora por día, dibujando desde la primera clase, con un asistente que corrige tu trabajo.</p>
<div class="hero-acc"><a class="btn btn-ink btn-l" href="#diplomaturas">Probar una clase gratis</a><a class="btn btn-l" href="#planes">Ver planes</a></div>
<dl class="hero-datos"><div><dt>Duración</dt><dd>16 semanas</dd></div><div><dt>Dedicación</dt><dd>1 hora por día</dd></div><div><dt>Desde</dt><dd>$63.000 por mes</dd></div></dl>
</div>
{LAMINA}
</div>
</section>

<section class="sec" id="diplomaturas" aria-labelledby="dip-t">
<div class="wrap">
<div class="sec-h"><h2 class="t-h2" id="dip-t">Cuatro diplomaturas, un proyecto real en cada una</h2><p class="t-lead">Cada una dura 16 semanas, tiene 80 clases y termina con un proyecto para tu portfolio. La primera clase es gratis.</p></div>
<div class="dips">
{chr(10).join(tarjetas)}
</div>
</div>
</section>

<section class="sec sec-papel" id="como-se-estudia" aria-labelledby="como-t">
<div class="wrap">
<div class="sec-h"><h2 class="t-h2" id="como-t">Una semana en boceto</h2><p class="t-lead">Cuatro clases y una entrega. Lo hacés a tu ritmo, en el horario que te quede cómodo.</p></div>
<ol class="semana">
<li><span class="dia">Lunes a jueves</span><h3 class="t-h4">Una clase por día</h3><p>Lectura con láminas y ejemplos, una práctica corta y un repaso de tres preguntas. Alrededor de una hora.</p></li>
<li><span class="dia">Viernes</span><h3 class="t-h4">Entregás en el Bocetador</h3><p>Dibujás o subís la foto de tu boceto en papel. El asistente marca sobre el dibujo qué corregir y por qué.</p></li>
<li><span class="dia">Cuando quieras</span><h3 class="t-h4">Corregís y avanzás</h3><p>Tu panel guarda las clases hechas, las entregas y tu portfolio, en la compu o en el celular.</p></li>
</ol>
<div class="extras">
<div><h3 class="t-h4">Un asistente que conoce la diplomatura</h3><p>Le preguntás en cada clase, a cualquier hora. Responde con lo que estás viendo y te da ejemplos.</p></div>
<div><h3 class="t-h4">Un proyecto para tu portfolio</h3><p>Las 16 entregas arman un proyecto completo: un departamento, una lámpara, una identidad o una colección.</p></div>
<div><h3 class="t-h4">Certificado verificable</h3><p>Al completar las 80 clases obtenés tu certificado, con un enlace para que cualquiera lo compruebe.</p></div>
</div>
</div>
</section>

<section class="sec" id="bocetador" aria-labelledby="boc-t">
<div class="wrap boc">
<div class="boc-txt">
<h2 class="t-h2" id="boc-t">El Bocetador: una mesa de dibujo para cada disciplina</h2>
<p class="t-lead">Funciona con mouse, con el dedo o con lápiz, y se instala como app en el celular, la tablet o la computadora. Para probarlo no hace falta registrarse.</p>
<a class="btn btn-ink btn-l" href="/bocetador/">Abrir el Bocetador</a>
</div>
<ul class="boc-lista">
{"".join(f'<li class="d-{c}"><span class="d-chip">{D[c]["corto"]}</span><p>{esc(D[c]["bocetador"])}</p></li>' for c in ORDEN)}
<li class="boc-foto"><span class="t-h4">¿Bocetás en papel?</span><p>Sacale una foto, subila y el asistente la corrige con marcas numeradas sobre tu dibujo.</p></li>
</ul>
</div>
</section>

<section class="sec sec-papel" id="planes" aria-labelledby="planes-t">
<div class="wrap">
<div class="sec-h"><h2 class="t-h2" id="planes-t">Planes</h2><p class="t-lead">Probá gratis la primera clase de cada diplomatura. Cuando te inscribís, la cuota se debita sola cada mes y podés darte de baja cuando quieras.</p></div>
<div class="planes">
<article class="plan"><h3 class="t-h4">Tu diplomatura</h3><p class="precio">$63.000<span> por mes</span></p><p>Una diplomatura, en 4 cuotas mensuales. Al pagar la última, el acceso queda para siempre.</p><a class="btn btn-l" href="/inscripcion.html?plan=diplomatura">Elegir mi diplomatura</a></article>
<article class="plan plan-dest"><h3 class="t-h4">Todas las diplomaturas</h3><p class="precio">$83.000<span> por mes</span></p><p>Las cuatro diplomaturas y las que se sumen, mientras sigas suscripto.</p><a class="btn btn-ink btn-l" href="/inscripcion.html?plan=todas">Suscribirme a todas</a></article>
<article class="plan"><h3 class="t-h4">Instituciones</h3><p class="precio">Desde $175.000</p><p>Por persona y por diplomatura, desde 10 personas. Para escuelas, estudios y equipos.</p><a class="btn btn-l" href="mailto:hola@bocetoo.app?subject=Planes%20para%20instituciones">Escribinos</a></article>
</div>
<p class="planes-nota"><b>Matrícula única de $45.000.</b> Se abona una sola vez, al inscribirte por primera vez, y vale para todas las diplomaturas. Pagás con tarjeta de crédito o débito por Mercado Pago. Si no se puede cobrar una cuota, el acceso se pausa hasta regularizarla.</p>
</div>
</section>

<section class="sec" id="preguntas" aria-labelledby="faq-t">
<div class="wrap faq-w">
<h2 class="t-h2" id="faq-t">Preguntas frecuentes</h2>
<div class="faq">
{"".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)}
</div>
</div>
</section>

<section class="cierre grilla">
<div class="wrap cierre-in">
<h2 class="t-h1">Tu primer proyecto empieza con un boceto.</h2>
<a class="btn btn-ink btn-l" href="#diplomaturas">Elegir una diplomatura</a>
</div>
</section>"""
    return pagina("boceto · Diplomaturas de diseño online: Interiores, Industrial, Gráfico e Indumentaria",
                  "Escuela de diseño online en Argentina. Diplomaturas de 16 semanas en Interiores y Mobiliario, Industrial, Gráfico e Indumentaria, con asistente de IA y bocetador. Primera clase gratis.",
                  body, "home.css", '\n<script src="/assets/home.js" defer></script>')

# ---------------------------------------------------------------- Fichas
def ficha(c):
    d, T = D[c], temario(c)
    unidades = []
    for u in T["unidades"]:
        semanas = "".join(
            f'<li><span class="sem-n">Semana {s["n"]}</span><div><b>{esc(s["titulo"])}</b>'
            f'<ul>{"".join(f"<li>{esc(x)}</li>" for x in s["clases"])}</ul>'
            f'<span class="sem-e">Entrega: {esc(s["entrega"])}</span></div></li>' for s in u["semanas"])
        rango = " y ".join(str(s["n"]) for s in u["semanas"])
        unidades.append(f'<details class="uni"><summary><span class="uni-n">{u["n"]}</span><span class="uni-t">{esc(u["titulo"])}</span><span class="uni-s">Semanas {rango}</span></summary><ol class="sems">{semanas}</ol></details>')
    faq = d["faq"] + FAQ_COMUN
    body = f"""<div class="d-{c}">
<section class="f-hero">
<div class="wrap f-hero-in">
<div class="f-hero-txt">
<nav class="migas" aria-label="Ruta"><a href="/#diplomaturas">Diplomaturas</a><span aria-hidden="true">/</span><span aria-current="page">{d["nombre"]}</span></nav>
<span class="d-chip">{d["nombre"]}</span>
<h1 class="t-h1">{esc(T["titulo"])}</h1>
<p class="t-lead">{esc(T["bajada"])}</p>
<dl class="f-datos"><div><dt>Duración</dt><dd>16 semanas</dd></div><div><dt>Dedicación</dt><dd>1 hora por día</dd></div><div><dt>Clases</dt><dd>80 y 16 entregas</dd></div><div><dt>Nivel</dt><dd>Inicial</dd></div></dl>
<div class="f-acc"><a class="btn btn-ink btn-l" href="/cursos/{c}/semana-01/clase-1.html">Probar la clase 1 gratis</a><a class="btn btn-l" href="/inscripcion.html?plan=diplomatura&amp;carrera={c}">Inscribirme</a></div>
</div>
<figure class="f-foto">{foto(c, "(max-width: 900px) 100vw, 560px", eager=True)}<figcaption>Foto: {esc(d["credito"])}</figcaption></figure>
</div>
</section>

<div class="wrap f-cuerpo">
<div class="f-main">
<section aria-labelledby="apr-t"><h2 class="t-h2" id="apr-t">Qué vas a aprender</h2>
<ul class="apr">{"".join(f"<li>{CHECK}<span>{esc(x)}</span></li>" for x in d["aprender"])}</ul></section>

<section aria-labelledby="prog-t"><div class="f-sec-h"><h2 class="t-h2" id="prog-t">Programa</h2><p class="t-small">8 unidades, 16 semanas, 80 clases. Abrí una unidad para ver sus clases.</p></div>
<div class="unis">{"".join(unidades)}</div>
<a class="btn" href="/cursos/{c}/programa.html">Ver el programa completo</a></section>

<section class="proy" aria-labelledby="proy-t"><span class="proy-k">Proyecto final</span><h2 class="t-h2" id="proy-t">{esc(d["proyecto"][0])}</h2><p>{esc(d["proyecto"][1])}</p></section>

<section class="f-dos" aria-label="Cómo se estudia">
<div><h2 class="t-h3">Cómo es cada clase</h2><p>Una lectura con láminas y diagramas, una práctica para hacer a mano o en el Bocetador, y un repaso corto. Los viernes, una entrega que el asistente corrige sobre tu dibujo.</p></div>
<div class="chat" aria-label="Ejemplo de consulta al asistente"><h2 class="t-h3">Preguntale al asistente</h2><p class="chat-me">{esc(d["pregunta"][0])}</p><p class="chat-ai">{esc(d["pregunta"][1])}</p></div>
</section>

<section aria-labelledby="mat-t"><h2 class="t-h3" id="mat-t">Materiales</h2><ul class="mat">{"".join(f"<li>{esc(x)}</li>" for x in d["materiales"])}</ul></section>

<section aria-labelledby="faq-t"><h2 class="t-h2" id="faq-t">Preguntas frecuentes</h2>
<div class="faq">{"".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)}</div></section>
</div>

<aside class="f-precio" aria-label="Precio e inscripción">
<div class="f-precio-in">
<p class="precio">$63.000<span> por mes</span></p>
<p class="t-small">4 cuotas mensuales. Matrícula única de $45.000. Al pagar la última cuota, el acceso queda para siempre.</p>
<a class="btn btn-ink btn-l" href="/inscripcion.html?plan=diplomatura&amp;carrera={c}">Inscribirme</a>
<a class="btn btn-l" href="/cursos/{c}/semana-01/clase-1.html">Probar la clase 1 gratis</a>
<ul class="incl">{"".join(f"<li>{CHECK}<span>{x}</span></li>" for x in ["80 clases cortas con láminas y diagramas", "Bocetador y asistente de IA en cada clase", "Correcciones sobre tus entregas", "Certificado verificable al terminar"])}</ul>
<p class="t-small">¿Querés las cuatro? <a href="/inscripcion.html?plan=todas">Todas las diplomaturas por $83.000 por mes</a>.</p>
</div>
</aside>
</div>
</div>"""
    return pagina(f"Diplomatura en {d['titulo']} online · 16 semanas · boceto", f"Curso online de {d['titulo']}: {T['bajada'][0].lower() + T['bajada'][1:]} Primera clase gratis.", body, "ficha.css")

if __name__ == "__main__":
    (PUB / "index.html").write_text(layout.aplicar(portada()), encoding="utf-8"); print("ok index.html")
    for c in ORDEN:
        (PUB / "cursos" / f"{c}.html").write_text(layout.aplicar(ficha(c)), encoding="utf-8"); print("ok", c)
