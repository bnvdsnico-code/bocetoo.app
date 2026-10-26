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
