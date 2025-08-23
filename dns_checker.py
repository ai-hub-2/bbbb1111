#!/usr/bin/env python3
"""
DNS Checker Tool - للتحقق من سجلات DNS
أداة لمساعدة في استعادة حساب Google My Business
"""

import dns.resolver
import requests
import json
import time
from datetime import datetime

class DNSChecker:
    def __init__(self, domain):
        self.domain = domain
        self.results = {}
    
    def check_txt_records(self):
        """فحص سجلات TXT"""
        try:
            answers = dns.resolver.resolve(self.domain, 'TXT')
            txt_records = []
            for rdata in answers:
                txt_records.append(str(rdata).strip('"'))
            
            self.results['TXT'] = txt_records
            print(f"✅ سجلات TXT للدومين {self.domain}:")
            for record in txt_records:
                print(f"   📝 {record}")
            
            # البحث عن سجلات Google
            google_records = [r for r in txt_records if 'google-site-verification' in r]
            if google_records:
                print(f"🎯 تم العثور على {len(google_records)} سجل Google!")
                for record in google_records:
                    print(f"   🔍 {record}")
            else:
                print("⚠️  لم يتم العثور على سجلات Google")
                
        except Exception as e:
            print(f"❌ خطأ في فحص سجلات TXT: {e}")
    
    def check_a_records(self):
        """فحص سجلات A"""
        try:
            answers = dns.resolver.resolve(self.domain, 'A')
            a_records = []
            for rdata in answers:
                a_records.append(str(rdata))
            
            self.results['A'] = a_records
            print(f"✅ سجلات A للدومين {self.domain}:")
            for record in a_records:
                print(f"   🌐 {record}")
                
        except Exception as e:
            print(f"❌ خطأ في فحص سجلات A: {e}")
    
    def check_mx_records(self):
        """فحص سجلات MX"""
        try:
            answers = dns.resolver.resolve(self.domain, 'MX')
            mx_records = []
            for rdata in answers:
                mx_records.append(f"{rdata.preference} {rdata.exchange}")
            
            self.results['MX'] = mx_records
            print(f"✅ سجلات MX للدومين {self.domain}:")
            for record in mx_records:
                print(f"   📧 {record}")
                
        except Exception as e:
            print(f"❌ خطأ في فحص سجلات MX: {e}")
    
    def check_cname_records(self):
        """فحص سجلات CNAME"""
        try:
            answers = dns.resolver.resolve(f"www.{self.domain}", 'CNAME')
            cname_records = []
            for rdata in answers:
                cname_records.append(str(rdata))
            
            self.results['CNAME'] = cname_records
            print(f"✅ سجلات CNAME للدومين www.{self.domain}:")
            for record in cname_records:
                print(f"   🔗 {record}")
                
        except Exception as e:
            print(f"ℹ️  لا توجد سجلات CNAME أو خطأ: {e}")
    
    def check_online_tools(self):
        """فحص باستخدام أدوات أونلاين"""
        print(f"\n🌐 روابط للفحص الإضافي:")
        print(f"   🔍 MXToolbox: https://mxtoolbox.com/SuperTool.aspx?action=txt&run=toolpage&txtvalue={self.domain}")
        print(f"   🔍 DNS Checker: https://dnschecker.org/txt-lookup.php?query={self.domain}")
        print(f"   🔍 What's My DNS: https://whatsmydns.net/#{self.domain}/TXT")
    
    def generate_report(self):
        """إنشاء تقرير مفصل"""
        report = {
            'domain': self.domain,
            'timestamp': datetime.now().isoformat(),
            'results': self.results
        }
        
        filename = f"dns_report_{self.domain}_{int(time.time())}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 تم حفظ التقرير في: {filename}")
        return filename
    
    def run_full_check(self):
        """تشغيل فحص شامل"""
        print(f"🚀 بدء فحص DNS للدومين: {self.domain}")
        print("=" * 50)
        
        self.check_txt_records()
        print()
        self.check_a_records()
        print()
        self.check_mx_records()
        print()
        self.check_cname_records()
        print()
        self.check_online_tools()
        
        report_file = self.generate_report()
        
        print("\n" + "=" * 50)
        print("✅ تم الانتهاء من الفحص!")
        return report_file

def main():
    """الدالة الرئيسية"""
    print("🔍 أداة فحص DNS - لمساعدتك في استعادة حسابك")
    print("=" * 50)
    
    # يمكنك تغيير الدومين هنا
    domain = "samma-sa.com"
    
    checker = DNSChecker(domain)
    checker.run_full_check()
    
    print(f"\n💡 نصائح:")
    print("1. إذا لم تجد سجلات Google، تحتاج لإضافتها")
    print("2. استخدم الروابط أعلاه للتحقق من انتشار DNS")
    print("3. قد يستغرق انتشار DNS 24-48 ساعة")

if __name__ == "__main__":
    main()