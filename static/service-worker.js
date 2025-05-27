const CACHE_NAME = 'chatbot-cache-v1';
const urlsToCache = [
  '/',
  '/static/manifest.json',
  '/static/styles.css',    // optional: if you have it
  '/static/logo.png',      // optional: if you have it
];

// Install service worker and cache assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting(); // force activation on install
});

// Activate and remove old caches (optional but good practice)
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME)
            .map(key => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

// Intercept fetch requests
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Don't cache POST requests or chat endpoint
  if (event.request.method !== 'GET' || url.pathname === '/chat') {
    return;
  }

  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    }).catch(() => {
      return new Response('Offline', {
        status: 503,
        statusText: 'Offline',
      });
    })
  );
});
