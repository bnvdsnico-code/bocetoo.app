// Service worker del Bocetador: lo deja instalable y usable sin conexión.
// La hoja se guarda en el navegador; la corrección del asistente y la sincronización necesitan internet.
const VERSION = "bocetador-1.0-r3"; // versión visible 1.0; el sufijo renueva la caché en cada publicación
const PRECARGA = [
  "/bocetador/",
  "/assets/sync.js",
  "/assets/favicon.svg",
  "/bocetador/manifest.webmanifest",
  "/bocetador/icons/icono-192.png",
  "/bocetador/icons/icono-512.png"
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(PRECARGA)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k.startsWith("bocetador-") && k !== VERSION).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  // Nunca se guardan respuestas de la cuenta, pagos o el asistente
  if (url.origin === location.origin && (url.pathname.startsWith("/api/") || url.pathname.startsWith("/auth/"))) return;

  // La página del Bocetador: primero la red (para tener siempre la última versión), si no hay conexión, la guardada
  if (req.mode === "navigate" && url.pathname.startsWith("/bocetador")) {
    e.respondWith(fetch(req).then((r) => { const copia = r.clone(); caches.open(VERSION).then((c) => c.put("/bocetador/", copia)); return r; })
      .catch(() => caches.match("/bocetador/", { ignoreSearch: true })));
    return;
  }

  // Consignas de las clases, archivos propios y tipografías: lo guardado al instante y se actualiza por detrás
  const propio = url.origin === location.origin && (url.pathname.startsWith("/assets/") || url.pathname.startsWith("/bocetador/") || url.pathname.endsWith("/consignas.json"));
  const fuente = url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com";
  if (!propio && !fuente) return;
  e.respondWith(caches.open(VERSION).then(async (c) => {
    const guardado = await c.match(req);
    const red = fetch(req).then((r) => { if (r.ok || r.type === "opaque") c.put(req, r.clone()); return r; }).catch(() => guardado);
    return guardado || red;
  }));
});
