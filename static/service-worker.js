const CACHE_NAME = 'chatbot-cache-v1';
const urlsToCache = [
  '/',
  '/static/manifest.json',
  '/static/styles.css', // if you have it
  '/static/logo.png',   // if you use any icons
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Don't cache POST requests or dynamic data like /chat
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
