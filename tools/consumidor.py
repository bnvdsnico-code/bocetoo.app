"""Genera las páginas "Botón de arrepentimiento" y "Botón de baja de servicio" y pone los dos botones
visibles arriba de cada página de entrada (portada, fichas, inscripción y panel). Se puede volver a correr."""
import pathlib

PUB = pathlib.Path(__file__).resolve().parent.parent / "public"

PAGINA = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titulo} · boceto</title>
<meta name="description" content="{descripcion}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/inscripcion.css">
</head>
<body>
<header class="i-top">
  <a class="i-brand" href="/"><span class="marks" aria-hidden="true"><i></i><i></i><i></i><i></i></span><b>boceto</b></a>
  <a href="/">Volver al inicio</a>
</header>
<main class="i-main">
  <section class="i-intro">
    <p class="i-kick">Defensa del consumidor</p>
    <h1>{titulo}</h1>
    <p>{intro}</p>
  </section>
  <section class="i-card" aria-labelledby="form-t">
    <h2 id="form-t">Tus datos</h2>
    <form id="solicitud" novalidate>
      <input type="hidden" name="tipo" value="{tipo}">
      <div class="i-field"><label for="nombre">Nombre y apellido</label><input id="nombre" name="nombre" autocomplete="name" required></div>
      <div class="i-field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
      <div class="i-field"><label for="dni">DNI (opcional)</label><input id="dni" name="dni" inputmode="numeric" autocomplete="off"></div>
      <div class="i-field"><label for="detalle">{detalle_label}</label><textarea id="detalle" name="detalle" rows="3" style="font:inherit;font-weight:400;font-size:16px;padding:12px 14px;border:1.5px solid #CFCFCF;border-radius:12px"></textarea></div>
      <button type="submit" class="i-cta" id="enviar">{boton}</button>
      <p class="i-legal">{legal}</p>
    </form>
    <div id="resultado" class="i-alert" role="status" hidden></div>
  </section>
</main>
<script>
  (() => {{
    const form = document.getElementById("solicitud"), out = document.getElementById("resultado"), btn = document.getElementById("enviar");
    form.addEventListener("submit", async (e) => {{
      e.preventDefault(); if (btn.disabled) return;
      const datos = Object.fromEntries(new FormData(form));
      btn.disabled = true; btn.textContent = "Enviando…"; out.hidden = true;
      try {{
        const r = await fetch("/api/solicitudes", {{ method: "POST", headers: {{ "content-type": "application/json" }}, body: JSON.stringify(datos) }});
        const d = await r.json().catch(() => ({{}}));
        if (!r.ok || !d.codigo) throw new Error(d.message || "No pudimos registrar la solicitud. Intentá nuevamente.");
        form.hidden = true; out.className = "i-alert ok";
        out.textContent = "✓ Recibimos tu solicitud. Tu código de identificación es " + d.codigo + ". Guardalo: {confirmacion}";
      }} catch (err) {{ out.className = "i-alert error"; out.textContent = err.message; btn.disabled = false; btn.textContent = "{boton}"; }}
      out.hidden = false;
    }});
  }})();
</script>
</body>
</html>
'''

PAGINAS = {
    "arrepentimiento.html": dict(
        tipo="arrepentimiento", titulo="Botón de arrepentimiento",
        descripcion="Revocá tu inscripción en boceto dentro de los 10 días corridos, sin registrarte.",
        intro="Podés revocar la aceptación de tu inscripción dentro de los 10 días corridos desde que te inscribiste o pagaste, sin dar explicaciones y sin costo (art. 34 de la Ley 24.240 y art. 1110 del Código Civil y Comercial). No hace falta registrarte ni iniciar sesión.",
        detalle_label="¿Qué querés revocar? (opcional: diplomatura, fecha o número de pago)",
        boton="Enviar arrepentimiento",
        legal="Te devolvemos lo abonado por el mismo medio de pago y cancelamos la suscripción.",
        confirmacion="en las próximas 24 horas damos curso a la revocación y te escribimos al email que dejaste."),
    "baja.html": dict(
        tipo="baja", titulo="Botón de baja de servicio",
        descripcion="Pedí la baja de tu suscripción a boceto, sin registrarte.",
        intro="Pedí la baja de tu suscripción a una diplomatura de boceto. No hace falta registrarte ni iniciar sesión, y no se te cobran más cuotas desde la baja (art. 10 ter de la Ley 24.240).",
        detalle_label="¿Qué suscripción querés dar de baja? (opcional)",
        boton="Pedir la baja",
        legal="Si te suscribiste desde este navegador, también podés cancelar al instante desde la página de inscripción.",
        confirmacion="en las próximas 24 horas hacemos efectiva la baja y te escribimos al email que dejaste."),
}

import sys; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import layout
for nombre, d in PAGINAS.items():
    (PUB / nombre).write_text(layout.migrar(PAGINA.format(**d)), encoding="utf-8")
    print("ok", nombre)

# La franja con los botones ya está en el encabezado común (tools/layout.py).
