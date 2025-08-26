#!/bin/bash

# 🚀 تشغيل فوري للتطبيق السحابي
# Instant Cloud App Launcher

echo "🔵 تشغيل التطبيق السحابي..."
echo "Cloud App Starting..."
echo "=================================================="

# التحقق من وجود البيئة الافتراضية
if [ ! -d "venv_cloud" ]; then
    echo "❌ البيئة الافتراضية غير موجودة"
    echo "🚀 إنشاء بيئة افتراضية جديدة..."
    python3 -m venv venv_cloud
fi

# تفعيل البيئة الافتراضية
echo "🔧 تفعيل البيئة الافتراضية..."
source venv_cloud/bin/activate

# التحقق من المكتبات
echo "📦 التحقق من المكتبات..."
if ! python3 -c "import streamlit, pandas, plotly" 2>/dev/null; then
    echo "⚠️ بعض المكتبات مفقودة"
    echo "📥 تثبيت المكتبات المطلوبة..."
    pip install streamlit pandas plotly
fi

# إيقاف أي عمليات streamlit سابقة
echo "🔄 إيقاف العمليات السابقة..."
pkill -f streamlit 2>/dev/null
sleep 2

# تشغيل التطبيق
echo "🚀 بدء تشغيل التطبيق السحابي..."
echo "=================================================="
echo "🌐 التطبيق سيكون متاحاً على: http://localhost:8501"
echo "📱 يمكنك الوصول إليه من أي متصفح"
echo "🔄 اضغط Ctrl+C لإيقاف التطبيق"
echo "=================================================="

# تشغيل Streamlit
streamlit run cloud_app.py --server.port 8501 --server.address 0.0.0.0