#!/usr/bin/env python3
"""
Cloudflare Pages Blue Badge App - تطبيق العلامة الزرقاء لـ Cloudflare Pages
Cloudflare Pages Compatible Blue Badge Application
"""

import streamlit as st
import requests
import json
import dns.resolver
import time
import datetime
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import base64
import io
import os

# إعدادات Cloudflare Pages
CLOUDFLARE_MODE = os.getenv('CLOUDFLARE_PAGES', 'false').lower() == 'true'

# إعداد الصفحة
st.set_page_config(
    page_title="🔵 تطبيق العلامة الزرقاء - Cloudflare",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص لـ Cloudflare
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
    }
    .success-card {
        border-left-color: #10b981;
    }
    .warning-card {
        border-left-color: #f59e0b;
    }
    .error-card {
        border-left-color: #ef4444;
    }
    .cloudflare-badge {
        background: #f97316;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #1e40af, #2563eb);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

class CloudflareBlueBadgeApp:
    def __init__(self):
        self.business_data = {
            'name': 'سمة السعودية',
            'domain': 'samma-sa.com',
            'country': 'SA',
            'phone': '+966 XX XXX XXXX',
            'address': 'المملكة العربية السعودية',
            'email': 'info@samma-sa.com'
        }
        
        # بيانات Cloudflare
        self.cloudflare_info = {
            'deployed': CLOUDFLARE_MODE,
            'deployment_time': datetime.datetime.now().isoformat(),
            'version': '1.0.0'
        }
        
    def main_header(self):
        """العنوان الرئيسي"""
        st.markdown("""
        <div class="main-header">
            <h1>🔵 تطبيق العلامة الزرقاء - Cloudflare Pages</h1>
            <h3>Blue Badge Application - Cloudflare Pages</h3>
            <p>أداة متقدمة للحصول على العلامة الزرقاء في Google My Business</p>
        </div>
        """, unsafe_allow_html=True)
        
        # شارة Cloudflare
        if self.cloudflare_info['deployed']:
            st.markdown("""
            <div class="cloudflare-badge">
                🚀 تم النشر على Cloudflare Pages
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("🌐 التطبيق يعمل محلياً - يمكن نشره على Cloudflare Pages")
    
    def sidebar_config(self):
        """إعداد الشريط الجانبي"""
        st.sidebar.title("⚙️ الإعدادات")
        
        # معلومات النشاط التجاري
        st.sidebar.subheader("🏢 معلومات النشاط التجاري")
        self.business_data['name'] = st.sidebar.text_input("اسم النشاط", self.business_data['name'])
        self.business_data['domain'] = st.sidebar.text_input("الدومين", self.business_data['domain'])
        self.business_data['country'] = st.sidebar.selectbox("البلد", ['SA', 'AE', 'KW', 'BH', 'OM', 'QA'])
        self.business_data['phone'] = st.sidebar.text_input("الهاتف", self.business_data['phone'])
        self.business_data['email'] = st.sidebar.text_input("البريد الإلكتروني", self.business_data['email'])
        
        # معلومات Cloudflare
        st.sidebar.subheader("☁️ معلومات Cloudflare")
        st.sidebar.info(f"**الحالة:** {'نشر' if self.cloudflare_info['deployed'] else 'محلي'}")
        st.sidebar.info(f"**الإصدار:** {self.cloudflare_info['version']}")
        st.sidebar.info(f"**وقت النشر:** {self.cloudflare_info['deployment_time'][:19]}")
        
        # إعدادات متقدمة
        st.sidebar.subheader("🔧 إعدادات متقدمة")
        auto_check = st.sidebar.checkbox("فحص تلقائي كل ساعة", value=True)
        notifications = st.sidebar.checkbox("إشعارات فورية", value=True)
        
        return auto_check, notifications
    
    def dashboard_overview(self):
        """لوحة المعلومات العامة"""
        st.header("📊 لوحة المعلومات العامة")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card success-card">
                <h3>🌐 حالة الموقع</h3>
                <h2>✅ يعمل</h2>
                <p>آخر فحص: منذ 5 دقائق</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card warning-card">
                <h3>🔍 DNS</h3>
                <h2>⚠️ يحتاج تحسين</h2>
                <p>3 سجلات مفقودة</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card success-card">
                <h3>📧 البريد الإلكتروني</h3>
                <h2>✅ جاهز</h2>
                <p>25 عنوان تم إنشاؤه</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card error-card">
                <h3>📝 الشكاوى</h3>
                <h2>❌ غير جاهز</h2>
                <p>0 رسالة تم إنشاؤها</p>
            </div>
            """, unsafe_allow_html=True)
        
        # معلومات Cloudflare
        if self.cloudflare_info['deployed']:
            st.success("🚀 التطبيق يعمل على Cloudflare Pages - متاح عالمياً!")
        else:
            st.info("💡 يمكن نشر التطبيق على Cloudflare Pages للوصول العالمي")
    
    def dns_checker_cloudflare(self):
        """فاحص DNS متوافق مع Cloudflare"""
        st.header("🌐 فاحص DNS - Cloudflare Compatible")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            domain = st.text_input("أدخل الدومين للفحص", self.business_data['domain'])
            
            if st.button("🔍 فحص DNS", type="primary"):
                with st.spinner("جاري فحص DNS..."):
                    results = self.perform_dns_check(domain)
                    self.display_dns_results(results)
        
        with col2:
            st.info("""
            **💡 نصائح:**
            - تأكد من صحة الدومين
            - انتظر 24-48 ساعة لانتشار DNS
            - استخدم أدوات فحص إضافية
            - **Cloudflare DNS** سريع وموثوق
            """)
    
    def perform_dns_check(self, domain):
        """تنفيذ فحص DNS"""
        results = {
            'domain': domain,
            'timestamp': datetime.datetime.now().isoformat(),
            'records': {},
            'cloudflare_compatible': True
        }
        
        try:
            # فحص سجلات TXT
            txt_records = []
            try:
                answers = dns.resolver.resolve(domain, 'TXT')
                for rdata in answers:
                    txt_records.append(str(rdata).strip('"'))
            except:
                pass
            results['records']['TXT'] = txt_records
            
            # فحص سجلات A
            a_records = []
            try:
                answers = dns.resolver.resolve(domain, 'A')
                for rdata in answers:
                    a_records.append(str(rdata))
            except:
                pass
            results['records']['A'] = a_records
            
            # فحص سجلات MX
            mx_records = []
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                for rdata in answers:
                    mx_records.append(f"{rdata.preference} {rdata.exchange}")
            except:
                pass
            results['records']['MX'] = mx_records
            
            # فحص سجلات CNAME
            cname_records = []
            try:
                answers = dns.resolver.resolve(f"www.{domain}", 'CNAME')
                for rdata in answers:
                    cname_records.append(str(rdata))
            except:
                pass
            results['records']['CNAME'] = cname_records
            
        except Exception as e:
            st.error(f"خطأ في فحص DNS: {e}")
        
        return results
    
    def display_dns_results(self, results):
        """عرض نتائج DNS"""
        st.subheader(f"📋 نتائج فحص DNS: {results['domain']}")
        
        # عرض السجلات
        for record_type, records in results['records'].items():
            with st.expander(f"سجلات {record_type} ({len(records)})"):
                if records:
                    for record in records:
                        st.code(record)
                else:
                    st.warning(f"لا توجد سجلات {record_type}")
        
        # تحليل النتائج
        st.subheader("📊 تحليل النتائج")
        
        # البحث عن سجلات Google
        txt_records = results['records'].get('TXT', [])
        google_records = [r for r in txt_records if 'google-site-verification' in r]
        
        if google_records:
            st.success(f"✅ تم العثور على {len(google_records)} سجل Google!")
            for record in google_records:
                st.code(record)
        else:
            st.warning("⚠️ لم يتم العثور على سجلات Google")
            st.info("تحتاج لإضافة سجلات Google للتحقق من ملكية الدومين")
        
        # معلومات Cloudflare
        if self.cloudflare_info['deployed']:
            st.info("🌐 **نصيحة Cloudflare:** استخدم Cloudflare DNS للحصول على أداء أفضل وأمان أعلى")
        
        # إنشاء تقرير
        if st.button("📄 حفظ التقرير"):
            self.save_dns_report(results)
    
    def save_dns_report(self, results):
        """حفظ تقرير DNS"""
        filename = f"dns_report_{results['domain']}_{int(time.time())}.json"
        
        # تحويل إلى DataFrame
        df_data = []
        for record_type, records in results['records'].items():
            for record in records:
                df_data.append({
                    'نوع السجل': record_type,
                    'القيمة': record,
                    'الدومين': results['domain'],
                    'التاريخ': results['timestamp']
                })
        
        df = pd.DataFrame(df_data)
        
        # عرض البيانات
        st.dataframe(df)
        
        # تحميل التقرير
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 تحميل التقرير CSV",
            data=csv,
            file_name=filename.replace('.json', '.csv'),
            mime='text/csv'
        )
    
    def run(self):
        """تشغيل التطبيق"""
        self.main_header()
        
        # الشريط الجانبي
        auto_check, notifications = self.sidebar_config()
        
        # التبويبات
        tab1, tab2 = st.tabs([
            "📊 لوحة المعلومات", "🌐 فاحص DNS"
        ])
        
        with tab1:
            self.dashboard_overview()
        
        with tab2:
            self.dns_checker_cloudflare()

def main():
    """الدالة الرئيسية"""
    app = CloudflareBlueBadgeApp()
    app.run()

if __name__ == "__main__":
    main()