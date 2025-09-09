// AgriAssist Service Worker
const CACHE_NAME = 'agriassist-v1.0.0';
const OFFLINE_URL = '/offline.html';

// Files to cache for offline functionality
const CACHE_URLS = [
  '/',
  '/index.html',
  '/pages/homepage_ai_query_interface.html',
  '/pages/knowledge_base_crop_season_guide.html',
  '/pages/community_hub_farmer_network.html',
  '/pages/expert_network_agricultural_officer_connect.html',
  '/pages/my_farm_dashboard_personalized_advisor.html',
  '/pages/crop_calculator_profit_analyzer.html',
  '/pages/help_support_multilingual_assistance.html',
  '/css/main.css',
  '/css/tailwind.css',
  '/public/manifest.json',
  '/public/favicon.ico'
];

// Install event - cache resources
self.addEventListener('install', event => {
  console.log('Service Worker: Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: Caching files');
        return cache.addAll(CACHE_URLS);
      })
      .then(() => {
        console.log('Service Worker: Installation complete');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('Service Worker: Installation failed', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('Service Worker: Activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: Deleting old cache', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('Service Worker: Activation complete');
      return self.clients.claim();
    })
  );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  // Skip external requests
  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached version if available
        if (response) {
          console.log('Service Worker: Serving from cache', event.request.url);
          return response;
        }

        // Otherwise fetch from network
        return fetch(event.request)
          .then(response => {
            // Check if valid response
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone the response
            const responseToCache = response.clone();

            // Add to cache for future use
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return response;
          })
          .catch(error => {
            console.log('Service Worker: Network request failed', error);
            
            // Return offline page for navigation requests
            if (event.request.destination === 'document') {
              return caches.match(OFFLINE_URL);
            }
            
            // Return a basic offline response for other requests
            return new Response('Offline content not available', {
              status: 503,
              statusText: 'Service Unavailable',
              headers: new Headers({
                'Content-Type': 'text/plain'
              })
            });
          });
      })
  );
});

// Background sync for offline data
self.addEventListener('sync', event => {
  console.log('Service Worker: Background sync', event.tag);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

// Push notification handling
self.addEventListener('push', event => {
  console.log('Service Worker: Push notification received');
  
  const options = {
    body: event.data ? event.data.text() : 'New farming advice available!',
    icon: '/public/favicon.ico',
    badge: '/public/favicon.ico',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'View Details',
        icon: '/public/favicon.ico'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/public/favicon.ico'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('AgriAssist', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
  console.log('Service Worker: Notification clicked');
  
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/pages/homepage_ai_query_interface.html')
    );
  } else if (event.action === 'close') {
    // Just close the notification
    return;
  } else {
    // Default action - open the app
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Background sync function
async function doBackgroundSync() {
  try {
    // Sync offline queries when back online
    const offlineQueries = await getOfflineQueries();
    
    for (const query of offlineQueries) {
      try {
        await syncQuery(query);
        await removeOfflineQuery(query.id);
      } catch (error) {
        console.error('Service Worker: Failed to sync query', error);
      }
    }
    
    console.log('Service Worker: Background sync complete');
  } catch (error) {
    console.error('Service Worker: Background sync failed', error);
  }
}

// Helper functions for offline data management
async function getOfflineQueries() {
  // This would typically read from IndexedDB
  // For now, return empty array
  return [];
}

async function syncQuery(query) {
  // Send query to server when back online
  const response = await fetch('/api/ask', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ question: query.question })
  });
  
  if (response.ok) {
    const data = await response.json();
    // Store response for user to see when they return
    await storeOfflineResponse(query.id, data.answer);
  }
}

async function removeOfflineQuery(id) {
  // Remove synced query from offline storage
  console.log('Service Worker: Removing synced query', id);
}

async function storeOfflineResponse(queryId, response) {
  // Store response for offline viewing
  console.log('Service Worker: Storing offline response', queryId);
}

// Message handling for communication with main thread
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME });
  }
});

console.log('Service Worker: Script loaded');
