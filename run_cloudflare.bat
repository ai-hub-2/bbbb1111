@echo off
chcp 65001 >nul

REM 🚀 ملف تشغيل التطبيق المتوافق مع Cloudflare للويندوز
REM Cloudflare Compatible App Runner for Windows

echo 🔵 تطبيق العلامة الزرقاء - Cloudflare Compatible
echo Blue Badge Application - Cloudflare Compatible
echo ==================================================

REM التحقق من وجود البيئة الافتراضية
if not exist "venv_cloudflare" (
    echo ❌ البيئة الافتراضية لـ Cloudflare غير موجودة
    echo 🚀 إنشاء بيئة افتراضية جديدة...
    python -m venv venv_cloudflare
)

REM تفعيل البيئة الافتراضية
echo 🔧 تفعيل البيئة الافتراضية لـ Cloudflare...
call venv_cloudflare\Scripts\activate.bat

REM التحقق من المكتبات
echo 📦 التحقق من المكتبات...
python -c "import streamlit, pandas, plotly" 2>nul
if errorlevel 1 (
    echo ⚠️ بعض المكتبات مفقودة
    echo 📥 تثبيت المكتبات المطلوبة...
    pip install -r requirements_cloudflare.txt
)

REM إيقاف أي عمليات streamlit سابقة
echo 🔄 إيقاف العمليات السابقة...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

REM تشغيل التطبيق
echo 🚀 بدء تشغيل التطبيق المتوافق مع Cloudflare...
echo ==================================================
echo 🌐 التطبيق سيكون متاحاً على: http://localhost:8501
echo 📱 يمكنك الوصول إليه من أي متصفح
echo ☁️ متوافق مع Cloudflare Pages
echo 🔄 اضغط Ctrl+C لإيقاف التطبيق
echo ==================================================

REM تشغيل Streamlit مع إعدادات Cloudflare
set CLOUDFLARE_PAGES=true
streamlit run cloudflare_app.py --server.port 8501 --server.address 0.0.0.0

pause