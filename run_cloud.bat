@echo off
chcp 65001 >nul

REM 🔵 ملف تشغيل التطبيق السحابي للويندوز
REM Cloud Blue Badge Application Runner for Windows

echo 🔵 تطبيق العلامة الزرقاء السحابي
echo Cloud Blue Badge Application
echo ==================================================

REM التحقق من وجود البيئة الافتراضية
if not exist "venv_cloud" (
    echo ❌ البيئة الافتراضية السحابية غير موجودة
    echo 🚀 إنشاء بيئة افتراضية سحابية جديدة...
    python -m venv venv_cloud
)

REM تفعيل البيئة الافتراضية
echo 🔧 تفعيل البيئة الافتراضية السحابية...
call venv_cloud\Scripts\activate.bat

REM التحقق من المكتبات السحابية
echo 📦 التحقق من المكتبات السحابية...
python -c "import streamlit, pandas, plotly" 2>nul
if errorlevel 1 (
    echo ⚠️ بعض المكتبات السحابية مفقودة
    echo 📥 تثبيت المكتبات السحابية المطلوبة...
    pip install -r requirements_cloud.txt
)

REM تشغيل التطبيق السحابي
echo 🚀 بدء تشغيل التطبيق السحابي...
echo ==================================================
echo 🌐 التطبيق سيكون متاحاً على: http://localhost:8501
echo 📱 يمكنك الوصول إليه من أي متصفح
echo 🔄 اضغط Ctrl+C لإيقاف التطبيق
echo ==================================================

REM تشغيل Streamlit
streamlit run cloud_app.py --server.port 8501 --server.address 0.0.0.0

pause