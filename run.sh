#!/bin/bash

# 🔵 ملف تشغيل تطبيق العلامة الزرقاء
# Blue Badge Application Runner

echo "🔵 تطبيق العلامة الزرقاء الشامل"
echo "Blue Badge Complete Application"
echo "=================================================="

# التحقق من وجود البيئة الافتراضية
if [ ! -d "venv" ]; then
    echo "❌ البيئة الافتراضية غير موجودة"
    echo "🚀 إنشاء بيئة افتراضية جديدة..."
    python3 -m venv venv
fi

# تفعيل البيئة الافتراضية
echo "🔧 تفعيل البيئة الافتراضية..."
source venv/bin/activate

# التحقق من المكتبات
echo "📦 التحقق من المكتبات..."
if ! python3 -c "import tkinter, requests, dns.resolver, bs4, lxml" 2>/dev/null; then
    echo "⚠️ بعض المكتبات مفقودة"
    echo "📥 تثبيت المكتبات المطلوبة..."
    pip install -r requirements.txt
fi

# تشغيل التطبيق
echo "🚀 بدء تشغيل التطبيق..."
echo "=================================================="

# تشغيل التطبيق الرئيسي
python3 main.py

# في حالة حدوث خطأ
if [ $? -ne 0 ]; then
    echo "❌ حدث خطأ في تشغيل التطبيق"
    echo "🔧 محاولة تشغيل التطبيق مباشرة..."
    python3 blue_badge_app.py
fi