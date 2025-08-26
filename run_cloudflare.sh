#!/bin/bash

# 🚀 ملف تشغيل التطبيق المتوافق مع Cloudflare
# Cloudflare Compatible App Runner

echo "🔵 تطبيق العلامة الزرقاء - Cloudflare Compatible"
echo "Blue Badge Application - Cloudflare Compatible"
echo "=================================================="

# التحقق من وجود البيئة الافتراضية
if [ ! -d "venv_cloudflare" ]; then
    echo "❌ البيئة الافتراضية لـ Cloudflare غير موجودة"
    echo "🚀 إنشاء بيئة افتراضية جديدة..."
    python3 -m venv venv_cloudflare
fi

# تفعيل البيئة الافتراضية
echo "🔧 تفعيل البيئة الافتراضية لـ Cloudflare..."
source venv_cloudflare/bin/activate

# التحقق من المكتبات
echo "📦 التحقق من المكتبات..."
if ! python3 -c "import streamlit, pandas, plotly" 2>/dev/null; then
    echo "⚠️ بعض المكتبات مفقودة"
    echo "📥 تثبيت المكتبات المطلوبة..."
    pip install -r requirements_cloudflare.txt
fi

# إيقاف أي عمليات streamlit سابقة
echo "🔄 إيقاف العمليات السابقة..."
pkill -f streamlit 2>/dev/null
sleep 2

# تشغيل التطبيق
echo "🚀 بدء تشغيل التطبيق المتوافق مع Cloudflare..."
echo "=================================================="
echo "🌐 التطبيق سيكون متاحاً على: http://localhost:8501"
echo "📱 يمكنك الوصول إليه من أي متصفح"
echo "☁️ متوافق مع Cloudflare Pages"
echo "🔄 اضغط Ctrl+C لإيقاف التطبيق"
echo "=================================================="

# تشغيل Streamlit مع إعدادات Cloudflare
CLOUDFLARE_PAGES=true streamlit run cloudflare_app.py --server.port 8501 --server.address 0.0.0.0