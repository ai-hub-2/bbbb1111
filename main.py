#!/usr/bin/env python3
"""
الملف الرئيسي لتشغيل تطبيق العلامة الزرقاء
Main file to run the Blue Badge application
"""

import sys
import os

# إضافة المجلد الحالي إلى مسار Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """الدالة الرئيسية للتطبيق"""
    print("🔵 تطبيق العلامة الزرقاء الشامل")
    print("Blue Badge Complete Application")
    print("=" * 50)
    
    try:
        # استيراد التطبيق الرئيسي
        from blue_badge_app import BlueBadgeApp
        import tkinter as tk
        
        print("✅ تم تحميل التطبيق بنجاح")
        print("🚀 بدء تشغيل واجهة المستخدم...")
        
        # إنشاء النافذة الرئيسية
        root = tk.Tk()
        app = BlueBadgeApp(root)
        
        # تشغيل التطبيق
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ خطأ في استيراد المكتبات: {e}")
        print("يرجى التأكد من تثبيت جميع المكتبات المطلوبة")
        return 1
        
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)