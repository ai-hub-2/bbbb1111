#!/bin/bash

# 🔵 ملف تشغيل التطبيق السحابي
# Cloud Blue Badge Application Runner

echo "🔵 تطبيق العلامة الزرقاء السحابي"
echo "Cloud Blue Badge Application"
echo "=================================================="

# التحقق من وجود البيئة الافتراضية
if [ ! -d "venv_cloud" ]; then
    echo "❌ البيئة الافتراضية السحابية غير موجودة"
    echo "🚀 إنشاء بيئة افتراضية سحابية جديدة..."
    python3 -m venv venv_cloud
fi

# تفعيل البيئة الافتراضية
echo "🔧 تفعيل البيئة الافتراضية السحابية..."
source venv_cloud/bin/activate

# التحقق من المكتبات السحابية
echo "📦 التحقق من المكتبات السحابية..."
if ! python3 -c "import streamlit, pandas, plotly" 2>/dev/null; then
    echo "⚠️ بعض المكتبات السحابية مفقودة"
    echo "📥 تثبيت المكتبات السحابية المطلوبة..."
    pip install -r requirements_cloud.txt
fi

# تشغيل التطبيق السحابي
echo "🚀 بدء تشغيل التطبيق السحابي..."
echo "=================================================="
echo "🌐 التطبيق سيكون متاحاً على: http://localhost:8501"
echo "📱 يمكنك الوصول إليه من أي متصفح"
echo "🔄 اضغط Ctrl+C لإيقاف التطبيق"
echo "=================================================="

# تشغيل Streamlit
streamlit run cloud_app.py --server.port 8501 --server.address 0.0.0.0