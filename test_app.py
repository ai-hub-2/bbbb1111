#!/usr/bin/env python3
"""
ملف اختبار التطبيق بدون واجهة رسومية
Test file for the application without GUI
"""

import sys
import os

# إضافة المجلد الحالي إلى مسار Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """اختبار استيراد جميع الوحدات"""
    print("🧪 اختبار استيراد الوحدات...")
    
    modules = [
        'blue_badge_app',
        'complaint_generator', 
        'dns_checker',
        'email_generator',
        'website_optimizer',
        'super_blue_badge_app'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}: تم الاستيراد بنجاح")
        except Exception as e:
            print(f"❌ {module}: فشل الاستيراد - {e}")
            return False
    
    return True

def test_dns_checker():
    """اختبار فاحص DNS"""
    print("\n🌐 اختبار فاحص DNS...")
    
    try:
        from dns_checker import DNSChecker
        
        checker = DNSChecker('example.com')
        results = checker.run_full_check()
        
        print("✅ فاحص DNS يعمل بشكل صحيح")
        return True
        
    except Exception as e:
        print(f"❌ فاحص DNS فشل: {e}")
        return False

def test_email_generator():
    """اختبار مولّد البريد الإلكتروني"""
    print("\n📧 اختبار مولّد البريد الإلكتروني...")
    
    try:
        from email_generator import EmailGenerator
        
        generator = EmailGenerator()
        email_content = generator.generate_professional_email('business')
        
        print("✅ مولّد البريد الإلكتروني يعمل بشكل صحيح")
        return True
        
    except Exception as e:
        print(f"❌ مولّد البريد الإلكتروني فشل: {e}")
        return False

def test_website_optimizer():
    """اختبار محسّن الموقع"""
    print("\n🚀 اختبار محسّن الموقع...")
    
    try:
        from website_optimizer import WebsiteOptimizer
        
        optimizer = WebsiteOptimizer('example.com')
        status = optimizer.check_website_status()
        
        print("✅ محسّن الموقع يعمل بشكل صحيح")
        return True
        
    except Exception as e:
        print(f"❌ محسّن الموقع فشل: {e}")
        return False

def main():
    """الدالة الرئيسية للاختبار"""
    print("🔵 اختبار تطبيق العلامة الزرقاء")
    print("Blue Badge Application Test")
    print("=" * 50)
    
    # اختبار الاستيراد
    if not test_imports():
        print("\n❌ فشل في اختبار الاستيراد")
        return 1
    
    # اختبار الوحدات الفردية
    tests = [
        test_dns_checker,
        test_email_generator,
        test_website_optimizer
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 نتائج الاختبار: {passed}/{total} نجح")
    
    if passed == total:
        print("🎉 جميع الاختبارات نجحت! التطبيق جاهز للاستخدام")
        return 0
    else:
        print("⚠️ بعض الاختبارات فشلت. يرجى مراجعة الأخطاء")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)