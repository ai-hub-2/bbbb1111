// Register service worker for PWA
if ('serviceWorker' in navigator) {
	navigator.serviceWorker.register('/web/sw.js').catch(() => {});
}

let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
	e.preventDefault();
	deferredPrompt = e;
	const btn = document.getElementById('installBtn');
	btn.disabled = false;
	btn.addEventListener('click', async () => {
		if (!deferredPrompt) return;
		deferredPrompt.prompt();
		await deferredPrompt.userChoice;
		deferredPrompt = null;
		btn.disabled = true;
	});
});

// Start app via Termux (Android intent)
document.getElementById('startBtn').addEventListener('click', () => {
	// Attempt to launch Termux via intent URL
	// Fallback: show instructions if not Android
	const ua = navigator.userAgent || '';
	const isAndroid = /Android/i.test(ua);
	if (!isAndroid) {
		alert('زر التشغيل يدعم أندرويد فقط. افتح هذه الصفحة من هاتف أندرويد.');
		return;
	}
	// Intent to open Termux app
	const intent = 'intent://#Intent;scheme=termux;package=com.termux;end';
	window.location.href = intent;
	// Optional: After small delay, suggest installing Termux if not present
	setTimeout(() => {
		if (document.visibilityState === 'visible') {
			alert('تأكد من تثبيت Termux ثم أعد المحاولة.');
		}
	}, 1500);
});