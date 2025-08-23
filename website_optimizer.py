#!/usr/bin/env python3
"""
Website Optimizer - محسن المواقع الإلكترونية
أداة لتحسين موقعك الإلكتروني وSEO لدعم استعادة حساب Google My Business
"""

import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import datetime

class WebsiteOptimizer:
    def __init__(self, domain):
        self.domain = domain
        self.base_url = f"https://{domain}"
        self.results = {}
        
    def check_website_status(self):
        """فحص حالة الموقع"""
        try:
            response = requests.get(self.base_url, timeout=10)
            self.results['status_code'] = response.status_code
            self.results['response_time'] = response.elapsed.total_seconds()
            
            print(f"✅ حالة الموقع: {response.status_code}")
            print(f"⏱️  وقت الاستجابة: {response.elapsed.total_seconds():.2f} ثانية")
            
            if response.status_code == 200:
                print("🎯 الموقع يعمل بشكل طبيعي")
                return True
            else:
                print(f"⚠️  مشكلة في الموقع: كود الحالة {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في الاتصال بالموقع: {e}")
            return False
    
    def analyze_seo(self):
        """تحليل SEO للموقع"""
        try:
            response = requests.get(self.base_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            seo_analysis = {}
            
            # فحص العنوان
            title = soup.find('title')
            if title:
                seo_analysis['title'] = title.get_text().strip()
                print(f"📝 عنوان الصفحة: {title.get_text().strip()}")
            else:
                print("❌ لا يوجد عنوان للصفحة")
                seo_analysis['title'] = None
            
            # فحص الوصف
            description = soup.find('meta', attrs={'name': 'description'})
            if description:
                seo_analysis['description'] = description.get('content')
                print(f"📄 الوصف: {description.get('content')}")
            else:
                print("❌ لا يوجد وصف للصفحة")
                seo_analysis['description'] = None
            
            # فحص الكلمات المفتاحية
            keywords = soup.find('meta', attrs={'name': 'keywords'})
            if keywords:
                seo_analysis['keywords'] = keywords.get('content')
                print(f"🔑 الكلمات المفتاحية: {keywords.get('content')}")
            else:
                print("❌ لا توجد كلمات مفتاحية")
                seo_analysis['keywords'] = None
            
            # فحص العناوين
            headings = {
                'h1': len(soup.find_all('h1')),
                'h2': len(soup.find_all('h2')),
                'h3': len(soup.find_all('h3'))
            }
            seo_analysis['headings'] = headings
            print(f"📊 العناوين: H1({headings['h1']}) H2({headings['h2']}) H3({headings['h3']})")
            
            # فحص الصور
            images = soup.find_all('img')
            images_without_alt = [img for img in images if not img.get('alt')]
            seo_analysis['images_total'] = len(images)
            seo_analysis['images_without_alt'] = len(images_without_alt)
            print(f"🖼️  الصور: {len(images)} إجمالي، {len(images_without_alt)} بدون نص بديل")
            
            self.results['seo'] = seo_analysis
            return seo_analysis
            
        except Exception as e:
            print(f"❌ خطأ في تحليل SEO: {e}")
            return None
    
    def generate_structured_data(self):
        """إنشاء البيانات المنظمة"""
        structured_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "سمة السعودية",
            "alternateName": "Samma Saudi Arabia",
            "url": f"https://{self.domain}",
            "telephone": "[رقم الهاتف]",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "[عنوان الشارع]",
                "addressLocality": "[المدينة]",
                "addressRegion": "[المنطقة]",
                "addressCountry": "SA"
            },
            "openingHours": [
                "Mo-Fr 09:00-18:00",
                "Sa 09:00-15:00"
            ],
            "sameAs": [
                f"https://{self.domain}",
                "[رابط Facebook]",
                "[رابط Twitter]",
                "[رابط Instagram]"
            ]
        }
        
        # حفظ البيانات المنظمة
        with open('structured_data.json', 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, indent=2, ensure_ascii=False)
        
        print("✅ تم إنشاء البيانات المنظمة في ملف structured_data.json")
        return structured_data
    
    def create_sitemap(self):
        """إنشاء خريطة الموقع"""
        sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://{self.domain}/</loc>
        <lastmod>{datetime.datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://{self.domain}/about</loc>
        <lastmod>{datetime.datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://{self.domain}/services</loc>
        <lastmod>{datetime.datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://{self.domain}/contact</loc>
        <lastmod>{datetime.datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
</urlset>'''
        
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        print("✅ تم إنشاء خريطة الموقع في ملف sitemap.xml")
        return sitemap_content
    
    def create_robots_txt(self):
        """إنشاء ملف robots.txt"""
        robots_content = f'''User-agent: *
Allow: /

Sitemap: https://{self.domain}/sitemap.xml

# Google
User-agent: Googlebot
Allow: /

# Bing
User-agent: Bingbot
Allow: /'''
        
        with open('robots.txt', 'w', encoding='utf-8') as f:
            f.write(robots_content)
        
        print("✅ تم إنشاء ملف robots.txt")
        return robots_content
    
    def generate_meta_tags(self):
        """إنشاء علامات META محسنة"""
        meta_tags = f'''<!-- Basic Meta Tags -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>سمة السعودية - Samma Saudi Arabia | خدمات تجارية متميزة</title>
<meta name="description" content="سمة السعودية - شركة رائدة في تقديم الخدمات التجارية المتميزة في المملكة العربية السعودية. نقدم حلول مبتكرة لعملائنا.">
<meta name="keywords" content="سمة السعودية, Samma Saudi Arabia, خدمات تجارية, السعودية, أعمال">
<meta name="author" content="سمة السعودية">

<!-- Open Graph Meta Tags -->
<meta property="og:title" content="سمة السعودية - Samma Saudi Arabia">
<meta property="og:description" content="شركة رائدة في تقديم الخدمات التجارية المتميزة في المملكة العربية السعودية">
<meta property="og:url" content="https://{self.domain}">
<meta property="og:type" content="business.business">
<meta property="og:image" content="https://{self.domain}/images/logo.jpg">
<meta property="og:site_name" content="سمة السعودية">

<!-- Twitter Card Meta Tags -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="سمة السعودية - Samma Saudi Arabia">
<meta name="twitter:description" content="شركة رائدة في تقديم الخدمات التجارية المتميزة في المملكة العربية السعودية">
<meta name="twitter:image" content="https://{self.domain}/images/logo.jpg">

<!-- Business Information -->
<meta name="geo.region" content="SA">
<meta name="geo.placename" content="Saudi Arabia">
<meta name="business.hours" content="Mo-Fr 09:00-18:00">
<meta name="business.phone" content="[رقم الهاتف]">

<!-- Google Site Verification -->
<meta name="google-site-verification" content="[كود التحقق من Google]">

<!-- Canonical URL -->
<link rel="canonical" href="https://{self.domain}">'''
        
        with open('meta_tags.html', 'w', encoding='utf-8') as f:
            f.write(meta_tags)
        
        print("✅ تم إنشاء علامات META في ملف meta_tags.html")
        return meta_tags
    
    def create_about_page_content(self):
        """إنشاء محتوى صفحة "حول""""
        about_content = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>حول سمة السعودية - About Samma Saudi Arabia</title>
    <meta name="description" content="تعرف على سمة السعودية، شركة رائدة في تقديم الخدمات التجارية المتميزة في المملكة العربية السعودية">
</head>
<body>
    <header>
        <h1>سمة السعودية - Samma Saudi Arabia</h1>
        <nav>
            <a href="/">الرئيسية</a>
            <a href="/about">حول</a>
            <a href="/services">خدماتنا</a>
            <a href="/contact">اتصل بنا</a>
        </nav>
    </header>
    
    <main>
        <section>
            <h2>حول شركتنا</h2>
            <p>سمة السعودية هي شركة رائدة في تقديم الخدمات التجارية المتميزة في المملكة العربية السعودية. تأسست الشركة برؤية واضحة لتقديم حلول مبتكرة ومتطورة تلبي احتياجات عملائنا وتساهم في نمو الاقتصاد السعودي.</p>
            
            <h3>رؤيتنا</h3>
            <p>أن نكون الشركة الرائدة في مجال الخدمات التجارية في المملكة العربية السعودية، ونساهم في تحقيق رؤية 2030.</p>
            
            <h3>رسالتنا</h3>
            <p>تقديم خدمات تجارية متميزة وحلول مبتكرة تساعد عملاءنا على تحقيق أهدافهم التجارية بكفاءة وفعالية.</p>
            
            <h3>قيمنا</h3>
            <ul>
                <li>الجودة والتميز في الخدمة</li>
                <li>الالتزام والمصداقية</li>
                <li>الابتكار والتطوير المستمر</li>
                <li>خدمة العملاء المتميزة</li>
            </ul>
        </section>
        
        <section>
            <h2>معلومات الاتصال</h2>
            <address>
                <p><strong>العنوان:</strong> [عنوان الشركة]</p>
                <p><strong>الهاتف:</strong> [رقم الهاتف]</p>
                <p><strong>البريد الإلكتروني:</strong> [البريد الإلكتروني]</p>
                <p><strong>الموقع الإلكتروني:</strong> https://{self.domain}</p>
            </address>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2024 سمة السعودية - Samma Saudi Arabia. جميع الحقوق محفوظة.</p>
    </footer>
</body>
</html>'''
        
        with open('about.html', 'w', encoding='utf-8') as f:
            f.write(about_content)
        
        print("✅ تم إنشاء صفحة 'حول' في ملف about.html")
        return about_content
    
    def generate_optimization_report(self):
        """إنشاء تقرير التحسين"""
        report = {
            'domain': self.domain,
            'timestamp': datetime.datetime.now().isoformat(),
            'results': self.results,
            'recommendations': [
                'إضافة سجلات DNS للتحقق من ملكية الدومين',
                'تحسين علامات META للصفحات',
                'إضافة البيانات المنظمة (Schema.org)',
                'إنشاء محتوى عالي الجودة',
                'تحسين سرعة الموقع',
                'إضافة شهادة SSL',
                'تحسين تجربة المستخدم على الهاتف المحمول'
            ]
        }
        
        filename = f"optimization_report_{self.domain}_{int(datetime.datetime.now().timestamp())}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 تم حفظ تقرير التحسين في: {filename}")
        return filename
    
    def run_full_optimization(self):
        """تشغيل التحسين الشامل"""
        print(f"🚀 بدء تحسين الموقع: {self.domain}")
        print("=" * 50)
        
        # فحص حالة الموقع
        if self.check_website_status():
            print()
            # تحليل SEO
            self.analyze_seo()
            print()
        
        # إنشاء الملفات المحسنة
        self.generate_structured_data()
        self.create_sitemap()
        self.create_robots_txt()
        self.generate_meta_tags()
        self.create_about_page_content()
        
        # إنشاء التقرير
        report_file = self.generate_optimization_report()
        
        print("\n" + "=" * 50)
        print("✅ تم الانتهاء من التحسين!")
        
        print(f"\n💡 الخطوات التالية:")
        print("1. ارفع الملفات المنشأة إلى موقعك")
        print("2. أضف علامات META إلى صفحاتك")
        print("3. أضف البيانات المنظمة إلى موقعك")
        print("4. اربط موقعك بـ Google Search Console")
        
        return report_file

def main():
    """الدالة الرئيسية"""
    print("🌐 محسن المواقع الإلكترونية - لدعم استعادة حسابك")
    print("=" * 50)
    
    # يمكنك تغيير الدومين هنا
    domain = "samma-sa.com"
    
    optimizer = WebsiteOptimizer(domain)
    optimizer.run_full_optimization()

if __name__ == "__main__":
    main()