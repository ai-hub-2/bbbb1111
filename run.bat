@echo off
chcp 65001 >nul

REM 🔵 ملف تشغيل تطبيق العلامة الزرقاء للويندوز
REM Blue Badge Application Runner for Windows

echo 🔵 تطبيق العلامة الزرقاء الشامل
echo Blue Badge Complete Application
echo ==================================================

REM التحقق من وجود البيئة الافتراضية
if not exist "venv" (
    echo ❌ البيئة الافتراضية غير موجودة
    echo 🚀 إنشاء بيئة افتراضية جديدة...
    python -m venv venv
)

REM تفعيل البيئة الافتراضية
echo 🔧 تفعيل البيئة الافتراضية...
call venv\Scripts\activate.bat

REM التحقق من المكتبات
echo 📦 التحقق من المكتبات...
python -c "import tkinter, requests, dns.resolver, bs4, lxml" 2>nul
if errorlevel 1 (
    echo ⚠️ بعض المكتبات مفقودة
    echo 📥 تثبيت المكتبات المطلوبة...
    pip install -r requirements.txt
)

REM تشغيل التطبيق
echo 🚀 بدء تشغيل التطبيق...
echo ==================================================

REM تشغيل التطبيق الرئيسي
python main.py

REM في حالة حدوث خطأ
if errorlevel 1 (
    echo ❌ حدث خطأ في تشغيل التطبيق
    echo 🔧 محاولة تشغيل التطبيق مباشرة...
    python blue_badge_app.py
)

pause