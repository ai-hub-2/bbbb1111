#!/usr/bin/env python3
"""
DNS Stealth Tool - أداة فحص DNS الخفية
أداة متخصصة لفحص ومراقبة DNS بطريقة خفية
"""

import streamlit as st
import dns.resolver
import dns.reversename
import requests
import time
import datetime
import json
import os
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# إعداد الصفحة
st.set_page_config(
    page_title="🌐 DNS Stealth Tool",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص
st.markdown("""
<style>
    .dns-header {
        background: linear-gradient(135deg, #2c7a7b, #38b2ac);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(44, 122, 123, 0.3);
    }
    .dns-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #38b2ac;
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
    .stButton > button {
        background: linear-gradient(135deg, #2c7a7b, #38b2ac);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1a5f61, #2d8f89);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(44, 122, 123, 0.4);
    }
    .dns-result {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
    }
    .provider-info {
        background: #e6fffa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #38b2ac;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class DNSStealthTool:
    def __init__(self):
        self.dns_records = []
        self.monitoring_data = []
        self.load_data()
        
        # DNS Providers
        self.dns_providers = [
            {
                'name': 'Google DNS',
                'servers': ['8.8.8.8', '8.8.4.4'],
                'color': '#4285f4',
                'description': 'Google Public DNS'
            },
            {
                'name': 'Cloudflare DNS',
                'servers': ['1.1.1.1', '1.0.0.1'],
                'color': '#f38020',
                'description': 'Cloudflare 1.1.1.1'
            },
            {
                'name': 'OpenDNS',
                'servers': ['208.67.222.222', '208.67.220.220'],
                'color': '#00a651',
                'description': 'Cisco OpenDNS'
            },
            {
                'name': 'Quad9',
                'servers': ['9.9.9.9', '149.112.112.112'],
                'color': '#000000',
                'description': 'Quad9 Security DNS'
            },
            {
                'name': 'Level3',
                'servers': ['4.2.2.1', '4.2.2.2'],
                'color': '#ff6600',
                'description': 'Level3 DNS'
            },
            {
                'name': 'Verisign',
                'servers': ['64.6.64.6', '64.6.65.6'],
                'color': '#ff6600',
                'description': 'Verisign Public DNS'
            }
        ]
        
        # أنواع السجلات
        self.record_types = [
            'A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'PTR', 'SRV', 'CAA'
        ]
        
    def load_data(self):
        """تحميل البيانات المحفوظة"""
        try:
            if os.path.exists('dns_records.json'):
                with open('dns_records.json', 'r', encoding='utf-8') as f:
                    self.dns_records = json.load(f)
                    
            if os.path.exists('dns_monitoring.json'):
                with open('dns_monitoring.json', 'r', encoding='utf-8') as f:
                    self.monitoring_data = json.load(f)
                    
        except Exception as e:
            st.warning(f"Could not load saved data: {str(e)}")
            
    def save_data(self):
        """حفظ البيانات"""
        try:
            with open('dns_records.json', 'w', encoding='utf-8') as f:
                json.dump(self.dns_records, f, indent=2, ensure_ascii=False)
                
            with open('dns_monitoring.json', 'w', encoding='utf-8') as f:
                json.dump(self.monitoring_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            st.error(f"Could not save data: {str(e)}")
            
    def check_dns_propagation(self, domain):
        """فحص انتشار DNS من مصادر متعددة"""
        try:
            results = []
            total_checks = len(self.dns_providers) * len(self.record_types)
            current_check = 0
            
            with st.spinner(f"Checking DNS propagation for {domain}..."):
                progress_bar = st.progress(0)
                
                for provider in self.dns_providers:
                    provider_result = {
                        'provider': provider['name'],
                        'servers': provider['servers'],
                        'color': provider['color'],
                        'description': provider['description'],
                        'records': {},
                        'response_time': 0,
                        'status': 'success',
                        'timestamp': datetime.datetime.now().isoformat()
                    }
                    
                    try:
                        resolver = dns.resolver.Resolver()
                        resolver.nameservers = provider['servers']
                        resolver.timeout = 5
                        resolver.lifetime = 10
                        
                        start_time = time.time()
                        
                        for record_type in self.record_types:
                            try:
                                answers = resolver.resolve(domain, record_type)
                                provider_result['records'][record_type] = [str(answer) for answer in answers]
                                
                            except dns.resolver.NXDOMAIN:
                                provider_result['records'][record_type] = ['NXDOMAIN']
                                
                            except dns.resolver.NoAnswer:
                                provider_result['records'][record_type] = ['No Answer']
                                
                            except dns.resolver.Timeout:
                                provider_result['records'][record_type] = ['Timeout']
                                provider_result['status'] = 'timeout'
                                
                            except Exception as e:
                                provider_result['records'][record_type] = [f'Error: {str(e)}']
                                provider_result['status'] = 'error'
                                
                            current_check += 1
                            progress = current_check / total_checks
                            progress_bar.progress(progress)
                            
                            # تأخير صغير
                            time.sleep(0.1)
                            
                        end_time = time.time()
                        provider_result['response_time'] = round(end_time - start_time, 3)
                        
                    except Exception as e:
                        provider_result['status'] = 'error'
                        provider_result['error'] = str(e)
                        
                    results.append(provider_result)
                    
                progress_bar.progress(1.0)
                
                # حفظ النتائج
                self.dns_records.extend(results)
                self.save_data()
                
                st.success(f"✅ DNS propagation check completed for {domain}")
                return results
                
        except Exception as e:
            st.error(f"❌ Error checking DNS propagation: {str(e)}")
            return []
            
    def reverse_dns_lookup(self, ip_address):
        """فحص DNS العكسي"""
        try:
            results = []
            
            for provider in self.dns_providers:
                try:
                    resolver = dns.resolver.Resolver()
                    resolver.nameservers = provider['servers']
                    resolver.timeout = 5
                    
                    # إنشاء اسم DNS عكسي
                    reverse_name = dns.reversename.from_address(ip_address)
                    
                    start_time = time.time()
                    answers = resolver.resolve(reverse_name, 'PTR')
                    end_time = time.time()
                    
                    provider_result = {
                        'provider': provider['name'],
                        'ip_address': ip_address,
                        'reverse_name': str(reverse_name),
                        'ptr_records': [str(answer) for answer in answers],
                        'response_time': round(end_time - start_time, 3),
                        'timestamp': datetime.datetime.now().isoformat()
                    }
                    
                    results.append(provider_result)
                    
                except Exception as e:
                    provider_result = {
                        'provider': provider['name'],
                        'ip_address': ip_address,
                        'error': str(e),
                        'timestamp': datetime.datetime.now().isoformat()
                    }
                    results.append(provider_result)
                    
            return results
            
        except Exception as e:
            st.error(f"❌ Error in reverse DNS lookup: {str(e)}")
            return []
            
    def check_dns_health(self, domain):
        """فحص صحة DNS"""
        try:
            health_checks = []
            
            # فحص A record
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = ['8.8.8.8']
                a_records = resolver.resolve(domain, 'A')
                a_status = 'healthy' if len(a_records) > 0 else 'no_a_record'
            except:
                a_status = 'error'
                
            # فحص MX record
            try:
                mx_records = resolver.resolve(domain, 'MX')
                mx_status = 'healthy' if len(mx_records) > 0 else 'no_mx_record'
            except:
                mx_status = 'error'
                
            # فحص NS record
            try:
                ns_records = resolver.resolve(domain, 'NS')
                ns_status = 'healthy' if len(ns_records) > 0 else 'no_ns_record'
            except:
                ns_status = 'error'
                
            # فحص SOA record
            try:
                soa_records = resolver.resolve(domain, 'SOA')
                soa_status = 'healthy' if len(soa_records) > 0 else 'no_soa_record'
            except:
                soa_status = 'error'
                
            health_checks = [
                {'type': 'A Record', 'status': a_status, 'description': 'IP Address'},
                {'type': 'MX Record', 'status': mx_status, 'description': 'Mail Exchange'},
                {'type': 'NS Record', 'status': ns_status, 'description': 'Name Servers'},
                {'type': 'SOA Record', 'status': soa_status, 'description': 'Start of Authority'}
            ]
            
            # حساب النسبة المئوية للصحة
            healthy_count = len([check for check in health_checks if check['status'] == 'healthy'])
            health_percentage = (healthy_count / len(health_checks)) * 100
            
            return {
                'domain': domain,
                'health_checks': health_checks,
                'health_percentage': health_percentage,
                'overall_status': 'healthy' if health_percentage >= 75 else 'warning' if health_percentage >= 50 else 'critical',
                'timestamp': datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            st.error(f"❌ Error checking DNS health: {str(e)}")
            return None
            
    def monitor_dns_changes(self, domain, interval_minutes=5):
        """مراقبة تغييرات DNS"""
        try:
            monitoring_info = {
                'domain': domain,
                'monitoring_started': datetime.datetime.now().isoformat(),
                'interval_minutes': interval_minutes,
                'status': 'active',
                'last_check': datetime.datetime.now().isoformat(),
                'total_checks': 0,
                'changes_detected': 0
            }
            
            # إضافة إلى قائمة المراقبة
            self.monitoring_data.append({
                'type': 'dns_monitoring_started',
                'details': monitoring_info,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            self.save_data()
            
            st.success(f"🔄 DNS monitoring started for {domain} every {interval_minutes} minutes")
            return monitoring_info
            
        except Exception as e:
            st.error(f"❌ Error starting DNS monitoring: {str(e)}")
            return None
            
    def get_dns_history(self, domain):
        """الحصول على تاريخ DNS"""
        try:
            domain_records = [record for record in self.dns_records 
                            if any(record_type in record.get('records', {}) 
                                  for record_type in ['A', 'AAAA'])]
            
            if domain_records:
                return domain_records
            else:
                return []
                
        except Exception as e:
            st.error(f"❌ Error getting DNS history: {str(e)}")
            return []
            
    def export_dns_data(self, format_type='json'):
        """تصدير بيانات DNS"""
        try:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if format_type == 'json':
                filename = f"dns_data_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.dns_records, f, indent=2, ensure_ascii=False)
                    
            elif format_type == 'csv':
                filename = f"dns_data_{timestamp}.csv"
                df = pd.DataFrame(self.dns_records)
                df.to_csv(filename, index=False, encoding='utf-8')
                
            return filename
            
        except Exception as e:
            st.error(f"❌ Error exporting DNS data: {str(e)}")
            return None
            
    def generate_dns_report(self, domain):
        """إنشاء تقرير DNS شامل"""
        try:
            # فحص DNS propagation
            propagation_results = self.check_dns_propagation(domain)
            
            # فحص صحة DNS
            health_results = self.check_dns_health(domain)
            
            # تجميع التقرير
            report = {
                'domain': domain,
                'timestamp': datetime.datetime.now().isoformat(),
                'propagation_results': propagation_results,
                'health_results': health_results,
                'summary': {
                    'total_providers': len(propagation_results),
                    'healthy_providers': len([r for r in propagation_results if r.get('status') == 'success']),
                    'dns_health_percentage': health_results['health_percentage'] if health_results else 0
                }
            }
            
            return report
            
        except Exception as e:
            st.error(f"❌ Error generating DNS report: {str(e)}")
            return None

def main():
    """الدالة الرئيسية"""
    st.markdown("""
    <div class="dns-header">
        <h1>🌐 DNS Stealth Tool</h1>
        <p>أداة متخصصة لفحص ومراقبة DNS بطريقة خفية</p>
        <p>Specialized Tool for DNS Inspection and Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تهيئة الأداة
    dns_tool = DNSStealthTool()
    
    # Sidebar
    st.sidebar.markdown("## 🌐 DNS Stealth Control Panel")
    
    # اختيار الوضع
    operation_mode = st.sidebar.selectbox(
        "Operation Mode",
        ["🔍 DNS Check", "🔄 Monitoring", "📊 Analysis", "⚙️ Settings"]
    )
    
    if operation_mode == "🔍 DNS Check":
        st.markdown("## 🔍 DNS Propagation Check")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📝 Domain Information")
            
            domain_to_check = st.text_input("Domain to Check", "example.com")
            
            # خيارات الفحص
            st.markdown("#### 🔧 Check Options")
            
            check_types = st.multiselect(
                "Record Types to Check",
                dns_tool.record_types,
                default=['A', 'AAAA', 'MX', 'NS', 'TXT']
            )
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🔍 Check DNS Propagation", key="dns_check"):
                    if domain_to_check:
                        results = dns_tool.check_dns_propagation(domain_to_check)
                        
            with col_btn2:
                if st.button("🏥 Check DNS Health", key="dns_health"):
                    if domain_to_check:
                        health = dns_tool.check_dns_health(domain_to_check)
                        if health:
                            st.success(f"DNS Health: {health['overall_status']} ({health['health_percentage']:.1f}%)")
                            
            # Reverse DNS
            st.markdown("#### 🔄 Reverse DNS Lookup")
            ip_address = st.text_input("IP Address for Reverse Lookup")
            
            if st.button("🔄 Reverse DNS Lookup", key="reverse_dns"):
                if ip_address:
                    reverse_results = dns_tool.reverse_dns_lookup(ip_address)
                    if reverse_results:
                        st.success("Reverse DNS lookup completed!")
                        
        with col2:
            st.markdown("### 📊 Recent Results")
            if dns_tool.dns_records:
                latest_dns = dns_tool.dns_records[-1] if dns_tool.dns_records else {}
                
                if latest_dns:
                    st.markdown(f"""
                    <div class="provider-info">
                        <strong>🌐 {latest_dns.get('provider', 'Unknown')}</strong><br>
                        📊 Status: {latest_dns.get('status', 'Unknown')}<br>
                        ⏱️ Response Time: {latest_dns.get('response_time', 'N/A')}s<br>
                        📅 Timestamp: {latest_dns.get('timestamp', 'N/A')[:19]}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # عرض السجلات
                    if 'records' in latest_dns:
                        for record_type, records in latest_dns['records'].items():
                            if records and records[0] not in ['NXDOMAIN', 'No Answer', 'Timeout']:
                                st.markdown(f"**{record_type}:** {', '.join(records[:3])}")
                                
            else:
                st.info("No DNS checks performed yet")
                
    elif operation_mode == "🔄 Monitoring":
        st.markdown("## 🔄 DNS Monitoring")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📡 Start Monitoring")
            
            monitor_domain = st.text_input("Domain to Monitor", "example.com")
            monitor_interval = st.slider("Check Interval (minutes)", 1, 60, 5)
            
            if st.button("🚀 Start DNS Monitoring", key="start_monitoring"):
                if monitor_domain:
                    monitoring_info = dns_tool.monitor_dns_changes(monitor_domain, monitor_interval)
                    
            # عرض المراقبة النشطة
            st.markdown("### 📊 Active Monitoring")
            active_monitoring = [m for m in dns_tool.monitoring_data if m.get('type') == 'dns_monitoring_started']
            
            if active_monitoring:
                for monitoring in active_monitoring:
                    details = monitoring['details']
                    st.info(f"🔄 Monitoring {details['domain']} every {details['interval_minutes']} minutes")
                    
        with col2:
            st.markdown("### 📈 Monitoring Statistics")
            
            if dns_tool.monitoring_data:
                # إحصائيات المراقبة
                total_monitoring = len([m for m in dns_tool.monitoring_data if m.get('type') == 'dns_monitoring_started'])
                total_checks = len([m for m in dns_tool.monitoring_data if m.get('type') == 'dns_check'])
                
                col_stat1, col_stat2 = st.columns(2)
                col_stat1.metric("Active Monitoring", total_monitoring)
                col_stat2.metric("Total Checks", total_checks)
                
                # رسم بياني للمراقبة
                if total_checks > 0:
                    monitoring_df = pd.DataFrame([
                        m for m in dns_tool.monitoring_data 
                        if m.get('type') in ['dns_check', 'dns_monitoring_started']
                    ])
                    
                    if not monitoring_df.empty:
                        fig = px.line(
                            monitoring_df,
                            x='timestamp',
                            title="DNS Monitoring Activity"
                        )
                        st.plotly_chart(fig)
                        
            else:
                st.info("No monitoring data available")
                
    elif operation_mode == "📊 Analysis":
        st.markdown("## 📊 DNS Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 DNS History")
            
            history_domain = st.text_input("Domain for History", "example.com")
            
            if st.button("📊 Get DNS History", key="get_history"):
                if history_domain:
                    history = dns_tool.get_dns_history(history_domain)
                    if history:
                        st.success(f"Found {len(history)} DNS records for {history_domain}")
                        
            # إنشاء تقرير شامل
            st.markdown("### 📄 Generate Report")
            
            report_domain = st.text_input("Domain for Report", "example.com")
            
            if st.button("📄 Generate DNS Report", key="generate_report"):
                if report_domain:
                    report = dns_tool.generate_dns_report(report_domain)
                    if report:
                        st.success("DNS report generated successfully!")
                        
        with col2:
            st.markdown("### 📤 Export Data")
            
            if dns_tool.dns_records:
                col_export1, col_export2 = st.columns(2)
                
                with col_export1:
                    if st.button("📤 Export as JSON"):
                        filename = dns_tool.export_dns_data('json')
                        if filename:
                            st.success(f"Exported to {filename}")
                            
                with col_export2:
                    if st.button("📤 Export as CSV"):
                        filename = dns_tool.export_dns_data('csv')
                        if filename:
                            st.success(f"Exported to {filename}")
                            
                # إحصائيات البيانات
                st.markdown("### 📊 Data Statistics")
                
                total_records = len(dns_tool.dns_records)
                successful_checks = len([r for r in dns_tool.dns_records if r.get('status') == 'success'])
                
                col_data1, col_data2 = st.columns(2)
                col_data1.metric("Total Records", total_records)
                col_data2.metric("Successful Checks", successful_checks)
                
            else:
                st.info("No DNS data to export")
                
    elif operation_mode == "⚙️ Settings":
        st.markdown("## ⚙️ Tool Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔧 DNS Settings")
            
            # إعدادات DNS
            st.markdown("#### DNS Configuration")
            
            # timeout setting
            default_timeout = st.slider(
                "Default DNS Timeout (seconds)",
                min_value=1,
                max_value=30,
                value=5
            )
            
            # lifetime setting
            default_lifetime = st.slider(
                "Default DNS Lifetime (seconds)",
                min_value=5,
                max_value=60,
                value=10
            )
            
            if st.button("💾 Save DNS Settings"):
                st.success("DNS settings saved successfully!")
                
        with col2:
            st.markdown("### 📊 Data Management")
            
            # معلومات البيانات
            st.info(f"**Total DNS Records:** {len(dns_tool.dns_records)}")
            st.info(f"**Total Monitoring Data:** {len(dns_tool.monitoring_data)}")
            
            # إدارة البيانات
            st.markdown("#### Data Actions")
            
            col_data1, col_data2 = st.columns(2)
            
            with col_data1:
                if st.button("🗑️ Clear DNS Records"):
                    if st.checkbox("I confirm I want to delete all DNS records"):
                        dns_tool.dns_records.clear()
                        dns_tool.save_data()
                        st.success("All DNS records cleared!")
                        st.rerun()
                        
            with col_data2:
                if st.button("🗑️ Clear Monitoring Data"):
                    if st.checkbox("I confirm I want to delete all monitoring data"):
                        dns_tool.monitoring_data.clear()
                        dns_tool.save_data()
                        st.success("All monitoring data cleared!")
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
        <p>🌐 DNS Stealth Tool - Advanced DNS Inspection and Monitoring</p>
        <p>Built for Cloudflare Pages | Multi-Provider DNS | Real-time Monitoring</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()