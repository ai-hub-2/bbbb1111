#!/bin/bash

# 🔥🔥🔥 RUN_POWER.sh - تشغيل القوة الخارقة! 🔥🔥🔥
# RUN_POWER.sh - Unleash the SUPER POWER!

echo "🚀🚀🚀 التطبيق الخارق للعلامة الزرقاء - REAL POWER! 🚀🚀🚀"
echo "🚀🚀🚀 SUPER BLUE BADGE APP - UNLEASHED POWER! 🚀🚀🚀"
echo ""

# التحقق من Python
echo "🔍 فحص Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python متوفر: $PYTHON_VERSION"
else
    echo "❌ Python غير متوفر!"
    echo "📥 قم بتثبيت Python 3.7+ أولاً"
    exit 1
fi

# التحقق من pip
echo "🔍 فحص pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip متوفر"
else
    echo "❌ pip غير متوفر!"
    echo "📥 قم بتثبيت pip أولاً"
    exit 1
fi

# تثبيت المتطلبات
echo ""
echo "📦 تثبيت المتطلبات..."
echo "1️⃣ تثبيت المتطلبات الأساسية..."
pip3 install -r requirements_real.txt

echo ""
echo "2️⃣ تثبيت جميع الأدوات..."
pip3 install -r requirements_all_tools.txt

echo ""
echo "✅ تم تثبيت جميع المتطلبات!"

# عرض القائمة
echo ""
echo "🔥🔥🔥 الأدوات المتاحة - AVAILABLE TOOLS! 🔥🔥🔥"
echo "1. 🚀 التطبيق الرئيسي - Main App"
echo "2. 🛡️ أداة DNS الخفية - DNS Stealth Tool"
echo "3. 📧 منشئ Gmail - Gmail Creator"
echo "4. 🌐 تطبيق Cloudflare - Cloudflare App"
echo "5. 🔍 أداة العمليات الخفية - Stealth Operations"
echo "6. 📱 أداة الأرقام - Phone Numbers Tool"
echo "7. 📧 أداة البريد المؤقت - Temp Mail Tool"
echo "8. 🚀 تشغيل كل شيء - Run Everything!"
echo "9. 🚪 خروج - Exit"
echo ""

# اختيار الأداة
read -p "اختر رقم الأداة (1-9): " choice

case $choice in
    1)
        echo "🚀 تشغيل التطبيق الرئيسي..."
        python3 real_blue_badge_app.py
        ;;
    2)
        echo "🛡️ تشغيل أداة DNS الخفية..."
        python3 dns_stealth_tool.py
        ;;
    3)
        echo "📧 تشغيل منشئ Gmail..."
        python3 gmail_creator_tool.py
        ;;
    4)
        echo "🌐 تشغيل تطبيق Cloudflare..."
        python3 cloudflare_app.py
        ;;
    5)
        echo "🔍 تشغيل أداة العمليات الخفية..."
        python3 stealth_operations_tool.py
        ;;
    6)
        echo "📱 تشغيل أداة الأرقام..."
        python3 real_blue_badge_app.py
        ;;
    7)
        echo "📧 تشغيل أداة البريد المؤقت..."
        python3 real_blue_badge_app.py
        ;;
    8)
        echo "🚀 تشغيل كل شيء - RUNNING EVERYTHING!"
        echo ""
        echo "🛡️ تشغيل DNS Stealth Tool..."
        python3 dns_stealth_tool.py &
        echo "📧 تشغيل Gmail Creator..."
        python3 gmail_creator_tool.py &
        echo "🌐 تشغيل Cloudflare App..."
        python3 cloudflare_app.py &
        echo "🔍 تشغيل Stealth Operations..."
        python3 stealth_operations_tool.py &
        echo "🚀 تشغيل التطبيق الرئيسي..."
        python3 real_blue_badge_app.py
        ;;
    9)
        echo "🚪 شكراً لاستخدام القوة الخارقة!"
        echo "🚀 معاً نحو النجاح! 💙"
        exit 0
        ;;
    *)
        echo "❌ اختيار غير صحيح!"
        echo "🚀 تشغيل التطبيق الرئيسي..."
        python3 real_blue_badge_app.py
        ;;
esac

echo ""
echo "🔥🔥🔥 القوة الخارقة تم تفعيلها! 🔥🔥🔥"
echo "🚀🚀🚀 SUPER POWER ACTIVATED! 🚀🚀🚀"
echo "💪💪💪 أنت الآن لا يقهر! 💪💪💪"