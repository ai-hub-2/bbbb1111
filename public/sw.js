// 🔥🔥🔥 Service Worker للتطبيق الخارق! 🔥🔥🔥
// Service Worker for the SUPER APP!

const CACHE_NAME = 'blue-badge-app-v3.0.0';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/css/style.css',
  '/js/app.js',
  '/js/tools.js',
  '/js/dns-tool.js',
  '/js/mail-tool.js',
  '/js/phone-tool.js',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
];

// تثبيت Service Worker
self.addEventListener('install', (event) => {
  console.log('🚀 Service Worker: Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('✅ Service Worker: Cache opened');
        return cache.addAll(urlsToCache);
      })
      .then(() => {
        console.log('✅ Service Worker: All resources cached');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('❌ Service Worker: Cache failed:', error);
      })
  );
});

// تفعيل Service Worker
self.addEventListener('activate', (event) => {
  console.log('🚀 Service Worker: Activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('🗑️ Service Worker: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('✅ Service Worker: Activated');
      return self.clients.claim();
    })
  );
});

// اعتراض الطلبات
self.addEventListener('fetch', (event) => {
  console.log('🔍 Service Worker: Fetching:', event.request.url);
  
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // إرجاع من الكاش إذا وجد
        if (response) {
          console.log('✅ Service Worker: Served from cache:', event.request.url);
          return response;
        }
        
        // محاولة جلب من الشبكة
        return fetch(event.request)
          .then((response) => {
            // التحقق من أن الاستجابة صالحة
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            // نسخ الاستجابة
            const responseToCache = response.clone();
            
            // إضافة للكاش
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
                console.log('💾 Service Worker: Cached new resource:', event.request.url);
              });
            
            return response;
          })
          .catch(() => {
            // إرجاع صفحة offline إذا فشل الاتصال
            if (event.request.mode === 'navigate') {
              return caches.match('/offline.html');
            }
          });
      })
  );
});

// معالجة الرسائل
self.addEventListener('message', (event) => {
  console.log('📨 Service Worker: Message received:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME });
  }
});

// معالجة الإشعارات
self.addEventListener('push', (event) => {
  console.log('🔔 Service Worker: Push notification received');
  
  const options = {
    body: event.data ? event.data.text() : '🔵 التطبيق الخارق للعلامة الزرقاء',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'استكشاف',
        icon: '/icons/icon-72x72.png'
      },
      {
        action: 'close',
        title: 'إغلاق',
        icon: '/icons/icon-72x72.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('🔵 التطبيق الخارق', options)
  );
});

// معالجة النقر على الإشعارات
self.addEventListener('notificationclick', (event) => {
  console.log('👆 Service Worker: Notification clicked');
  
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// معالجة التحديثات
self.addEventListener('sync', (event) => {
  console.log('🔄 Service Worker: Background sync:', event.tag);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

// مزامنة في الخلفية
async function doBackgroundSync() {
  try {
    console.log('🔄 Service Worker: Performing background sync...');
    
    // تحديث البيانات
    const response = await fetch('/api/update-data');
    const data = await response.json();
    
    console.log('✅ Service Worker: Background sync completed');
    
    // إرسال إشعار
    self.registration.showNotification('🔄 تم التحديث', {
      body: 'تم تحديث البيانات بنجاح',
      icon: '/icons/icon-192x192.png'
    });
    
  } catch (error) {
    console.error('❌ Service Worker: Background sync failed:', error);
  }
}

// معالجة الأخطاء
self.addEventListener('error', (event) => {
  console.error('❌ Service Worker: Error:', event.error);
});

// معالجة الرفض
self.addEventListener('unhandledrejection', (event) => {
  console.error('❌ Service Worker: Unhandled rejection:', event.reason);
});

console.log('🚀 Service Worker: Loaded successfully!');