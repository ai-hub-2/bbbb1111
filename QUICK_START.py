#!/usr/bin/env python3
"""
🚀🚀🚀 QUICK START - بدء سريع! 🚀🚀🚀
تشغيل سريع للتطبيق الخارق
"""

import os
import sys
import subprocess
import time

def print_banner():
    """طباعة البانر"""
    print("🔥🔥🔥" * 20)
    print("🚀🚀🚀 التطبيق الخارق للعلامة الزرقاء - REAL POWER! 🚀🚀🚀")
    print("🚀🚀🚀 SUPER BLUE BADGE APP - UNLEASHED POWER! 🚀🚀🚀")
    print("🔥🔥🔥" * 20)
    print()

def check_python():
    """فحص Python"""
    print("🔍 فحص Python...")
    try:
        import sys
        version = sys.version_info
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} متوفر!")
        return True
    except:
        print("❌ Python غير متوفر!")
        return False

def install_requirements():
    """تثبيت المتطلبات"""
    print("📦 تثبيت المتطلبات...")
    
    try:
        # تثبيت المتطلبات الأساسية
        print("1️⃣ تثبيت المتطلبات الأساسية...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_real.txt"], check=True)
        
        print("2️⃣ تثبيت جميع الأدوات...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_all_tools.txt"], check=True)
        
        print("✅ تم تثبيت جميع المتطلبات!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ خطأ في تثبيت المتطلبات: {e}")
        return False

def show_menu():
    """عرض القائمة"""
    print("\n🔥🔥🔥 الأدوات المتاحة - AVAILABLE TOOLS! 🔥🔥🔥")
    print("1. 🚀 التطبيق الرئيسي - Main App")
    print("2. 🛡️ أداة DNS الخفية - DNS Stealth Tool")
    print("3. 📧 منشئ Gmail - Gmail Creator")
    print("4. 🌐 تطبيق Cloudflare - Cloudflare App")
    print("5. 🔍 أداة العمليات الخفية - Stealth Operations")
    print("6. 🚀 تشغيل كل شيء - Run Everything!")
    print("7. 🚪 خروج - Exit")
    print()

def run_tool(choice):
    """تشغيل الأداة المختارة"""
    tools = {
        '1': 'real_blue_badge_app.py',
        '2': 'dns_stealth_tool.py',
        '3': 'gmail_creator_tool.py',
        '4': 'cloudflare_app.py',
        '5': 'stealth_operations_tool.py'
    }
    
    if choice in tools:
        tool = tools[choice]
        if os.path.exists(tool):
            print(f"🚀 تشغيل {tool}...")
            try:
                subprocess.run([sys.executable, tool])
            except KeyboardInterrupt:
                print("\n🚪 تم إيقاف الأداة")
        else:
            print(f"❌ الملف {tool} غير موجود!")
    elif choice == '6':
        run_everything()
    elif choice == '7':
        print("\n🚪 شكراً لاستخدام القوة الخارقة!")
        print("🚀 معاً نحو النجاح! 💙")
        sys.exit(0)
    else:
        print("❌ اختيار غير صحيح!")

def run_everything():
    """تشغيل كل شيء"""
    print("🚀 تشغيل كل شيء - RUNNING EVERYTHING!")
    print()
    
    tools = [
        'dns_stealth_tool.py',
        'gmail_creator_tool.py',
        'cloudflare_app.py',
        'stealth_operations_tool.py'
    ]
    
    processes = []
    
    # تشغيل الأدوات في الخلفية
    for tool in tools:
        if os.path.exists(tool):
            print(f"🛡️ تشغيل {tool}...")
            try:
                process = subprocess.Popen([sys.executable, tool])
                processes.append(process)
                time.sleep(1)
            except Exception as e:
                print(f"❌ خطأ في تشغيل {tool}: {e}")
    
    # تشغيل التطبيق الرئيسي
    print("🚀 تشغيل التطبيق الرئيسي...")
    try:
        subprocess.run([sys.executable, "real_blue_badge_app.py"])
    except KeyboardInterrupt:
        print("\n🚪 تم إيقاف التطبيق")
    
    # إيقاف جميع العمليات
    print("🛑 إيقاف جميع العمليات...")
    for process in processes:
        try:
            process.terminate()
        except:
            pass

def main():
    """الدالة الرئيسية"""
    print_banner()
    
    # فحص Python
    if not check_python():
        print("❌ يجب تثبيت Python أولاً!")
        input("اضغط Enter للخروج...")
        return
    
    # تثبيت المتطلبات
    if not install_requirements():
        print("❌ فشل في تثبيت المتطلبات!")
        input("اضغط Enter للخروج...")
        return
    
    print("✅ كل شيء جاهز!")
    
    # حلقة التشغيل
    while True:
        try:
            show_menu()
            choice = input("اختر رقم الأداة (1-7): ").strip()
            run_tool(choice)
            
            if choice != '6':  # إذا لم يكن "تشغيل كل شيء"
                input("\nاضغط Enter للعودة...")
                
        except KeyboardInterrupt:
            print("\n\n🚪 تم إيقاف التطبيق")
            break
        except Exception as e:
            print(f"\n❌ خطأ: {e}")
            input("اضغط Enter للعودة...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ خطأ في التشغيل: {e}")
        input("اضغط Enter للخروج...")