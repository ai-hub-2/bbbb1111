// PWA: service worker
if ('serviceWorker' in navigator) {
	navigator.serviceWorker.register('/web/sw.js').catch(() => {});
}

const statusEl = document.getElementById('status');
function setStatus(msg) { statusEl.textContent = msg || ''; }

// Detect if already installed
const isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone;
if (isStandalone) setStatus('التطبيق مثبت ويعمل في نمط مستقل.');

let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
	e.preventDefault();
	deferredPrompt = e;
	const btn = document.getElementById('installBtn');
	btn.disabled = false;
	btn.addEventListener('click', async () => {
		try {
			setStatus('جارٍ طلب التثبيت...');
			deferredPrompt.prompt();
			const choice = await deferredPrompt.userChoice;
			if (choice && choice.outcome === 'accepted') setStatus('تم قبول التثبيت. ابحث عن الأيقونة على الشاشة الرئيسية.');
			else setStatus('تم إلغاء التثبيت من قبل المستخدم.');
		} catch (_) {
			setStatus('تعذر بدء التثبيت.');
		} finally {
			deferredPrompt = null;
			btn.disabled = true;
		}
	});
});

window.addEventListener('appinstalled', () => setStatus('تم تثبيت التطبيق بنجاح.'));

// Start app via Termux (Android intent)
document.getElementById('startBtn').addEventListener('click', () => {
	const ua = navigator.userAgent || '';
	const isAndroid = /Android/i.test(ua);
	if (!isAndroid) {
		setStatus('زر التشغيل يدعم أندرويد فقط.');
		return;
	}
	const intent = 'intent://#Intent;scheme=termux;package=com.termux;end';
	window.location.href = intent;
	setTimeout(() => {
		if (document.visibilityState === 'visible') setStatus('تأكد من تثبيت Termux ثم أعد المحاولة.');
	}, 1200);
});