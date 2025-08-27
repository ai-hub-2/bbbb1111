#!/usr/bin/env python3
"""
Real Tools Runner - مشغل الأدوات الحقيقية
Enhanced version focusing on Google-acceptable temp mail with Arabic countries support
نسخة محسنة تركز على البريد المؤقت المقبول عند جوجل مع دعم الدول العربية
"""
import os
import sys
import subprocess
import time

def print_banner():
    """Print application banner"""
    print("🔥" * 60)
    print("🔥 REAL TOOLS RUNNER - مشغل الأدوات الحقيقية 🔥")
    print("🔥 Enhanced for Google Acceptance & Arabic Countries 🔥")
    print("🔥 محسن لقبول جوجل والدول العربية 🔥")
    print("🔥" * 60)

def check_python():
    """Check Python installation"""
    try:
        result = subprocess.run(['python3', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Python3 not found")
            return False
    except FileNotFoundError:
        print("❌ Python3 not found")
        return False

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    
    requirements_files = [
        'requirements_real_tools.txt',
        'requirements_real.txt',
        'requirements.txt'
    ]
    
    for req_file in requirements_files:
        if os.path.exists(req_file):
            print(f"📦 Installing from {req_file}...")
            try:
                result = subprocess.run(['pip3', 'install', '-r', req_file], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Successfully installed from {req_file}")
                else:
                    print(f"⚠️  Some packages from {req_file} may not have installed")
            except Exception as e:
                print(f"⚠️  Could not install from {req_file}: {e}")
    
    print("✅ Package installation completed")

def run_temp_mail():
    """Run the enhanced temp mail tool"""
    print("\n📧 Running Enhanced Temp Mail Tool...")
    print("🔥 Features:")
    print("   ✅ Google Acceptable Domains")
    print("   🌍 17 Arabic Countries Support")
    print("   🔄 Dynamic Domain Changing")
    print("   🌐 Real API Integration")
    print("   📱 Country-Specific Features")
    
    if os.path.exists('real_tools/real_temp_mail.py'):
        try:
            subprocess.run(['python3', 'real_tools/real_temp_mail.py'])
        except Exception as e:
            print(f"❌ Error running temp mail: {e}")
    else:
        print("❌ Temp mail tool not found")

def run_gmail_creator():
    """Run the auto Gmail creator tool"""
    print("\n📧 Running Auto Gmail Creator...")
    print("🔥 Features:")
    print("   🤖 Real Gmail Account Creation")
    print("   🌐 Selenium Automation")
    print("   🔒 Stealth Mode")
    print("   📱 Phone Verification Support")
    
    if os.path.exists('real_tools/auto_gmail_creator.py'):
        try:
            subprocess.run(['python3', 'real_tools/auto_gmail_creator.py'])
        except Exception as e:
            print(f"❌ Error running Gmail creator: {e}")
    else:
        print("❌ Gmail creator tool not found")

def run_dns_checker():
    """Run the DNS checker tool"""
    print("\n🔍 Running Real DNS Checker...")
    print("🔥 Features:")
    print("   🌐 Real DNS API Integration")
    print("   🔍 Multiple Record Types")
    print("   🌍 Multiple DNS Servers")
    print("   📊 Comprehensive Reports")
    
    if os.path.exists('real_tools/real_dns_checker.py'):
        try:
            subprocess.run(['python3', 'real_tools/real_dns_checker.py'])
        except Exception as e:
            print(f"❌ Error running DNS checker: {e}")
    else:
        print("❌ DNS checker tool not found")

def show_menu():
    """Show main menu"""
    while True:
        print("\n" + "=" * 60)
        print("🎯 MAIN MENU - القائمة الرئيسية")
        print("=" * 60)
        print("1. 📧 Enhanced Temp Mail (البريد المؤقت المحسن)")
        print("2. 🤖 Auto Gmail Creator (منشئ Gmail التلقائي)")
        print("3. 🔍 Real DNS Checker (فحص DNS الحقيقي)")
        print("4. 🚀 Run All Tools (تشغيل جميع الأدوات)")
        print("5. 📦 Install Requirements (تثبيت المتطلبات)")
        print("6. ℹ️  Show Tool Info (معلومات الأدوات)")
        print("0. ❌ Exit (خروج)")
        print("=" * 60)
        
        try:
            choice = input("\n🎯 Enter your choice (اختر رقم العملية): ").strip()
            
            if choice == '1':
                run_temp_mail()
            elif choice == '2':
                run_gmail_creator()
            elif choice == '3':
                run_dns_checker()
            elif choice == '4':
                print("\n🚀 Running all tools...")
                run_temp_mail()
                time.sleep(2)
                run_gmail_creator()
                time.sleep(2)
                run_dns_checker()
            elif choice == '5':
                install_requirements()
            elif choice == '6':
                show_tool_info()
            elif choice == '0':
                print("\n👋 Goodbye! مع السلامة")
                break
            else:
                print("❌ Invalid choice")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! مع السلامة")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def show_tool_info():
    """Show detailed information about tools"""
    print("\n📚 TOOL INFORMATION - معلومات الأدوات")
    print("=" * 60)
    
    print("\n📧 ENHANCED TEMP MAIL:")
    print("   ✅ Google Acceptable Domains")
    print("   🌍 17 Arabic Countries (Saudi, UAE, Egypt, Kuwait, Qatar, etc.)")
    print("   🔄 Dynamic Domain Selection")
    print("   🌐 Real API Integration (Guerrilla, 10minutemail, etc.)")
    print("   📱 Country-Specific Features (Phone, Timezone, Language)")
    print("   🔒 Secure & Private")
    
    print("\n🤖 AUTO GMAIL CREATOR:")
    print("   🌐 Real Gmail Account Creation")
    print("   🤖 Selenium Web Automation")
    print("   🔒 Stealth Mode (Anti-Detection)")
    print("   📱 Phone Verification Support")
    print("   🌍 Multi-Country Support")
    
    print("\n🔍 REAL DNS CHECKER:")
    print("   🌐 Real DNS API Integration")
    print("   🔍 Multiple Record Types (A, AAAA, MX, TXT, etc.)")
    print("   🌍 Multiple DNS Servers (Google, Cloudflare, Arabic)")
    print("   📊 Comprehensive Reports")
    print("   🚀 Fast & Reliable")

def main():
    """Main function"""
    print_banner()
    
    if not check_python():
        print("❌ Python3 is required. Please install Python3 first.")
        return
    
    print("\n🚀 Welcome to Real Tools Runner!")
    print("🔥 All tools are REAL and WORKING - جميع الأدوات حقيقية وتعمل")
    
    show_menu()

if __name__ == "__main__":
    main()