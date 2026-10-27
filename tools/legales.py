"""Genera /privacidad.html y /terminos.html (páginas simples, mismo estilo que inscripción)."""
import pathlib

PUB = pathlib.Path(__file__).resolve().parent.parent / "public"

BASE = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titulo} · boceto</title>
<meta name="description" content="{descripcion}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/inscripcion.css">
<style>.legal h2{{font-size:18px;margin:8px 0 0}}.legal p,.legal li{{font-size:16px;line-height:1.6;color:#2A2A2A;margin:0}}.legal ul{{margin:0;padding-left:22px;display:flex;flex-direction:column;gap:6px}}</style>
</head>
<body>
<header class="i-top">
  <a class="i-brand" href="/"><span class="marks" aria-hidden="true"><i></i><i></i><i></i><i></i></span><b>boceto</b></a>
  <a href="/">Volver al inicio</a>
</header>
<main class="i-main">
  <section class="i-intro"><p class="i-kick">Legales</p><h1>{titulo}</h1><p>Última actualización: 27 de octubre de 2026.</p></section>
  <section class="i-card legal">
{cuerpo}
  </section>
</main>
</body>
</html>
'''

PRIVACIDAD = '''    <p>boceto es una escuela de diseño online. Esta política explica qué datos personales tratamos, para qué y cuáles son tus derechos, de acuerdo con la Ley 25.326 de Protección de Datos Personales.</p>
    <h2>Qué datos usamos</h2>
    <ul>
      <li><b>Cuenta:</b> cuando ingresás con Google recibimos tu nombre, tu email y tu foto de perfil. No accedemos a tu correo, tus contactos ni ningún otro dato de tu cuenta de Google.</li>
      <li><b>Pagos:</b> los procesa Mercado Pago. Nosotros guardamos el estado de tu suscripción y de la matrícula, el email de pago y el identificador de la operación. Nunca vemos ni guardamos los datos de tu tarjeta.</li>
      <li><b>Tu progreso y tus trabajos:</b> las clases completadas, las entregas y los bocetos se guardan en tu navegador.</li>
      <li><b>Asistente de IA:</b> las preguntas que le hacés y las imágenes que mandás a corregir se procesan para responderte y no se usan para otros fines.</li>
      <li><b>Solicitudes:</b> si usás el Botón de arrepentimiento o el de baja, guardamos los datos que completes para darles curso.</li>
    </ul>
    <h2>Para qué los usamos</h2>
    <p>Para darte acceso a las diplomaturas que contrataste, cobrar las cuotas, responder tus consultas y cumplir obligaciones legales. No vendemos ni compartimos tus datos con terceros, salvo con los proveedores necesarios para prestar el servicio (Google para el ingreso, Mercado Pago para los pagos y Cloudflare para alojar el sitio).</p>
    <h2>Cuánto tiempo los guardamos</h2>
    <p>Mientras tengas una cuenta o una suscripción, y después el tiempo que exijan las normas contables y de defensa del consumidor.</p>
    <h2>Tus derechos</h2>
    <p>Podés pedir acceso, rectificación o supresión de tus datos escribiéndonos por el formulario de <a href="/baja.html">baja</a> o a <a href="mailto:hola@bocetoo.app">hola@bocetoo.app</a>. La Agencia de Acceso a la Información Pública, órgano de control de la Ley 25.326, atiende las denuncias y reclamos de quienes vean afectados sus derechos.</p>
    <h2>Cookies</h2>
    <p>Usamos una sola cookie necesaria para mantener tu sesión iniciada. No usamos cookies de publicidad.</p>'''

TERMINOS = '''    <p>Al inscribirte en boceto aceptás estas condiciones. Por cualquier consulta escribinos a <a href="mailto:hola@bocetoo.app">hola@bocetoo.app</a>.</p>
    <h2>El servicio</h2>
    <p>boceto ofrece diplomaturas online de Diseño de Interiores y Mobiliario, Industrial, Gráfico e Indumentaria, con clases, ejercicios, un asistente de IA y un bocetador. Las diplomaturas son cursos libres y no otorgan un título oficial.</p>
    <h2>Precios y pagos</h2>
    <ul>
      <li>"Tu diplomatura": cuota mensual de $63.000 durante 4 meses. "Todas las diplomaturas": cuota mensual de $83.000 mientras la suscripción esté activa.</li>
      <li>Matrícula única de $45.000, que se abona una sola vez.</li>
      <li>Las cuotas se debitan automáticamente por Mercado Pago. Si una cuota no se puede cobrar, el acceso a las clases se suspende hasta regularizarla.</li>
    </ul>
    <h2>Arrepentimiento y baja</h2>
    <p>Podés revocar la contratación dentro de los 10 días corridos con el <a href="/arrepentimiento.html">Botón de arrepentimiento</a>, y pedir la baja en cualquier momento con el <a href="/baja.html">Botón de baja de servicio</a> o desde la página de inscripción. Desde la baja no se cobran nuevas cuotas.</p>
    <h2>Tu cuenta</h2>
    <p>La cuenta es personal: el acceso a las clases es para quien se inscribió. Lo que produzcas en el sitio es tuyo.</p>
    <h2>Cambios</h2>
    <p>Si cambiamos estas condiciones o los precios, te avisaremos antes de que se apliquen a tu suscripción.</p>'''

for nombre, titulo, desc, cuerpo in [
    ("privacidad.html", "Política de privacidad", "Cómo trata boceto tus datos personales.", PRIVACIDAD),
    ("terminos.html", "Términos y condiciones", "Condiciones de uso y de contratación de las diplomaturas de boceto.", TERMINOS),
]:
    import sys; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import layout
    (PUB / nombre).write_text(layout.migrar(BASE.format(titulo=titulo, descripcion=desc, cuerpo=cuerpo).replace('class="i-card legal"', 'class="i-card i-legal-txt"')), encoding="utf-8")
    print("ok", nombre)

