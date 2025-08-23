#!/usr/bin/env python3
"""
Email Generator - مولد الإيميلات الاحترافية
أداة لإنشاء إيميلات احترافية مقبولة في Google
"""

import random
import string
import json
import datetime
from pathlib import Path

class EmailGenerator:
    def __init__(self):
        self.business_name = "سمة السعودية"
        self.domain = "samma-sa.com"
        self.generated_emails = []
        
        # قوائم الكلمات الاحترافية
        self.professional_words = [
            'info', 'contact', 'support', 'admin', 'manager', 'director',
            'sales', 'marketing', 'service', 'help', 'office', 'business',
            'team', 'staff', 'dept', 'group', 'unit', 'division'
        ]
        
        self.arabic_business_words = [
            'maktab', 'sharika', 'moassasa', 'markaz', 'idara', 'qism',
            'fariq', 'majmoua', 'wakalah', 'mashroa', 'tijara', 'khadamat'
        ]
        
        # أسماء احترافية
        self.professional_names = [
            'ahmed', 'mohammed', 'abdullah', 'omar', 'khalid', 'faisal',
            'nasser', 'saud', 'sultan', 'turki', 'bandar', 'salman',
            'fahad', 'yazid', 'majid', 'waleed', 'rashed', 'saeed'
        ]
        
        # مناصب إدارية
        self.positions = [
            'ceo', 'manager', 'director', 'supervisor', 'coordinator',
            'specialist', 'consultant', 'advisor', 'executive', 'officer'
        ]
    
    def generate_professional_email(self, email_type='business'):
        """إنشاء إيميل احترافي"""
        if email_type == 'business':
            return self._generate_business_email()
        elif email_type == 'personal':
            return self._generate_personal_email()
        elif email_type == 'department':
            return self._generate_department_email()
        elif email_type == 'support':
            return self._generate_support_email()
        else:
            return self._generate_business_email()
    
    def _generate_business_email(self):
        """إنشاء إيميل تجاري"""
        patterns = [
            f"{random.choice(self.professional_words)}@{self.domain}",
            f"{random.choice(self.arabic_business_words)}@{self.domain}",
            f"samma.{random.choice(self.professional_words)}@{self.domain}",
            f"business.{random.choice(self.professional_words)}@{self.domain}",
            f"{random.choice(self.professional_words)}.samma@{self.domain}",
        ]
        return random.choice(patterns)
    
    def _generate_personal_email(self):
        """إنشاء إيميل شخصي احترافي"""
        name = random.choice(self.professional_names)
        position = random.choice(self.positions)
        
        patterns = [
            f"{name}@{self.domain}",
            f"{name}.{position}@{self.domain}",
            f"{name}.samma@{self.domain}",
            f"{position}.{name}@{self.domain}",
            f"{name}{random.randint(1, 99)}@{self.domain}",
        ]
        return random.choice(patterns)
    
    def _generate_department_email(self):
        """إنشاء إيميل قسم"""
        departments = [
            'sales', 'marketing', 'support', 'finance', 'hr', 'it',
            'operations', 'admin', 'legal', 'quality', 'research', 'development'
        ]
        
        dept = random.choice(departments)
        patterns = [
            f"{dept}@{self.domain}",
            f"{dept}.team@{self.domain}",
            f"{dept}.dept@{self.domain}",
            f"samma.{dept}@{self.domain}",
        ]
        return random.choice(patterns)
    
    def _generate_support_email(self):
        """إنشاء إيميل دعم"""
        support_types = [
            'support', 'help', 'service', 'assistance', 'care',
            'contact', 'info', 'inquiry', 'feedback'
        ]
        
        support_type = random.choice(support_types)
        patterns = [
            f"{support_type}@{self.domain}",
            f"customer.{support_type}@{self.domain}",
            f"{support_type}.center@{self.domain}",
            f"samma.{support_type}@{self.domain}",
        ]
        return random.choice(patterns)
    
    def generate_gmail_compatible_emails(self, count=20):
        """إنشاء إيميلات متوافقة مع Gmail"""
        gmail_emails = []
        
        for _ in range(count):
            # أنواع مختلفة من الإيميلات
            email_types = ['business', 'personal', 'department', 'support']
            email_type = random.choice(email_types)
            
            # إنشاء إيميل Gmail
            gmail_prefix = self._generate_gmail_prefix()
            gmail_email = f"{gmail_prefix}@gmail.com"
            
            # إنشاء إيميل مخصص للدومين
            custom_email = self.generate_professional_email(email_type)
            
            email_pair = {
                'gmail': gmail_email,
                'custom': custom_email,
                'type': email_type,
                'created': datetime.datetime.now().isoformat()
            }
            
            gmail_emails.append(email_pair)
        
        return gmail_emails
    
    def _generate_gmail_prefix(self):
        """إنشاء بادئة Gmail احترافية"""
        patterns = [
            # أسماء + أرقام
            f"{random.choice(self.professional_names)}{random.randint(100, 9999)}",
            f"{random.choice(self.professional_names)}.{random.choice(self.positions)}",
            f"samma.{random.choice(self.professional_names)}",
            f"{random.choice(self.professional_names)}.business",
            f"saudi.{random.choice(self.professional_names)}",
            
            # أعمال + كلمات احترافية
            f"samma.{random.choice(self.professional_words)}",
            f"business.{random.choice(self.professional_words)}",
            f"saudi.{random.choice(self.professional_words)}",
            f"{random.choice(self.professional_words)}.pro",
            f"{random.choice(self.professional_words)}.saudi",
            
            # مزج كلمات عربية مع إنجليزية
            f"samma.{random.choice(self.arabic_business_words)}",
            f"{random.choice(self.arabic_business_words)}.pro",
            f"saudi.{random.choice(self.arabic_business_words)}",
        ]
        
        return random.choice(patterns)
    
    def create_email_signatures(self, email_list):
        """إنشاء توقيعات إيميل احترافية"""
        signatures = []
        
        for email_data in email_list:
            signature = f"""
--
{random.choice(self.professional_names).title()} {random.choice(['Al-Saudi', 'Al-Samma', 'Mohammed', 'Abdullah'])}
{random.choice(self.positions).title()} | سمة السعودية - Samma Saudi Arabia
📧 {email_data['custom']}
🌐 https://{self.domain}
📱 +966 5X XXX XXXX
📍 المملكة العربية السعودية

"نحو تميز في الخدمات التجارية"
            """
            
            signatures.append({
                'email': email_data['custom'],
                'signature': signature.strip()
            })
        
        return signatures
    
    def generate_email_templates(self):
        """إنشاء قوالب إيميل احترافية"""
        templates = {
            'welcome': {
                'subject': 'مرحباً بك في سمة السعودية - Welcome to Samma Saudi Arabia',
                'body': '''السلام عليكم ورحمة الله وبركاته،

مرحباً بك في سمة السعودية، شركتك المتخصصة في الخدمات التجارية المتميزة.

نحن سعداء لانضمامك إلى عائلة عملائنا الكرام، ونتطلع لخدمتك بأفضل ما لدينا.

خدماتنا تشمل:
• الاستشارات التجارية
• الحلول المبتكرة
• الدعم الفني المتخصص
• خدمة العملاء على مدار الساعة

لأي استفسار، لا تتردد في التواصل معنا.

مع أطيب التحيات،
فريق سمة السعودية

---

Peace be upon you,

Welcome to Samma Saudi Arabia, your specialized company for distinguished business services.

We are happy to have you join our valued customer family and look forward to serving you with the best we have.

Best regards,
Samma Saudi Arabia Team'''
            },
            
            'inquiry_response': {
                'subject': 'رد على استفسارك - Response to Your Inquiry',
                'body': '''السلام عليكم ورحمة الله وبركاته،

شكراً لك على تواصلك مع سمة السعودية.

لقد تلقينا استفسارك وسيقوم فريقنا المختص بالرد عليك خلال 24 ساعة.

نحن ملتزمون بتقديم أفضل الخدمات لعملائنا الكرام.

مع أطيب التحيات،
فريق خدمة العملاء
سمة السعودية'''
            },
            
            'business_proposal': {
                'subject': 'عرض تجاري من سمة السعودية - Business Proposal',
                'body': '''السلام عليكم ورحمة الله وبركاته،

يسعدنا في سمة السعودية أن نقدم لكم عرضنا التجاري المتميز.

تفاصيل العرض:
• خدمات متخصصة وفقاً لاحتياجاتكم
• أسعار تنافسية
• جودة عالية في التنفيذ
• دعم فني متواصل

نحن واثقون من قدرتنا على تلبية توقعاتكم وتحقيق أهدافكم.

للمزيد من التفاصيل، يرجى التواصل معنا.

مع أطيب التحيات،
فريق المبيعات
سمة السعودية'''
            }
        }
        
        return templates
    
    def save_emails_to_file(self, emails, filename=None):
        """حفظ الإيميلات في ملف"""
        if not filename:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"generated_emails_{timestamp}.json"
        
        data = {
            'business_name': self.business_name,
            'domain': self.domain,
            'generated_at': datetime.datetime.now().isoformat(),
            'total_emails': len(emails),
            'emails': emails
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ تم حفظ {len(emails)} إيميل في: {filename}")
        return filename
    
    def export_to_csv(self, emails, filename=None):
        """تصدير الإيميلات إلى CSV"""
        if not filename:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"emails_{timestamp}.csv"
        
        csv_content = "Gmail,Custom Email,Type,Created\n"
        
        for email in emails:
            csv_content += f"{email['gmail']},{email['custom']},{email['type']},{email['created']}\n"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        print(f"✅ تم تصدير الإيميلات إلى: {filename}")
        return filename
    
    def generate_complete_package(self, email_count=50):
        """إنشاء حزمة كاملة من الإيميلات"""
        print("🚀 إنشاء حزمة إيميلات احترافية...")
        print("=" * 50)
        
        # إنشاء الإيميلات
        emails = self.generate_gmail_compatible_emails(email_count)
        print(f"✅ تم إنشاء {len(emails)} إيميل")
        
        # إنشاء التوقيعات
        signatures = self.create_email_signatures(emails)
        print(f"✅ تم إنشاء {len(signatures)} توقيع")
        
        # إنشاء القوالب
        templates = self.generate_email_templates()
        print(f"✅ تم إنشاء {len(templates)} قالب")
        
        # حفظ الملفات
        email_file = self.save_emails_to_file(emails)
        csv_file = self.export_to_csv(emails)
        
        # حفظ التوقيعات
        sig_filename = f"email_signatures_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(sig_filename, 'w', encoding='utf-8') as f:
            json.dump(signatures, f, indent=2, ensure_ascii=False)
        print(f"✅ تم حفظ التوقيعات في: {sig_filename}")
        
        # حفظ القوالب
        temp_filename = f"email_templates_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(temp_filename, 'w', encoding='utf-8') as f:
            json.dump(templates, f, indent=2, ensure_ascii=False)
        print(f"✅ تم حفظ القوالب في: {temp_filename}")
        
        print("\n" + "=" * 50)
        print("✅ تم إنشاء الحزمة الكاملة!")
        
        # إحصائيات
        stats = self._generate_statistics(emails)
        print(f"\n📊 الإحصائيات:")
        for key, value in stats.items():
            print(f"   📈 {key}: {value}")
        
        return {
            'emails': emails,
            'signatures': signatures,
            'templates': templates,
            'files': [email_file, csv_file, sig_filename, temp_filename],
            'statistics': stats
        }
    
    def _generate_statistics(self, emails):
        """إنشاء إحصائيات الإيميلات"""
        stats = {
            'إجمالي الإيميلات': len(emails),
            'إيميلات الأعمال': len([e for e in emails if e['type'] == 'business']),
            'إيميلات شخصية': len([e for e in emails if e['type'] == 'personal']),
            'إيميلات الأقسام': len([e for e in emails if e['type'] == 'department']),
            'إيميلات الدعم': len([e for e in emails if e['type'] == 'support'])
        }
        return stats
    
    def create_usage_guide(self):
        """إنشاء دليل الاستخدام"""
        guide = """
# دليل استخدام الإيميلات المولدة 📧

## 🎯 كيفية الاستخدام

### 1. إيميلات Gmail
- استخدم الإيميلات المولدة لإنشاء حسابات Gmail جديدة
- اختر الأسماء الاحترافية والمناسبة لعملك
- فعّل المصادقة الثنائية لكل حساب

### 2. إيميلات مخصصة
- استخدم الإيميلات المخصصة لدومينك
- أضفها في إعدادات البريد الإلكتروني
- اربطها بحسابات Gmail للإدارة السهلة

### 3. التوقيعات
- أضف التوقيعات الاحترافية لكل إيميل
- عدّل المعلومات الشخصية حسب الحاجة
- استخدم التوقيعات في جميع المراسلات

## 💡 نصائح مهمة

1. **لا تستخدم جميع الإيميلات مرة واحدة**
2. **اختر الأسماء المناسبة لنشاطك**
3. **احتفظ بكلمات مرور قوية**
4. **فعّل المصادقة الثنائية**
5. **استخدم الإيميلات للأغراض التجارية فقط**

## 🚨 تنبيهات

- لا تستخدم الإيميلات للأنشطة المشبوهة
- احترم شروط خدمة Google
- استخدم الإيميلات للأغراض التجارية المشروعة فقط
        """
        
        with open('email_usage_guide.md', 'w', encoding='utf-8') as f:
            f.write(guide)
        
        print("✅ تم إنشاء دليل الاستخدام في: email_usage_guide.md")
        return guide

def main():
    """الدالة الرئيسية"""
    print("📧 مولد الإيميلات الاحترافية - لدعم استعادة حسابك")
    print("=" * 50)
    
    generator = EmailGenerator()
    
    # إنشاء الحزمة الكاملة
    package = generator.generate_complete_package(50)
    
    # إنشاء دليل الاستخدام
    generator.create_usage_guide()
    
    print(f"\n💡 نصائح:")
    print("1. استخدم الإيميلات للأغراض التجارية المشروعة")
    print("2. فعّل المصادقة الثنائية لكل حساب")
    print("3. احتفظ بكلمات مرور قوية")
    print("4. لا تستخدم جميع الإيميلات مرة واحدة")
    
    print(f"\n🎯 الهدف:")
    print("استخدام هذه الإيميلات لدعم استعادة حساب Google My Business")

if __name__ == "__main__":
    main()