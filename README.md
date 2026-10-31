# boceto: escuela de diseño online

Sitio estático con una función para el asistente de IA. Se publica en Cloudflare Pages (también funciona en Netlify).

## Estructura

```
public/                       lo que se publica
  index.html                  landing
  cursos/                     fichas: interiores, industrial, grafico, indumentaria
  aprender/                   lección de ejemplo y devolución del asistente
  panel.html                  panel del alumno
  bocetador/                  programa de dibujo asistido
  assets/                     site.css, site.js, favicon
  404.html
functions/api/asistente.ts    POST /api/asistente en Cloudflare Pages (Workers AI o Claude)
wrangler.toml                 configuración de Cloudflare Pages
public/_headers, _redirects   encabezados y redirecciones en Cloudflare
netlify/functions/            versión para Netlify del mismo asistente
netlify.toml                  configuración de Netlify
tools/                        scripts para regenerar y probar (no se publican)
```

## Asistente de IA

`/api/asistente` usa el AI Gateway de Netlify: no hace falta cargar una clave de Anthropic.
El Gateway se activa después del primer deploy a producción, en planes con créditos (Free, Personal o Pro).
Cada consulta consume créditos de la cuenta de Netlify. La función limita a 20 consultas por minuto por visitante.
Para usar otro modelo, crear la variable de entorno `ASISTENTE_MODEL` en Netlify.

## Probar localmente

```
python3 tools/test_site.py      # prueba de punta a punta con Playwright, asistente simulado
```

## Publicar

Opción A, desde la web: en app.netlify.com, abrir el proyecto boceto-escuela-diseno → Deploys →
arrastrar esta carpeta completa (la que contiene netlify.toml).

Opción B, con Node instalado:

```
npx netlify-cli deploy --prod --site 327006dc-8a67-464a-8449-fe1ad0723827
```

## Cloudflare Pages

Conectar el repositorio de GitHub en Cloudflare: Workers y Pages → Crear → Pages → Conectar a Git.
- Framework: ninguno. Comando de compilación: vacío. Directorio de salida: `public`.
- Cada cambio que se sube a la rama `main` se publica solo.

El asistente usa Workers AI (incluido en el plan gratis, sin tarjeta), a través del binding `AI` de `wrangler.toml`.
Si más adelante se carga la variable `ANTHROPIC_API_KEY` en Cloudflare (Settings → Variables and Secrets), pasa a responder con Claude
y vuelve a Workers AI si Claude no está disponible.

## Suscripciones con Mercado Pago

- Página de inscripción: `/inscripcion.html` (los botones "Inscribirme" de las fichas y los planes del inicio llevan ahí).
- Servidor: `src/suscripciones.ts` (rutas `/api/mp-config`, `/api/subscriptions`, `/api/subscriptions/:id`, `/api/subscriptions/:id/{pause|reactivate|cancel}`).
- Planes: los crea el Worker solo (tarea programada cada 15 minutos) en cuanto está cargada la credencial; sus IDs quedan en el KV `SUSCRIPCIONES`. `/api/estado-pagos` muestra qué falta.
- Secretos en Cloudflare (Worker → Settings → Variables and Secrets): `MP_ACCESS_TOKEN`, `MP_PUBLIC_KEY` y, después, `MP_WEBHOOK_SECRET`. Plantilla en `.env.example`.

### Webhook de Mercado Pago

- Receptor: `POST /api/mp/webhook` (`src/webhook.ts`). Valida la firma `x-signature` con el secreto de webhooks, responde 200 y procesa después.
- Temas: `subscription_preapproval` (estado de la suscripción), `subscription_authorized_payment` (cobro de cada cuota) y `payment`.
- Avisos: cada pedido de baja o arrepentimiento, suscripción nueva o cancelación manda un email desde avisos@bocetoo.app a bnvds.nico@gmail.com (Email Routing, `[[send_email]]` en wrangler.toml).
- En Mercado Pago: Tus integraciones → bocetoo app → Webhooks → URL `https://bocetoo-app.bnvds-nico.workers.dev/api/mp/webhook` (también funciona `https://bocetoo.app/api/mp/webhook`). El sitio vive en https://bocetoo.app; la dirección de workers.dev redirige ahí salvo /api.

### Matrícula (Checkout Pro)

- Después de suscribirse, el alumno ve "Pagar matrícula con Mercado Pago" en `/inscripcion.html` ($45.000, pago único con cualquier medio).
- Servidor: `src/matricula.ts` (`POST /api/matricula` crea la preferencia; `POST /api/matricula/confirmar` verifica el pago al volver). El webhook `payment` también la marca como paga.

### Botón de arrepentimiento y Botón de baja de servicio

- Páginas `/arrepentimiento.html` y `/baja.html` (generadas por `tools/consumidor.py`), con enlaces visibles arriba de la portada, fichas, inscripción y panel.
- Sin registro: el consumidor completa nombre y email y recibe en pantalla un código de identificación (`ARR-…` / `BAJ-…`).
- Las solicitudes quedan en Cloudflare → Workers KV → `bocetoo-suscripciones`, claves `solicitud:…`. Hay que darles curso dentro de las 24 horas.

### Cuentas de alumno (Google) y acceso a las clases

- Ingreso con Google (`src/auth.ts`): `/auth/google` → Google → `/auth/callback`; sesión en cookie segura y en KV (`sess:…`), 30 días. `/auth/salir` cierra la sesión.
- Para suscribirse hay que ingresar: la suscripción queda asociada al email de Google (`email:<email>` → ids).
- Clases: la primera de cada diplomatura es libre; el resto requiere una suscripción `authorized` que la incluya. Si no, se redirige a `/acceso.html`.
- Configuración: `GOOGLE_CLIENT_ID` (variable) y `GOOGLE_CLIENT_SECRET` (secreto) en Cloudflare. URI de redirección autorizada en Google: `https://<dominio>/auth/callback`.

## SEO
- `python3 tools/kb.py` regenera la base de conocimiento del asistente (`src/conocimiento.json`, un índice de las 320 clases) y `content/fuentes/referentes.md`. Correrlo después de cambiar cualquier clase: el asistente busca ahí las clases que responden cada pregunta.
- `python3 tools/seo.py` agrega canonical, Open Graph, datos estructurados y noindex, y regenera `sitemap.xml` y `robots.txt`. Correrlo después de cualquier `build_curso.py` o `legales.py`.
- `python3 tools/og.py <carpeta @fontsource>` regenera las imágenes para compartir (`public/assets/og/`).

## Administración
- https://bocetoo.app/admin: solo para las cuentas de Google en la variable `ADMINS` (por defecto bnvds.nico@gmail.com). Muestra alumnos, suscripciones, cuotas, matrícula, avance, certificados y los pedidos de baja/arrepentimiento (se marcan como atendidos).
