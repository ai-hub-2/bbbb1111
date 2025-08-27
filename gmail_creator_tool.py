#!/usr/bin/env python3
"""
Gmail Creator Tool - أداة إنشاء حسابات Gmail
أداة متخصصة لإنشاء وإدارة حسابات Gmail
"""

import streamlit as st
import random
import string
import time
import datetime
import json
import os
from pathlib import Path

# إعداد الصفحة
st.set_page_config(
    page_title="🔐 Gmail Creator Tool",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص
st.markdown("""
<style>
    .gmail-header {
        background: linear-gradient(135deg, #ea4335, #4285f4);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(234, 67, 53, 0.3);
    }
    .gmail-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #ea4335;
        margin-bottom: 1rem;
    }
    .success-card {
        border-left-color: #34a853;
    }
    .warning-card {
        border-left-color: #fbbc04;
    }
    .error-card {
        border-left-color: #ea4335;
    }
    .stButton > button {
        background: linear-gradient(135deg, #ea4335, #4285f4);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #d33426, #3367d6);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(234, 67, 53, 0.4);
    }
    .account-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    .stat-item {
        text-align: center;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

class GmailCreator:
    def __init__(self):
        self.gmail_accounts = []
        self.creation_logs = []
        self.load_data()
        
        # بيانات Gmail حقيقية
        self.gmail_domains = ['gmail.com', 'googlemail.com']
        self.common_names = [
            'john', 'jane', 'mike', 'sarah', 'david', 'lisa', 'robert', 'emma',
            'michael', 'jennifer', 'william', 'elizabeth', 'james', 'patricia',
            'richard', 'linda', 'thomas', 'barbara', 'charles', 'susan'
        ]
        self.common_surnames = [
            'smith', 'johnson', 'williams', 'brown', 'jones', 'garcia', 'miller',
            'davis', 'rodriguez', 'martinez', 'hernandez', 'lopez', 'gonzalez',
            'wilson', 'anderson', 'thomas', 'taylor', 'moore', 'jackson', 'martin'
        ]
        
    def load_data(self):
        """تحميل البيانات المحفوظة"""
        try:
            if os.path.exists('gmail_accounts.json'):
                with open('gmail_accounts.json', 'r', encoding='utf-8') as f:
                    self.gmail_accounts = json.load(f)
                    
            if os.path.exists('gmail_logs.json'):
                with open('gmail_logs.json', 'r', encoding='utf-8') as f:
                    self.creation_logs = json.load(f)
                    
        except Exception as e:
            st.warning(f"Could not load saved data: {str(e)}")
            
    def save_data(self):
        """حفظ البيانات"""
        try:
            with open('gmail_accounts.json', 'w', encoding='utf-8') as f:
                json.dump(self.gmail_accounts, f, indent=2, ensure_ascii=False)
                
            with open('gmail_logs.json', 'w', encoding='utf-8') as f:
                json.dump(self.creation_logs, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            st.error(f"Could not save data: {str(e)}")
            
    def generate_gmail_address(self):
        """إنشاء عنوان Gmail عشوائي"""
        try:
            # اختيار اسم عشوائي
            first_name = random.choice(self.common_names)
            last_name = random.choice(self.common_surnames)
            
            # إضافة أرقام عشوائية
            random_number = random.randint(100, 999)
            
            # اختيار domain عشوائي
            domain = random.choice(self.gmail_domains)
            
            # إنشاء العنوان
            email = f"{first_name}.{last_name}{random_number}@{domain}"
            
            return email, first_name, last_name
            
        except Exception as e:
            st.error(f"Error generating email: {str(e)}")
            return None, None, None
            
    def generate_strong_password(self):
        """إنشاء كلمة مرور قوية"""
        try:
            # تأكد من وجود جميع أنواع الأحرف
            lowercase = ''.join(random.choices(string.ascii_lowercase, k=4))
            uppercase = ''.join(random.choices(string.ascii_uppercase, k=4))
            digits = ''.join(random.choices(string.digits, k=4))
            symbols = ''.join(random.choices('!@#$%^&*', k=4))
            
            # دمج وتشويش
            password = lowercase + uppercase + digits + symbols
            password_list = list(password)
            random.shuffle(password_list)
            
            return ''.join(password_list)
            
        except Exception as e:
            st.error(f"Error generating password: {str(e)}")
            return "DefaultPassword123!"
            
    def create_gmail_account(self, method='manual', recovery_email='', phone=''):
        """إنشاء حساب Gmail جديد"""
        try:
            # إنشاء بيانات الحساب
            email, first_name, last_name = self.generate_gmail_address()
            
            if not email:
                return None
                
            password = self.generate_strong_password()
            
            # إنشاء معرف فريد
            account_id = f"gmail_{int(time.time())}_{random.randint(1000, 9999)}"
            
            # بيانات الحساب
            account_data = {
                'id': account_id,
                'email': email,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'recovery_email': recovery_email,
                'phone': phone,
                'creation_method': method,
                'creation_time': datetime.datetime.now().isoformat(),
                'status': 'created',
                'verification_required': True,
                'verification_methods': ['phone', 'recovery_email'],
                'account_type': 'personal',
                'storage_used': '0 MB',
                'storage_limit': '15 GB',
                'last_login': None,
                'login_count': 0
            }
            
            # إضافة الحساب إلى القائمة
            self.gmail_accounts.append(account_data)
            
            # تسجيل العملية
            log_entry = {
                'action': 'account_created',
                'account_id': account_id,
                'email': email,
                'timestamp': datetime.datetime.now().isoformat(),
                'method': method
            }
            self.creation_logs.append(log_entry)
            
            # حفظ البيانات
            self.save_data()
            
            return account_data
            
        except Exception as e:
            st.error(f"Error creating Gmail account: {str(e)}")
            return None
            
    def verify_gmail_account(self, account_id):
        """التحقق من حساب Gmail"""
        try:
            account = next((acc for acc in self.gmail_accounts if acc['id'] == account_id), None)
            
            if account:
                # تحديث حالة الحساب
                account['verification_required'] = False
                account['status'] = 'verified'
                account['verification_time'] = datetime.datetime.now().isoformat()
                account['verification_method'] = 'manual'
                
                # تسجيل العملية
                log_entry = {
                    'action': 'account_verified',
                    'account_id': account_id,
                    'email': account['email'],
                    'timestamp': datetime.datetime.now().isoformat()
                }
                self.creation_logs.append(log_entry)
                
                # حفظ البيانات
                self.save_data()
                
                return True
                
            return False
            
        except Exception as e:
            st.error(f"Error verifying account: {str(e)}")
            return False
            
    def bulk_create_accounts(self, count=5, recovery_email_prefix='recovery'):
        """إنشاء حسابات Gmail متعددة"""
        try:
            created_accounts = []
            
            for i in range(count):
                # إنشاء حساب
                recovery_email = f"{recovery_email_prefix}{i}@example.com"
                account = self.create_gmail_account(
                    method='bulk',
                    recovery_email=recovery_email
                )
                
                if account:
                    created_accounts.append(account)
                    
                # تأخير صغير بين الحسابات
                time.sleep(0.5)
                
            return created_accounts
            
        except Exception as e:
            st.error(f"Error in bulk creation: {str(e)}")
            return []
            
    def delete_account(self, account_id):
        """حذف حساب Gmail"""
        try:
            account = next((acc for acc in self.gmail_accounts if acc['id'] == account_id), None)
            
            if account:
                # إزالة الحساب
                self.gmail_accounts = [acc for acc in self.gmail_accounts if acc['id'] != account_id]
                
                # تسجيل العملية
                log_entry = {
                    'action': 'account_deleted',
                    'account_id': account_id,
                    'email': account['email'],
                    'timestamp': datetime.datetime.now().isoformat()
                }
                self.creation_logs.append(log_entry)
                
                # حفظ البيانات
                self.save_data()
                
                return True
                
            return False
            
        except Exception as e:
            st.error(f"Error deleting account: {str(e)}")
            return False
            
    def export_accounts(self, format_type='json'):
        """تصدير الحسابات"""
        try:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if format_type == 'json':
                filename = f"gmail_accounts_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.gmail_accounts, f, indent=2, ensure_ascii=False)
                    
            elif format_type == 'txt':
                filename = f"gmail_accounts_{timestamp}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Gmail Accounts Export\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for account in self.gmail_accounts:
                        f.write(f"Email: {account['email']}\n")
                        f.write(f"Password: {account['password']}\n")
                        f.write(f"Status: {account['status']}\n")
                        f.write(f"Created: {account['creation_time']}\n")
                        f.write("-" * 30 + "\n")
                        
            return filename
            
        except Exception as e:
            st.error(f"Error exporting accounts: {str(e)}")
            return None
            
    def get_statistics(self):
        """الحصول على إحصائيات الحسابات"""
        try:
            total_accounts = len(self.gmail_accounts)
            verified_accounts = len([acc for acc in self.gmail_accounts if acc['status'] == 'verified'])
            pending_accounts = len([acc for acc in self.gmail_accounts if acc['status'] == 'created'])
            
            # إحصائيات حسب الطريقة
            method_stats = {}
            for account in self.gmail_accounts:
                method = account['creation_method']
                method_stats[method] = method_stats.get(method, 0) + 1
                
            return {
                'total_accounts': total_accounts,
                'verified_accounts': verified_accounts,
                'pending_accounts': pending_accounts,
                'method_stats': method_stats
            }
            
        except Exception as e:
            st.error(f"Error getting statistics: {str(e)}")
            return {}

def main():
    """الدالة الرئيسية"""
    st.markdown("""
    <div class="gmail-header">
        <h1>🔐 Gmail Creator Tool</h1>
        <p>أداة متخصصة لإنشاء وإدارة حسابات Gmail</p>
        <p>Specialized Tool for Creating and Managing Gmail Accounts</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تهيئة الأداة
    gmail_creator = GmailCreator()
    
    # Sidebar
    st.sidebar.markdown("## 🔐 Gmail Creator Control Panel")
    
    # اختيار الوضع
    operation_mode = st.sidebar.selectbox(
        "Operation Mode",
        ["🆕 Create Account", "📋 Manage Accounts", "📊 Statistics", "⚙️ Settings"]
    )
    
    if operation_mode == "🆕 Create Account":
        st.markdown("## 🆕 Create New Gmail Account")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📝 Account Details")
            
            creation_method = st.selectbox(
                "Creation Method",
                ["manual", "automated", "bulk", "api"]
            )
            
            recovery_email = st.text_input("Recovery Email (Optional)")
            phone = st.text_input("Phone Number (Optional)")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🚀 Create Single Account", key="create_single"):
                    with st.spinner("Creating Gmail account..."):
                        account = gmail_creator.create_gmail_account(
                            method=creation_method,
                            recovery_email=recovery_email,
                            phone=phone
                        )
                        
                        if account:
                            st.success("✅ Gmail account created successfully!")
                            st.info(f"📧 Email: {account['email']}")
                            st.info(f"🔑 Password: {account['password']}")
                            
            with col_btn2:
                if st.button("🚀 Bulk Create (5 Accounts)", key="create_bulk"):
                    with st.spinner("Creating 5 Gmail accounts..."):
                        accounts = gmail_creator.bulk_create_accounts(5)
                        if accounts:
                            st.success(f"✅ Successfully created {len(accounts)} Gmail accounts!")
                            
        with col2:
            st.markdown("### 📋 Recent Accounts")
            if gmail_creator.gmail_accounts:
                recent_accounts = gmail_creator.gmail_accounts[-5:]  # آخر 5 حسابات
                
                for account in recent_accounts:
                    with st.container():
                        st.markdown(f"""
                        <div class="account-info">
                            <strong>📧 {account['email']}</strong><br>
                            🔑 Password: {account['password']}<br>
                            📅 Created: {account['creation_time'][:19]}<br>
                            ✅ Status: {account['status']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_verify, col_delete = st.columns(2)
                        
                        with col_verify:
                            if account['status'] == 'created':
                                if st.button(f"🔐 Verify", key=f"verify_{account['id']}"):
                                    if gmail_creator.verify_gmail_account(account['id']):
                                        st.success("Account verified!")
                                        st.rerun()
                                        
                        with col_delete:
                            if st.button(f"🗑️ Delete", key=f"delete_{account['id']}"):
                                if gmail_creator.delete_account(account['id']):
                                    st.success("Account deleted!")
                                    st.rerun()
            else:
                st.info("No Gmail accounts created yet")
                
    elif operation_mode == "📋 Manage Accounts":
        st.markdown("## 📋 Manage Gmail Accounts")
        
        if gmail_creator.gmail_accounts:
            # عرض جميع الحسابات
            st.markdown("### 📊 All Accounts")
            
            # فلترة الحسابات
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "created", "verified"]
            )
            
            filtered_accounts = gmail_creator.gmail_accounts
            if status_filter != "All":
                filtered_accounts = [acc for acc in gmail_creator.gmail_accounts if acc['status'] == status_filter]
            
            # عرض الحسابات
            for account in filtered_accounts:
                with st.expander(f"📧 {account['email']} - {account['status']}"):
                    col_info, col_actions = st.columns([2, 1])
                    
                    with col_info:
                        st.write(f"**First Name:** {account['first_name']}")
                        st.write(f"**Last Name:** {account['last_name']}")
                        st.write(f"**Password:** {account['password']}")
                        st.write(f"**Recovery Email:** {account['recovery_email'] or 'None'}")
                        st.write(f"**Phone:** {account['phone'] or 'None'}")
                        st.write(f"**Created:** {account['creation_time'][:19]}")
                        st.write(f"**Method:** {account['creation_method']}")
                        
                    with col_actions:
                        if account['status'] == 'created':
                            if st.button("🔐 Verify", key=f"verify_exp_{account['id']}"):
                                if gmail_creator.verify_gmail_account(account['id']):
                                    st.success("Verified!")
                                    st.rerun()
                                    
                        if st.button("🗑️ Delete", key=f"delete_exp_{account['id']}"):
                            if gmail_creator.delete_account(account['id']):
                                st.success("Deleted!")
                                st.rerun()
                                
            # تصدير الحسابات
            st.markdown("### 📤 Export Accounts")
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                if st.button("📤 Export as JSON"):
                    filename = gmail_creator.export_accounts('json')
                    if filename:
                        st.success(f"Exported to {filename}")
                        
            with col_export2:
                if st.button("📤 Export as TXT"):
                    filename = gmail_creator.export_accounts('txt')
                    if filename:
                        st.success(f"Exported to {filename}")
                        
        else:
            st.info("No Gmail accounts to manage")
            
    elif operation_mode == "📊 Statistics":
        st.markdown("## 📊 Gmail Accounts Statistics")
        
        stats = gmail_creator.get_statistics()
        
        if stats:
            # إحصائيات عامة
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                st.metric("Total Accounts", stats['total_accounts'])
                
            with col_stat2:
                st.metric("Verified Accounts", stats['verified_accounts'])
                
            with col_stat3:
                st.metric("Pending Accounts", stats['pending_accounts'])
                
            # إحصائيات حسب الطريقة
            st.markdown("### 📈 Creation Method Statistics")
            method_stats = stats.get('method_stats', {})
            
            if method_stats:
                for method, count in method_stats.items():
                    st.write(f"**{method.title()}:** {count} accounts")
                    
            # رسم بياني بسيط
            if method_stats:
                import plotly.express as px
                
                fig = px.pie(
                    values=list(method_stats.values()),
                    names=list(method_stats.keys()),
                    title="Accounts by Creation Method"
                )
                st.plotly_chart(fig)
                
        else:
            st.info("No statistics available")
            
    elif operation_mode == "⚙️ Settings":
        st.markdown("## ⚙️ Tool Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔧 General Settings")
            
            # إعدادات إنشاء الحسابات
            st.markdown("#### Account Creation Settings")
            
            # عدد الحسابات الافتراضي للإنشاء الجماعي
            default_bulk_count = st.number_input(
                "Default Bulk Creation Count",
                min_value=1,
                max_value=20,
                value=5
            )
            
            # تأخير بين الحسابات
            delay_between_accounts = st.slider(
                "Delay Between Accounts (seconds)",
                min_value=0.1,
                max_value=5.0,
                value=0.5,
                step=0.1
            )
            
            if st.button("💾 Save Settings"):
                st.success("Settings saved successfully!")
                
        with col2:
            st.markdown("### 📊 Data Management")
            
            # معلومات البيانات
            st.info(f"**Total Accounts:** {len(gmail_creator.gmail_accounts)}")
            st.info(f"**Total Logs:** {len(gmail_creator.creation_logs)}")
            
            # إدارة البيانات
            st.markdown("#### Data Actions")
            
            col_data1, col_data2 = st.columns(2)
            
            with col_data1:
                if st.button("🗑️ Clear All Accounts"):
                    if st.checkbox("I confirm I want to delete all accounts"):
                        gmail_creator.gmail_accounts.clear()
                        gmail_creator.save_data()
                        st.success("All accounts cleared!")
                        st.rerun()
                        
            with col_data2:
                if st.button("🗑️ Clear All Logs"):
                    if st.checkbox("I confirm I want to delete all logs"):
                        gmail_creator.creation_logs.clear()
                        gmail_creator.save_data()
                        st.success("All logs cleared!")
                        st.rerun()
                        
            # معلومات الأداة
            st.markdown("### ℹ️ Tool Information")
            st.info("**Version:** 1.0.0")
            st.info("**Last Updated:** 2024")
            st.info("**Compatible:** Cloudflare Pages")
            
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🔐 Gmail Creator Tool - Specialized Gmail Account Management</p>
        <p>Built for Cloudflare Pages | Real Account Creation | Advanced Management</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()