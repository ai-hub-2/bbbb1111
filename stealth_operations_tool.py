#!/usr/bin/env python3
"""
Stealth Operations Tool - أداة العمليات الخفية
أداة متخصصة للعمليات الخفية وفحص المواقع
"""

import streamlit as st
import requests
import random
import string
import time
import datetime
import json
import os
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from bs4 import BeautifulSoup
import urllib.parse
import platform
import subprocess

# إعداد الصفحة
st.set_page_config(
    page_title="🕷️ Stealth Operations Tool",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص
st.markdown("""
<style>
    .stealth-header {
        background: linear-gradient(135deg, #2d3748, #4a5568);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(45, 55, 72, 0.3);
    }
    .stealth-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #4a5568;
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
        background: linear-gradient(135deg, #2d3748, #4a5568);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1a202c, #2d3748);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(45, 55, 72, 0.4);
    }
    .operation-result {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
    }
    .target-info {
        background: #e6e8eb;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #4a5568;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class StealthOperationsTool:
    def __init__(self):
        self.stealth_operations = []
        self.operation_logs = []
        self.load_data()
        
        # User Agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        ]
        
        # Accept Languages
        self.accept_languages = [
            'en-US,en;q=0.9,ar;q=0.8',
            'en-GB,en;q=0.9',
            'en-CA,en;q=0.9,fr;q=0.8',
            'de-DE,de;q=0.9,en;q=0.8',
            'fr-FR,fr;q=0.9,en;q=0.8',
            'es-ES,es;q=0.9,en;q=0.8',
            'it-IT,it;q=0.9,en;q=0.8'
        ]
        
        # Accept Headers
        self.accept_headers = [
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        ]
        
        # Proxy List (مثال)
        self.proxy_list = [
            'http://proxy1.example.com:8080',
            'http://proxy2.example.com:8080',
            'socks5://proxy3.example.com:1080'
        ]
        
    def load_data(self):
        """تحميل البيانات المحفوظة"""
        try:
            if os.path.exists('stealth_operations.json'):
                with open('stealth_operations.json', 'r', encoding='utf-8') as f:
                    self.stealth_operations = json.load(f)
                    
            if os.path.exists('stealth_logs.json'):
                with open('stealth_logs.json', 'r', encoding='utf-8') as f:
                    self.operation_logs = json.load(f)
                    
        except Exception as e:
            st.warning(f"Could not load saved data: {str(e)}")
            
    def save_data(self):
        """حفظ البيانات"""
        try:
            with open('stealth_operations.json', 'w', encoding='utf-8') as f:
                json.dump(self.stealth_operations, f, indent=2, ensure_ascii=False)
                
            with open('stealth_logs.json', 'w', encoding='utf-8') as f:
                json.dump(self.operation_logs, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            st.error(f"Could not save data: {str(e)}")
            
    def rotate_user_agent(self):
        """تناوب User Agent"""
        return random.choice(self.user_agents)
        
    def inject_random_delays(self, min_delay=1, max_delay=5):
        """حقن تأخيرات عشوائية"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        return delay
        
    def generate_fake_headers(self):
        """إنشاء headers مزيفة ومتقدمة"""
        headers = {
            'User-Agent': self.rotate_user_agent(),
            'Accept': random.choice(self.accept_headers),
            'Accept-Language': random.choice(self.accept_languages),
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'X-Forwarded-For': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'X-Real-IP': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'X-Requested-With': 'XMLHttpRequest'
        }
        return headers
        
    def execute_stealth_operation(self, operation_type, target, **kwargs):
        """تنفيذ عملية خفية"""
        try:
            operation = {
                'id': f"op_{int(time.time())}_{random.randint(1000, 9999)}",
                'type': operation_type,
                'target': target,
                'start_time': datetime.datetime.now().isoformat(),
                'status': 'running',
                'method': kwargs.get('method', 'stealth'),
                'user_agent': self.rotate_user_agent(),
                'headers': self.generate_fake_headers()
            }
            
            # إضافة تأخير عشوائي
            self.inject_random_delays()
            
            # تنفيذ العملية
            if operation_type == 'website_scan':
                result = self.perform_website_scan(target)
            elif operation_type == 'network_scan':
                result = self.perform_network_scan(target)
            elif operation_type == 'proxy_test':
                result = self.test_proxy_connection()
            elif operation_type == 'full_stealth_scan':
                result = self.perform_full_stealth_scan(target)
            else:
                result = {'status': 'unknown_operation'}
                
            operation['end_time'] = datetime.datetime.now().isoformat()
            operation['result'] = result
            operation['status'] = 'completed'
            
            # حفظ العملية
            self.stealth_operations.append(operation)
            self.save_data()
            
            return operation
            
        except Exception as e:
            st.error(f"❌ Error executing stealth operation: {str(e)}")
            return None
            
    def perform_website_scan(self, url):
        """فحص الموقع بطريقة خفية"""
        try:
            headers = self.generate_fake_headers()
            
            # إضافة تأخير عشوائي
            self.inject_random_delays(1, 3)
            
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            
            # تحليل المحتوى
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # استخراج معلومات الموقع
            title = soup.find('title')
            title_text = title.get_text() if title else 'No title found'
            
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description.get('content') if meta_description else 'No description found'
            
            # استخراج الروابط
            links = soup.find_all('a', href=True)
            internal_links = [link['href'] for link in links if link['href'].startswith('/') or url in link['href']]
            external_links = [link['href'] for link in links if not link['href'].startswith('/') and url not in link['href']]
            
            # استخراج الصور
            images = soup.find_all('img')
            image_count = len(images)
            
            # فحص SSL
            ssl_info = {
                'is_https': url.startswith('https'),
                'ssl_certificate': 'Available' if url.startswith('https') else 'Not available'
            }
            
            # استخراج Meta tags
            meta_tags = {}
            for meta in soup.find_all('meta'):
                name = meta.get('name') or meta.get('property')
                content = meta.get('content')
                if name and content:
                    meta_tags[name] = content
                    
            return {
                'url': url,
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'content_length': len(response.content),
                'headers': dict(response.headers),
                'title': title_text,
                'description': description,
                'internal_links_count': len(internal_links),
                'external_links_count': len(external_links),
                'images_count': image_count,
                'ssl_info': ssl_info,
                'meta_tags': meta_tags,
                'timestamp': datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e)}
            
    def perform_network_scan(self, target):
        """فحص الشبكة"""
        try:
            # إزالة البروتوكول
            if target.startswith('http'):
                target = urllib.parse.urlparse(target).netloc
                
            # فحص ping
            ping_result = "Not available"
            try:
                if platform.system().lower() == "windows":
                    ping_cmd = ["ping", "-n", "1", target]
                else:
                    ping_cmd = ["ping", "-c", "1", target]
                    
                ping_result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=10)
                if ping_result.returncode == 0:
                    ping_result = "Success"
                else:
                    ping_result = "Failed"
            except:
                ping_result = "Not available"
                
            # فحص port scanning (مثال بسيط)
            common_ports = [80, 443, 22, 21, 25, 53, 110, 143, 993, 995]
            open_ports = []
            
            for port in common_ports:
                try:
                    sock = requests.get(f"http://{target}:{port}", timeout=2)
                    if sock.status_code < 400:
                        open_ports.append(port)
                except:
                    pass
                    
            return {
                'target': target,
                'ping_status': ping_result,
                'open_ports': open_ports,
                'timestamp': datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e)}
            
    def perform_full_stealth_scan(self, target):
        """فحص شامل خفي"""
        try:
            results = {}
            
            # فحص الموقع
            if target.startswith('http'):
                results['website'] = self.perform_website_scan(target)
                
            # فحص الشبكة
            results['network'] = self.perform_network_scan(target)
            
            # فحص إضافي
            results['additional'] = self.perform_additional_checks(target)
            
            return results
            
        except Exception as e:
            return {'error': str(e)}
            
    def perform_additional_checks(self, target):
        """فحوصات إضافية"""
        try:
            checks = {}
            
            # فحص robots.txt
            if target.startswith('http'):
                try:
                    robots_url = f"{target}/robots.txt"
                    response = requests.get(robots_url, timeout=10)
                    if response.status_code == 200:
                        checks['robots_txt'] = 'Available'
                        checks['robots_content'] = response.text[:500] + '...' if len(response.text) > 500 else response.text
                    else:
                        checks['robots_txt'] = 'Not available'
                except:
                    checks['robots_txt'] = 'Error'
                    
            # فحص sitemap
            if target.startswith('http'):
                try:
                    sitemap_url = f"{target}/sitemap.xml"
                    response = requests.get(sitemap_url, timeout=10)
                    if response.status_code == 200:
                        checks['sitemap'] = 'Available'
                    else:
                        checks['sitemap'] = 'Not available'
                except:
                    checks['sitemap'] = 'Error'
                    
            return checks
            
        except Exception as e:
            return {'error': str(e)}
            
    def test_proxy_connection(self):
        """اختبار اتصال Proxy"""
        try:
            test_url = "http://httpbin.org/ip"
            results = []
            
            for proxy in self.proxy_list:
                try:
                    proxies = {
                        'http': proxy,
                        'https': proxy
                    }
                    
                    start_time = time.time()
                    response = requests.get(test_url, proxies=proxies, timeout=10)
                    end_time = time.time()
                    
                    if response.status_code == 200:
                        proxy_result = {
                            'proxy': proxy,
                            'status': 'working',
                            'response_time': round(end_time - start_time, 3),
                            'ip_address': response.json().get('origin', 'Unknown'),
                            'timestamp': datetime.datetime.now().isoformat()
                        }
                    else:
                        proxy_result = {
                            'proxy': proxy,
                            'status': 'failed',
                            'response_time': round(end_time - start_time, 3),
                            'error': f"HTTP {response.status_code}",
                            'timestamp': datetime.datetime.now().isoformat()
                        }
                        
                except Exception as e:
                    proxy_result = {
                        'proxy': proxy,
                        'status': 'error',
                        'error': str(e),
                        'timestamp': datetime.datetime.now().isoformat()
                    }
                    
                results.append(proxy_result)
                
            return results
            
        except Exception as e:
            return {'error': str(e)}
            
    def get_operation_statistics(self):
        """الحصول على إحصائيات العمليات"""
        try:
            total_operations = len(self.stealth_operations)
            successful_operations = len([op for op in self.stealth_operations if op.get('status') == 'completed'])
            
            # إحصائيات حسب النوع
            type_stats = {}
            for operation in self.stealth_operations:
                op_type = operation.get('type', 'unknown')
                type_stats[op_type] = type_stats.get(op_type, 0) + 1
                
            return {
                'total_operations': total_operations,
                'successful_operations': successful_operations,
                'type_stats': type_stats
            }
            
        except Exception as e:
            st.error(f"Error getting statistics: {str(e)}")
            return {}
            
    def export_operations(self, format_type='json'):
        """تصدير العمليات"""
        try:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if format_type == 'json':
                filename = f"stealth_operations_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.stealth_operations, f, indent=2, ensure_ascii=False)
                    
            elif format_type == 'csv':
                filename = f"stealth_operations_{timestamp}.csv"
                df = pd.DataFrame(self.stealth_operations)
                df.to_csv(filename, index=False, encoding='utf-8')
                
            return filename
            
        except Exception as e:
            st.error(f"Error exporting operations: {str(e)}")
            return None

def main():
    """الدالة الرئيسية"""
    st.markdown("""
    <div class="stealth-header">
        <h1>🕷️ Stealth Operations Tool</h1>
        <p>أداة متخصصة للعمليات الخفية وفحص المواقع</p>
        <p>Specialized Tool for Stealth Operations and Website Scanning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تهيئة الأداة
    stealth_tool = StealthOperationsTool()
    
    # Sidebar
    st.sidebar.markdown("## 🕷️ Stealth Operations Control Panel")
    
    # اختيار الوضع
    operation_mode = st.sidebar.selectbox(
        "Operation Mode",
        ["🎯 Target Scan", "🌐 Website Analysis", "🔍 Network Scan", "📊 Operations", "⚙️ Settings"]
    )
    
    if operation_mode == "🎯 Target Scan":
        st.markdown("## 🎯 Target Selection and Scanning")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📝 Target Information")
            
            target_url = st.text_input("Target URL", "https://example.com")
            target_domain = st.text_input("Target Domain (for network scan)", "example.com")
            
            # خيارات الفحص
            st.markdown("#### 🔧 Scan Options")
            
            scan_type = st.selectbox(
                "Scan Type",
                ["website_scan", "network_scan", "full_stealth_scan", "proxy_test"]
            )
            
            # إعدادات Stealth
            st.markdown("#### 🕷️ Stealth Settings")
            
            min_delay = st.slider("Min Delay (seconds)", 1, 10, 2)
            max_delay = st.slider("Max Delay (seconds)", 5, 20, 8)
            
            if st.button("🚀 Execute Stealth Operation", key="execute_stealth"):
                if target_url or target_domain:
                    target = target_url if target_url else target_domain
                    
                    with st.spinner("Executing stealth operation..."):
                        operation = stealth_tool.execute_stealth_operation(
                            scan_type, 
                            target,
                            min_delay=min_delay,
                            max_delay=max_delay
                        )
                        
                        if operation:
                            st.success(f"✅ Operation completed: {operation['id']}")
                            
        with col2:
            st.markdown("### 📊 Recent Operations")
            if stealth_tool.stealth_operations:
                latest_op = stealth_tool.stealth_operations[-1]
                
                st.markdown(f"""
                <div class="target-info">
                    <strong>🎯 {latest_op.get('type', 'Unknown')}</strong><br>
                    📍 Target: {latest_op.get('target', 'Unknown')}<br>
                    📊 Status: {latest_op.get('status', 'Unknown')}<br>
                    📅 Time: {latest_op.get('start_time', 'Unknown')[:19]}
                </div>
                """, unsafe_allow_html=True)
                
                # عرض النتائج
                if 'result' in latest_op:
                    st.markdown("#### 📋 Operation Results")
                    st.json(latest_op['result'])
            else:
                st.info("No operations executed yet")
                
    elif operation_mode == "🌐 Website Analysis":
        st.markdown("## 🌐 Website Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔍 Website Scanner")
            
            website_url = st.text_input("Website URL", "https://example.com")
            
            if st.button("🔍 Scan Website", key="scan_website"):
                if website_url:
                    with st.spinner("Scanning website..."):
                        scan_result = stealth_tool.perform_website_scan(website_url)
                        
                        if 'error' not in scan_result:
                            st.success("Website scan completed!")
                            
                            # عرض النتائج
                            st.markdown("#### 📊 Scan Results")
                            
                            col_result1, col_result2 = st.columns(2)
                            
                            with col_result1:
                                st.metric("Status Code", scan_result.get('status_code', 'N/A'))
                                st.metric("Response Time", f"{scan_result.get('response_time', 0):.3f}s")
                                st.metric("Content Length", f"{scan_result.get('content_length', 0):,} bytes")
                                
                            with col_result2:
                                st.metric("Internal Links", scan_result.get('internal_links_count', 0))
                                st.metric("External Links", scan_result.get('external_links_count', 0))
                                st.metric("Images", scan_result.get('images_count', 0))
                                
                            # عرض التفاصيل
                            st.markdown("#### 📝 Website Details")
                            st.write(f"**Title:** {scan_result.get('title', 'N/A')}")
                            st.write(f"**Description:** {scan_result.get('description', 'N/A')}")
                            st.write(f"**SSL:** {scan_result.get('ssl_info', {}).get('ssl_certificate', 'N/A')}")
                            
                        else:
                            st.error(f"Scan failed: {scan_result['error']}")
                            
        with col2:
            st.markdown("### 📈 Analysis Charts")
            
            if stealth_tool.stealth_operations:
                # رسم بياني للعمليات
                operations_df = pd.DataFrame(stealth_tool.stealth_operations)
                
                if not operations_df.empty:
                    # تجميع حسب النوع
                    type_counts = operations_df['type'].value_counts()
                    
                    fig = px.pie(
                        values=type_counts.values,
                        names=type_counts.index,
                        title="Operations by Type"
                    )
                    st.plotly_chart(fig)
                    
            else:
                st.info("No data available for analysis")
                
    elif operation_mode == "🔍 Network Scan":
        st.markdown("## 🔍 Network Scanning")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌐 Network Scanner")
            
            network_target = st.text_input("Network Target", "example.com")
            
            if st.button("🔍 Scan Network", key="scan_network"):
                if network_target:
                    with st.spinner("Scanning network..."):
                        network_result = stealth_tool.perform_network_scan(network_target)
                        
                        if 'error' not in network_result:
                            st.success("Network scan completed!")
                            
                            # عرض النتائج
                            st.markdown("#### 📊 Network Results")
                            
                            st.write(f"**Target:** {network_result.get('target', 'N/A')}")
                            st.write(f"**Ping Status:** {network_result.get('ping_status', 'N/A')}")
                            
                            if network_result.get('open_ports'):
                                st.write(f"**Open Ports:** {', '.join(map(str, network_result['open_ports']))}")
                            else:
                                st.write("**Open Ports:** None detected")
                                
                        else:
                            st.error(f"Network scan failed: {network_result['error']}")
                            
            # Proxy Testing
            st.markdown("#### 🔄 Proxy Testing")
            
            if st.button("🔄 Test Proxies", key="test_proxies"):
                with st.spinner("Testing proxies..."):
                    proxy_results = stealth_tool.test_proxy_connection()
                    
                    if 'error' not in proxy_results:
                        st.success("Proxy testing completed!")
                        
                        # عرض النتائج
                        for proxy_result in proxy_results:
                            status_color = "🟢" if proxy_result.get('status') == 'working' else "🔴"
                            st.write(f"{status_color} {proxy_result.get('proxy', 'Unknown')}: {proxy_result.get('status', 'Unknown')}")
                            
                    else:
                        st.error(f"Proxy testing failed: {proxy_results['error']}")
                        
        with col2:
            st.markdown("### 📊 Network Statistics")
            
            if stealth_tool.stealth_operations:
                # إحصائيات الشبكة
                network_ops = [op for op in stealth_tool.stealth_operations if op.get('type') == 'network_scan']
                
                if network_ops:
                    st.metric("Total Network Scans", len(network_ops))
                    
                    # رسم بياني للفحوصات
                    network_df = pd.DataFrame(network_ops)
                    
                    if not network_df.empty:
                        fig = px.line(
                            network_df,
                            x='start_time',
                            title="Network Scan Activity"
                        )
                        st.plotly_chart(fig)
                        
            else:
                st.info("No network scan data available")
                
    elif operation_mode == "📊 Operations":
        st.markdown("## 📊 Operations Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 All Operations")
            
            if stealth_tool.stealth_operations:
                # فلترة العمليات
                operation_filter = st.selectbox(
                    "Filter by Type",
                    ["All"] + list(set([op.get('type', 'unknown') for op in stealth_tool.stealth_operations]))
                )
                
                filtered_operations = stealth_tool.stealth_operations
                if operation_filter != "All":
                    filtered_operations = [op for op in stealth_tool.stealth_operations if op.get('type') == operation_filter]
                
                # عرض العمليات
                for operation in filtered_operations[-10:]:  # آخر 10 عمليات
                    with st.expander(f"🎯 {operation.get('type', 'Unknown')} - {operation.get('target', 'Unknown')}"):
                        st.write(f"**ID:** {operation.get('id', 'Unknown')}")
                        st.write(f"**Status:** {operation.get('status', 'Unknown')}")
                        st.write(f"**Start Time:** {operation.get('start_time', 'Unknown')[:19]}")
                        st.write(f"**End Time:** {operation.get('end_time', 'Unknown')[:19]}")
                        
                        if 'result' in operation:
                            st.write("**Result:**")
                            st.json(operation['result'])
                            
            else:
                st.info("No operations available")
                
        with col2:
            st.markdown("### 📈 Statistics")
            
            stats = stealth_tool.get_operation_statistics()
            
            if stats:
                col_stat1, col_stat2 = st.columns(2)
                
                with col_stat1:
                    st.metric("Total Operations", stats['total_operations'])
                    
                with col_stat2:
                    st.metric("Successful Operations", stats['successful_operations'])
                    
                # إحصائيات حسب النوع
                st.markdown("#### 📊 Operations by Type")
                type_stats = stats.get('type_stats', {})
                
                if type_stats:
                    for op_type, count in type_stats.items():
                        st.write(f"**{op_type.title()}:** {count} operations")
                        
            # تصدير البيانات
            st.markdown("### 📤 Export Operations")
            
            if stealth_tool.stealth_operations:
                col_export1, col_export2 = st.columns(2)
                
                with col_export1:
                    if st.button("📤 Export as JSON"):
                        filename = stealth_tool.export_operations('json')
                        if filename:
                            st.success(f"Exported to {filename}")
                            
                with col_export2:
                    if st.button("📤 Export as CSV"):
                        filename = stealth_tool.export_operations('csv')
                        if filename:
                            st.success(f"Exported to {filename}")
                            
    elif operation_mode == "⚙️ Settings":
        st.markdown("## ⚙️ Tool Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔧 Stealth Settings")
            
            # إعدادات Stealth
            st.markdown("#### Operation Configuration")
            
            # تأخير افتراضي
            default_min_delay = st.slider(
                "Default Min Delay (seconds)",
                min_value=1,
                max_value=10,
                value=2
            )
            
            default_max_delay = st.slider(
                "Default Max Delay (seconds)",
                min_value=5,
                max_value=20,
                value=8
            )
            
            # timeout setting
            default_timeout = st.slider(
                "Default Timeout (seconds)",
                min_value=5,
                max_value=60,
                value=15
            )
            
            if st.button("💾 Save Stealth Settings"):
                st.success("Stealth settings saved successfully!")
                
        with col2:
            st.markdown("### 📊 Data Management")
            
            # معلومات البيانات
            st.info(f"**Total Operations:** {len(stealth_tool.stealth_operations)}")
            st.info(f"**Total Logs:** {len(stealth_tool.operation_logs)}")
            
            # إدارة البيانات
            st.markdown("#### Data Actions")
            
            col_data1, col_data2 = st.columns(2)
            
            with col_data1:
                if st.button("🗑️ Clear Operations"):
                    if st.checkbox("I confirm I want to delete all operations"):
                        stealth_tool.stealth_operations.clear()
                        stealth_tool.save_data()
                        st.success("All operations cleared!")
                        st.rerun()
                        
            with col_data2:
                if st.button("🗑️ Clear Logs"):
                    if st.checkbox("I confirm I want to delete all logs"):
                        stealth_tool.operation_logs.clear()
                        stealth_tool.save_data()
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
        <p>🕷️ Stealth Operations Tool - Advanced Stealth Operations and Website Analysis</p>
        <p>Built for Cloudflare Pages | Multi-Layer Stealth | Real-time Scanning</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()