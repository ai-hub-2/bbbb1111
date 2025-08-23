#!/usr/bin/env python3
"""
Complaint Generator - مولد رسائل الشكوى
أداة لإنشاء رسائل شكوى قوية لاستعادة حساب Google My Business
"""

import json
import datetime
from pathlib import Path

class ComplaintGenerator:
    def __init__(self):
        self.business_name = "سمة السعودية"
        self.domain = "samma-sa.com"
        self.stolen_url = "https://maps.app.goo.gl/QcGgQm13g3qi3cUh7"
        self.templates = {}
        
    def load_templates(self):
        """تحميل قوالب الرسائل"""
        self.templates = {
            'urgent': {
                'subject': 'URGENT: My Business Account Has Been Stolen - Family Crisis - Need Immediate Recovery',
                'content': '''Dear Google Support Team,

I am writing regarding my stolen Google My Business account for "{business_name}" (Samma Saudi Arabia). This is a matter of family survival and urgent business recovery.

Business Details:
- Business Name: {business_name} (Samma Saudi Arabia)
- Website: {domain} (registered in my name)
- Stolen Listing: {stolen_url}
- Business Type: Commercial Business
- Location: Saudi Arabia
- Business Registration: Valid and active

Evidence of Ownership:
- Domain ownership: {domain} (registered in my name)
- DNS verification completed successfully
- Business registration documents available
- Location photos and business license
- Historical business records
- Customer testimonials

CRITICAL SITUATION:
- My children cannot attend school due to financial hardship
- My business is completely paralyzed
- Family is facing severe financial crisis
- This is a matter of family survival

I have completed DNS verification for my domain and can provide all necessary documentation to prove ownership.

Please help me restore my verified business listing with the blue verification badge immediately.

This is a matter of urgent business survival and family welfare.

Thank you for your understanding and immediate assistance.

Best regards,
[Your Name]
[Phone Number]
[Email Address]
[Business Address]
[National ID Number]'''
            },
            'followup': {
                'subject': 'Follow-up: Stolen Business Account Recovery - Case Escalation Request - Family Emergency',
                'content': '''Dear Google Support Team,

I am following up on my urgent request regarding my stolen Google My Business account for "{business_name}" (Samma Saudi Arabia).

Previous communication date: {date}
Business: {business_name}
Website: {domain}
Case Reference: [If you have one]

I have not received any response yet, and this situation is causing severe financial hardship for my family.

Additional evidence I can provide:
- Business license and registration (Ministry of Commerce)
- Domain ownership certificates
- Location verification photos
- Customer testimonials and reviews
- Business bank statements
- Tax registration documents
- Employee contracts and payroll records

I kindly request:
1. IMMEDIATE case escalation to senior support
2. Priority handling due to family crisis
3. Direct contact from a support specialist
4. Emergency recovery of my business account

This business is my family's only source of income, and the stolen account is destroying our livelihood and children's future.

Please help me recover my account as soon as possible.

Thank you.

Best regards,
[Your Name]
[Emergency Phone Number]'''
            },
            'final': {
                'subject': 'FINAL URGENT REQUEST: Business Account Theft - Family Crisis - Legal Action Imminent',
                'content': '''Dear Google Support Team,

This is my final urgent request regarding my stolen Google My Business account for "{business_name}" (Samma Saudi Arabia).

Previous communications: {date}
Business: {business_name}
Website: {domain}

CRITICAL FAMILY CRISIS:
- My children cannot attend school due to financial hardship
- My business is completely paralyzed
- Family is facing eviction from home
- This is a matter of family survival and children's future

I have provided all requested documentation:
- DNS verification completed successfully
- Business ownership proof (Ministry of Commerce)
- Location verification
- All legal documents
- Customer testimonials
- Business financial records

I am requesting:
1. IMMEDIATE case escalation to senior support
2. Direct phone call from support team
3. Emergency recovery of my business account
4. Compensation for lost business during this period

If I cannot get help from Google, I will be forced to:
- Contact local media (Saudi newspapers and TV)
- File official complaints with Saudi authorities
- Seek legal assistance from Saudi lawyers
- Contact business protection organizations
- File complaint with Ministry of Commerce
- Contact Saudi Chamber of Commerce

Please help me save my family's future and business.

Thank you.

Best regards,
[Your Name]
[Emergency Phone Number]
[Business Address]
[National ID Number]'''
            },
            'twitter': [
                '@GoogleMyBiz @Google My business account "{business_name}" has been stolen! Need urgent help to recover it. This is affecting my family\'s survival. Domain: {domain} - I can prove ownership! #GoogleMyBusiness #Support #FamilyCrisis',
                '@GoogleMyBiz Please help! My verified business listing was stolen and I can\'t feed my children. Domain: {domain} - I can prove ownership! This is a family emergency! #BusinessEmergency #FamilyCrisis',
                '@GoogleMyBiz URGENT: Business account theft affecting family survival. Need immediate support to recover "{business_name}". Please help! #GoogleSupport #FamilyEmergency'
            ]
        }
    
    def generate_complaint(self, complaint_type='urgent', custom_data=None):
        """إنشاء رسالة شكوى"""
        self.load_templates()
        
        if complaint_type not in self.templates:
            print(f"❌ نوع الشكوى غير متوفر: {complaint_type}")
            return None
        
        # البيانات الافتراضية
        data = {
            'business_name': self.business_name,
            'domain': self.domain,
            'stolen_url': self.stolen_url,
            'date': datetime.datetime.now().strftime('%Y-%m-%d')
        }
        
        # إضافة البيانات المخصصة
        if custom_data:
            data.update(custom_data)
        
        template = self.templates[complaint_type]
        
        if complaint_type == 'twitter':
            # رسائل Twitter متعددة
            tweets = []
            for tweet_template in template:
                tweet = tweet_template.format(**data)
                tweets.append(tweet)
            return {
                'type': 'twitter',
                'messages': tweets,
                'timestamp': datetime.datetime.now().isoformat()
            }
        else:
            # رسائل البريد الإلكتروني
            complaint = {
                'type': complaint_type,
                'subject': template['subject'].format(**data),
                'content': template['content'].format(**data),
                'timestamp': datetime.datetime.now().isoformat()
            }
            return complaint
    
    def save_complaint(self, complaint, filename=None):
        """حفظ الرسالة في ملف"""
        if not filename:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"complaint_{complaint['type']}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            if complaint['type'] == 'twitter':
                f.write("Twitter Messages:\n")
                f.write("=" * 50 + "\n\n")
                for i, message in enumerate(complaint['messages'], 1):
                    f.write(f"Tweet {i}:\n")
                    f.write(message + "\n\n")
            else:
                f.write(f"Subject: {complaint['subject']}\n\n")
                f.write(complaint['content'])
        
        print(f"✅ تم حفظ الرسالة في: {filename}")
        return filename
    
    def generate_all_complaints(self):
        """إنشاء جميع أنواع الرسائل"""
        print("🚀 إنشاء جميع رسائل الشكوى...")
        print("=" * 50)
        
        complaints = []
        
        # رسالة عاجلة
        urgent = self.generate_complaint('urgent')
        if urgent:
            file1 = self.save_complaint(urgent)
            complaints.append(file1)
            print("✅ تم إنشاء الرسالة العاجلة")
        
        # رسالة متابعة
        followup = self.generate_complaint('followup')
        if followup:
            file2 = self.save_complaint(followup)
            complaints.append(file2)
            print("✅ تم إنشاء رسالة المتابعة")
        
        # رسالة نهائية
        final = self.generate_complaint('final')
        if final:
            file3 = self.save_complaint(final)
            complaints.append(file3)
            print("✅ تم إنشاء الرسالة النهائية")
        
        # رسائل Twitter
        twitter = self.generate_complaint('twitter')
        if twitter:
            file4 = self.save_complaint(twitter)
            complaints.append(file4)
            print("✅ تم إنشاء رسائل Twitter")
        
        print("\n" + "=" * 50)
        print("✅ تم إنشاء جميع الرسائل!")
        print(f"📁 الملفات المنشأة: {len(complaints)}")
        
        return complaints
    
    def create_schedule(self):
        """إنشاء جدول زمني للإرسال"""
        schedule = {
            'اليوم الأول': 'إرسال الرسالة العاجلة',
            'اليوم الرابع': 'إرسال رسالة المتابعة',
            'اليوم السابع': 'إرسال الرسالة النهائية',
            'يومياً': 'نشر رسائل Twitter'
        }
        
        print("\n📅 الجدول الزمني المقترح:")
        print("=" * 30)
        for day, action in schedule.items():
            print(f"📌 {day}: {action}")
        
        return schedule

def main():
    """الدالة الرئيسية"""
    print("📝 مولد رسائل الشكوى - لاستعادة حسابك")
    print("=" * 50)
    
    generator = ComplaintGenerator()
    
    # إنشاء جميع الرسائل
    files = generator.generate_all_complaints()
    
    # إنشاء الجدول الزمني
    generator.create_schedule()
    
    print(f"\n💡 نصائح:")
    print("1. اقرأ الرسائل وعدّل البيانات الشخصية")
    print("2. اتبع الجدول الزمني للإرسال")
    print("3. احتفظ بنسخ من جميع المراسلات")
    print("4. لا تستسلم واستمر في المتابعة")

if __name__ == "__main__":
    main()