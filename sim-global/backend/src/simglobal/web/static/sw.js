// Service worker mínimo — cacheia estáticos. Pré-cache pode crescer
// conforme o app evoluir; por ora, apenas runtime cache.
const CACHE = "simglobal-v1";
const PRECACHE = ["/static/css/main.css", "/static/js/main.js", "/static/manifest.json"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  // API responses sempre da rede (estado de jogo é dinâmico).
  if (url.pathname.startsWith("/api/")) return;
  // Estáticos: cache-first.
  if (url.pathname.startsWith("/static/")) {
    event.respondWith(
      caches.match(event.request).then((hit) =>
        hit || fetch(event.request).then((resp) => {
          const copy = resp.clone();
          caches.open(CACHE).then((c) => c.put(event.request, copy));
          return resp;
        })
      )
    );
  }
});
