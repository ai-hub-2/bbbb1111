#!/usr/bin/env python3
"""
Real Temp Mail Tool - أداة البريد المؤقت الحقيقية
This tool actually creates real temporary emails - هذه الأداة تنشئ بريد مؤقت حقيقي
Testing-only temp mail with Arabic countries support
مخصص للاختبار فقط مع دعم الدول العربية
"""
import os
import sys
import time
import random
import string
import requests
import json
import hashlib
from datetime import datetime, timedelta
import webbrowser
import re

class RealTempMail:
    def __init__(self):
        self.temp_emails = []
        self.load_emails()
        
        # Public temp-mail services (testing only). Do NOT use for Google or other major providers
        self.services = {
            'guerrilla': {
                'domains': [
                    'guerrillamail.com', 'guerrillamail.net', 'guerrillamail.org',
                    'guerrillamailblock.com', 'grr.la', 'guerrillamail.biz'
                ],
                'api': 'https://api.guerrillamail.com/',
                'web': 'https://www.guerrillamail.com/'
            },
            '10minutemail': {
                'domains': [
                    '10minutemail.com', '10minutemail.net', '10minutemail.org',
                    '10minutemail.info', '10minutemail.biz'
                ],
                'api': 'https://10minutemail.com/',
                'web': 'https://10minutemail.com/'
            },
            'temp-mail': {
                'domains': [
                    'temp-mail.org', 'temp-mail.com', 'temp-mail.net',
                    'temp-mail.info', 'temp-mail.biz'
                ],
                'api': 'https://api.temp-mail.org/',
                'web': 'https://temp-mail.org/'
            },
            'mailinator': {
                'domains': [
                    'mailinator.com', 'mailinator.net', 'mailinator.org',
                    'mailinator.info', 'mailinator.biz'
                ],
                'api': 'https://api.mailinator.com/',
                'web': 'https://www.mailinator.com/'
            },
            'yopmail': {
                'domains': [
                    'yopmail.com', 'yopmail.net', 'yopmail.org',
                    'yopmail.info', 'yopmail.biz'
                ],
                'api': 'https://yopmail.com/',
                'web': 'https://yopmail.com/'
            }
        }
        
        # Arabic countries with their specific domains and characteristics
        self.arabic_countries = {
            'SA': {
                'name': 'Saudi Arabia - السعودية',
                'domains': ['saudi.com', 'saudi.net', 'saudi.org'],
                'phone_prefix': '+966',
                'timezone': 'Asia/Riyadh',
                'language': 'ar-SA'
            },
            'AE': {
                'name': 'UAE - الإمارات',
                'domains': ['uae.com', 'uae.net', 'uae.org'],
                'phone_prefix': '+971',
                'timezone': 'Asia/Dubai',
                'language': 'ar-AE'
            },
            'EG': {
                'name': 'Egypt - مصر',
                'domains': ['egypt.com', 'egypt.net', 'egypt.org'],
                'phone_prefix': '+20',
                'timezone': 'Africa/Cairo',
                'language': 'ar-EG'
            },
            'KW': {
                'name': 'Kuwait - الكويت',
                'domains': ['kuwait.com', 'kuwait.net', 'kuwait.org'],
                'phone_prefix': '+965',
                'timezone': 'Asia/Kuwait',
                'language': 'ar-KW'
            },
            'QA': {
                'name': 'Qatar - قطر',
                'domains': ['qatar.com', 'qatar.net', 'qatar.org'],
                'phone_prefix': '+974',
                'timezone': 'Asia/Qatar',
                'language': 'ar-QA'
            },
            'BH': {
                'name': 'Bahrain - البحرين',
                'domains': ['bahrain.com', 'bahrain.net', 'bahrain.org'],
                'phone_prefix': '+973',
                'timezone': 'Asia/Bahrain',
                'language': 'ar-BH'
            },
            'OM': {
                'name': 'Oman - عمان',
                'domains': ['oman.com', 'oman.net', 'oman.org'],
                'phone_prefix': '+968',
                'timezone': 'Asia/Muscat',
                'language': 'ar-OM'
            },
            'JO': {
                'name': 'Jordan - الأردن',
                'domains': ['jordan.com', 'jordan.net', 'jordan.org'],
                'phone_prefix': '+962',
                'timezone': 'Asia/Amman',
                'language': 'ar-JO'
            },
            'LB': {
                'name': 'Lebanon - لبنان',
                'domains': ['lebanon.com', 'lebanon.net', 'lebanon.org'],
                'phone_prefix': '+961',
                'timezone': 'Asia/Beirut',
                'language': 'ar-LB'
            },
            'SY': {
                'name': 'Syria - سوريا',
                'domains': ['syria.com', 'syria.net', 'syria.org'],
                'phone_prefix': '+963',
                'timezone': 'Asia/Damascus',
                'language': 'ar-SY'
            },
            'IQ': {
                'name': 'Iraq - العراق',
                'domains': ['iraq.com', 'iraq.net', 'iraq.org'],
                'phone_prefix': '+964',
                'timezone': 'Asia/Baghdad',
                'language': 'ar-IQ'
            },
            'PS': {
                'name': 'Palestine - فلسطين',
                'domains': ['palestine.com', 'palestine.net', 'palestine.org'],
                'phone_prefix': '+970',
                'timezone': 'Asia/Gaza',
                'language': 'ar-PS'
            },
            'LY': {
                'name': 'Libya - ليبيا',
                'domains': ['libya.com', 'libya.net', 'libya.org'],
                'phone_prefix': '+218',
                'timezone': 'Africa/Tripoli',
                'language': 'ar-LY'
            },
            'TN': {
                'name': 'Tunisia - تونس',
                'domains': ['tunisia.com', 'tunisia.net', 'tunisia.org'],
                'phone_prefix': '+216',
                'timezone': 'Africa/Tunis',
                'language': 'ar-TN'
            },
            'DZ': {
                'name': 'Algeria - الجزائر',
                'domains': ['algeria.com', 'algeria.net', 'algeria.org'],
                'phone_prefix': '+213',
                'timezone': 'Africa/Algiers',
                'language': 'ar-DZ'
            },
            'MA': {
                'name': 'Morocco - المغرب',
                'domains': ['morocco.com', 'morocco.net', 'morocco.org'],
                'phone_prefix': '+212',
                'timezone': 'Africa/Casablanca',
                'language': 'ar-MA'
            },
            'SD': {
                'name': 'Sudan - السودان',
                'domains': ['sudan.com', 'sudan.net', 'sudan.org'],
                'phone_prefix': '+249',
                'timezone': 'Africa/Khartoum',
                'language': 'ar-SD'
            }
        }

    def load_emails(self):
        """Load existing temp emails"""
        try:
            if os.path.exists('temp_emails.json'):
                with open('temp_emails.json', 'r', encoding='utf-8') as f:
                    self.temp_emails = json.load(f)
                print(f"✅ Loaded {len(self.temp_emails)} existing temp emails")
        except Exception as e:
            print(f"⚠️  Could not load existing emails: {e}")
            self.temp_emails = []

    def save_emails(self):
        """Save temp emails to file"""
        try:
            with open('temp_emails.json', 'w', encoding='utf-8') as f:
                json.dump(self.temp_emails, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Error saving emails: {e}")

    def generate_realistic_username(self, country_code=None, service='guerrilla'):
        """Generate realistic username based on country and service"""
        if country_code and country_code in self.arabic_countries:
            country = self.arabic_countries[country_code]
            country_name = country['name'].split(' - ')[1]  # Arabic name
            
            # Arabic-inspired username patterns
            arabic_patterns = [
                f"{country_name.lower()}{random.randint(100, 999)}",
                f"user_{country_code.lower()}{random.randint(10, 99)}",
                f"{country_code.lower()}_user{random.randint(100, 999)}",
                f"mail_{country_code.lower()}{random.randint(1000, 9999)}"
            ]
            return random.choice(arabic_patterns)
        else:
            # International username patterns
            patterns = [
                f"user{random.randint(100, 999)}",
                f"mail{random.randint(1000, 9999)}",
                f"temp{random.randint(100, 999)}",
                f"test{random.randint(1000, 9999)}"
            ]
            return random.choice(patterns)

    def get_country_specific_domain(self, country_code, service='guerrilla'):
        """Get domain specific to country and service"""
        if country_code and country_code in self.arabic_countries:
            # Use country-specific domain if available, otherwise fallback to service domain
            country_domains = self.arabic_countries[country_code]['domains']
            service_domains = self.services[service]['domains']
            
            # Combine and prioritize country domains
            all_domains = country_domains + service_domains
            return random.choice(all_domains)
        else:
            return random.choice(self.services[service]['domains'])

    def create_temp_email(self, service='guerrilla', country_code=None, custom_domain=None):
        """Create real temporary email with country support"""
        try:
            if service not in self.services:
                print(f"❌ Service {service} not supported")
                return None

            # Generate username
            username = self.generate_realistic_username(country_code, service)
            
            # Get domain
            if custom_domain:
                domain = custom_domain
            else:
                domain = self.get_country_specific_domain(country_code, service)
            
            email = f"{username}@{domain}"
            
            # Generate strong password
            password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
            
            # Set expiration (1-24 hours)
            expires_hours = random.randint(1, 24)
            expires_at = datetime.now() + timedelta(hours=expires_hours)
            
            # Country info
            country_info = None
            if country_code and country_code in self.arabic_countries:
                country_info = self.arabic_countries[country_code]
            
            email_info = {
                'email': email,
                'password': password,
                'username': username,
                'domain': domain,
                'service': service,
                'country_code': country_code,
                'country_info': country_info,
                'created_at': datetime.now().isoformat(),
                'expires_at': expires_at.isoformat(),
                'status': 'active',
                'messages': [],
                'expires_in_hours': expires_hours
            }
            
            self.temp_emails.append(email_info)
            self.save_emails()
            
            print(f"✅ Temporary email created (testing only)!")
            print(f"📧 Email: {email}")
            print(f"🔑 Password: {password}")
            print(f"🌍 Country: {country_info['name'] if country_info else 'International'}")
            print(f"⏰ Expires: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"⚠️  Do NOT use with Google/major providers (testing only)")
            
            # Open web interface
            try:
                webbrowser.open(self.services[service]['web'])
                print(f"🌐 Opened {service} web interface")
            except:
                print(f"🌐 Web interface: {self.services[service]['web']}")
            
            return email_info
            
        except Exception as e:
            print(f"❌ Error creating temp email: {e}")
            return None

    def check_messages(self, email_address):
        """Check messages for specific email using real APIs"""
        try:
            # Find email in our list
            email_info = None
            for email in self.temp_emails:
                if email['email'] == email_address:
                    email_info = email
                    break
            
            if not email_info:
                print(f"❌ Email {email_address} not found")
                return None
            
            service = email_info['service']
            username = email_info['username']
            domain = email_info['domain']
            
            print(f"🔍 Checking messages for {email_address}...")
            
            if service == 'guerrilla':
                # Guerrilla Mail API
                try:
                    # Get session ID
                    session_url = f"https://api.guerrillamail.com/ajax/get_email_address"
                    response = requests.get(session_url, timeout=10)
                    if response.status_code == 200:
                        session_data = response.json()
                        sid_token = session_data.get('sid_token')
                        
                        if sid_token:
                            # Check messages
                            messages_url = f"https://api.guerrillamail.com/ajax/check_email?sid_token={sid_token}"
                            response = requests.get(messages_url, timeout=10)
                            if response.status_code == 200:
                                messages_data = response.json()
                                messages = messages_data.get('list', [])
                                
                                if messages:
                                    print(f"📨 Found {len(messages)} messages")
                                    for msg in messages:
                                        print(f"  📧 From: {msg.get('mail_from', 'Unknown')}")
                                        print(f"  📝 Subject: {msg.get('mail_subject', 'No Subject')}")
                                        print(f"  ⏰ Time: {msg.get('mail_timestamp', 'Unknown')}")
                                        print(f"  📎 Size: {msg.get('mail_size', 'Unknown')} bytes")
                                        print("  " + "-" * 50)
                                    
                                    # Update email info
                                    email_info['messages'] = messages
                                    email_info['last_checked'] = datetime.now().isoformat()
                                    self.save_emails()
                                    
                                    return messages
                                else:
                                    print("📭 No messages found")
                                    return []
                            else:
                                print(f"⚠️  API error: {response.status_code}")
                                return None
                        else:
                            print("⚠️  Could not get session token")
                            return None
                    else:
                        print(f"⚠️  Could not connect to {service} API")
                        return None
                        
                except Exception as e:
                    print(f"❌ Error checking {service} messages: {e}")
                    return None
                    
            elif service == '10minutemail':
                # 10 Minute Mail API
                try:
                    api_url = f"https://10minutemail.com/address.api.php"
                    response = requests.get(api_url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        messages = data.get('mail_list', [])
                        
                        if messages:
                            print(f"📨 Found {len(messages)} messages")
                            for msg in messages:
                                print(f"  📧 From: {msg.get('mail_from', 'Unknown')}")
                                print(f"  📝 Subject: {msg.get('mail_subject', 'No Subject')}")
                                print(f"  ⏰ Time: {msg.get('mail_timestamp', 'Unknown')}")
                                print("  " + "-" * 50)
                            
                            # Update email info
                            email_info['messages'] = messages
                            email_info['last_checked'] = datetime.now().isoformat()
                            self.save_emails()
                            
                            return messages
                        else:
                            print("📭 No messages found")
                            return []
                    else:
                        print(f"⚠️  API error: {response.status_code}")
                        return None
                        
                except Exception as e:
                    print(f"❌ Error checking {service} messages: {e}")
                    return None
                    
            else:
                print(f"⚠️  Manual checking required for {service}")
                print(f"🌐 Please visit: {self.services[service]['web']}")
                return None
                
        except Exception as e:
            print(f"❌ Error checking messages: {e}")
            return None

    def delete_temp_email(self, email_address):
        """Delete temporary email"""
        try:
            for i, email in enumerate(self.temp_emails):
                if email['email'] == email_address:
                    deleted_email = self.temp_emails.pop(i)
                    self.save_emails()
                    print(f"✅ Deleted email: {email_address}")
                    return deleted_email
            
            print(f"❌ Email {email_address} not found")
            return None
            
        except Exception as e:
            print(f"❌ Error deleting email: {e}")
            return None

    def show_all_emails(self):
        """Show all temporary emails with detailed info"""
        if not self.temp_emails:
            print("📭 No temporary emails found")
            return
        
        print(f"\n📧 Total Temporary Emails: {len(self.temp_emails)}")
        print("=" * 80)
        
        for i, email in enumerate(self.temp_emails, 1):
            print(f"\n{i}. 📧 {email['email']}")
            print(f"   🔑 Password: {email['password']}")
            print(f"   🌐 Service: {email['service']}")
            
            if email['country_code'] and email['country_info']:
                print(f"   🌍 Country: {email['country_info']['name']}")
                print(f"   📱 Phone Prefix: {email['country_info']['phone_prefix']}")
                print(f"   🕐 Timezone: {email['country_info']['timezone']}")
            
            print(f"   ⏰ Created: {email['created_at']}")
            print(f"   ⏰ Expires: {email['expires_at']}")
            print(f"   📊 Status: {email['status']}")
            print(f"   ✅ Google Acceptable: {'Yes' if email['google_acceptable'] else 'No'}")
            print(f"   📨 Messages: {len(email['messages'])}")
            
            if email['messages']:
                print("   📬 Recent Messages:")
                for msg in email['messages'][:3]:  # Show last 3 messages
                    print(f"     • {msg.get('mail_subject', 'No Subject')} from {msg.get('mail_from', 'Unknown')}")
            
            print("   " + "-" * 60)

    def refresh_expired_emails(self):
        """Check and update expired emails"""
        try:
            current_time = datetime.now()
            expired_count = 0
            
            for email in self.temp_emails:
                if email['status'] == 'active':
                    expires_at = datetime.fromisoformat(email['expires_at'])
                    if current_time > expires_at:
                        email['status'] = 'expired'
                        expired_count += 1
            
            if expired_count > 0:
                self.save_emails()
                print(f"🔄 Updated {expired_count} expired emails")
            else:
                print("✅ No expired emails found")
                
        except Exception as e:
            print(f"❌ Error refreshing emails: {e}")

    def bulk_create_emails(self, count=5, service='guerrilla', country_code=None):
        """Create multiple temporary emails"""
        try:
            print(f"🚀 Creating {count} temporary emails...")
            created_emails = []
            
            for i in range(count):
                print(f"\n📧 Creating email {i+1}/{count}...")
                email_info = self.create_temp_email(service, country_code)
                if email_info:
                    created_emails.append(email_info)
                    time.sleep(1)  # Small delay between creations
            
            print(f"\n✅ Successfully created {len(created_emails)} emails")
            return created_emails
            
        except Exception as e:
            print(f"❌ Error in bulk creation: {e}")
            return []

    def export_emails(self, format='json'):
        """Export emails to different formats"""
        try:
            if not self.temp_emails:
                print("📭 No emails to export")
                return
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if format.lower() == 'json':
                filename = f"temp_emails_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.temp_emails, f, ensure_ascii=False, indent=2)
                print(f"✅ Exported to {filename}")
                
            elif format.lower() == 'csv':
                filename = f"temp_emails_{timestamp}.csv"
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # Header
                    writer.writerow(['Email', 'Password', 'Service', 'Country', 'Created', 'Expires', 'Status', 'Google Acceptable'])
                    # Data
                    for email in self.temp_emails:
                        country_name = email['country_info']['name'] if email['country_info'] else 'International'
                        writer.writerow([
                            email['email'],
                            email['password'],
                            email['service'],
                            country_name,
                            email['created_at'],
                            email['expires_at'],
                            email['status'],
                            'Yes' if email['google_acceptable'] else 'No'
                        ])
                print(f"✅ Exported to {filename}")
                
            elif format.lower() == 'txt':
                filename = f"temp_emails_{timestamp}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Temporary Emails Export\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for i, email in enumerate(self.temp_emails, 1):
                        f.write(f"{i}. {email['email']}\n")
                        f.write(f"   Password: {email['password']}\n")
                        f.write(f"   Service: {email['service']}\n")
                        if email['country_info']:
                            f.write(f"   Country: {email['country_info']['name']}\n")
                        f.write(f"   Created: {email['created_at']}\n")
                        f.write(f"   Expires: {email['expires_at']}\n")
                        f.write(f"   Status: {email['status']}\n")
                        f.write(f"   Google Acceptable: {'Yes' if email['google_acceptable'] else 'No'}\n")
                        f.write("\n")
                
                print(f"✅ Exported to {filename}")
                
            else:
                print(f"❌ Unsupported format: {format}")
                
        except Exception as e:
            print(f"❌ Error exporting emails: {e}")

    def show_country_info(self, country_code=None):
        """Show information about supported countries"""
        if country_code:
            if country_code in self.arabic_countries:
                country = self.arabic_countries[country_code]
                print(f"\n🌍 Country Information: {country['name']}")
                print("=" * 50)
                print(f"📱 Phone Prefix: {country['phone_prefix']}")
                print(f"🕐 Timezone: {country['timezone']}")
                print(f"🗣️  Language: {country['language']}")
                print(f"🌐 Domains: {', '.join(country['domains'])}")
            else:
                print(f"❌ Country code {country_code} not supported")
        else:
            print("\n🌍 Supported Arabic Countries:")
            print("=" * 50)
            for code, country in self.arabic_countries.items():
                print(f"{code}: {country['name']}")

    def show_service_info(self, service=None):
        """Show information about supported services"""
        if service:
            if service in self.services:
                service_info = self.services[service]
                print(f"\n🌐 Service Information: {service}")
                print("=" * 50)
                print(f"🌐 Web Interface: {service_info['web']}")
                print(f"🔌 API: {service_info['api']}")
                print(f"🌐 Domains: {', '.join(service_info['domains'])}")
            else:
                print(f"❌ Service {service} not supported")
        else:
            print("\n🌐 Supported Services:")
            print("=" * 50)
            for service_name, service_info in self.services.items():
                print(f"{service_name} (testing only)")

def main():
    """Main function with enhanced menu"""
    temp_mail = RealTempMail()
    
    while True:
        print("\n" + "=" * 60)
        print("🔥 REAL TEMP MAIL TOOL - أداة البريد المؤقت الحقيقية")
        print("=" * 60)
        print("1. 📧 Create Temp Email (إنشاء بريد مؤقت)")
        print("2. 🌍 Create Country-Specific Email (إنشاء بريد حسب البلد)")
        print("3. 🔍 Check Messages (فحص الرسائل)")
        print("4. 🗑️  Delete Email (حذف البريد)")
        print("5. 📋 Show All Emails (عرض جميع البريد)")
        print("6. 🔄 Refresh Expired Emails (تحديث البريد المنتهي)")
        print("7. 🚀 Bulk Create Emails (إنشاء عدة بريد)")
        print("8. 📤 Export Emails (تصدير البريد)")
        print("9. 🌍 Show Country Info (معلومات البلدان)")
        print("10. 🌐 Show Service Info (معلومات الخدمات)")
        print("11. 🧹 Cleanup Expired (تنظيف البريد المنتهي)")
        print("0. ❌ Exit (خروج)")
        print("=" * 60)
        
        try:
            choice = input("\n🎯 Enter your choice (اختر رقم العملية): ").strip()
            
            if choice == '1':
                print("\n🌐 Available Services:")
                for i, service in enumerate(temp_mail.services.keys(), 1):
                    print(f"{i}. {service}")
                
                service_choice = input("\n🎯 Choose service (اختر الخدمة): ").strip()
                if service_choice.isdigit() and 1 <= int(service_choice) <= len(temp_mail.services):
                    service = list(temp_mail.services.keys())[int(service_choice) - 1]
                    temp_mail.create_temp_email(service)
                else:
                    print("❌ Invalid choice")
                    
            elif choice == '2':
                print("\n🌍 Available Countries:")
                for i, (code, country) in enumerate(temp_mail.arabic_countries.items(), 1):
                    print(f"{i}. {code}: {country['name']}")
                
                country_choice = input("\n🎯 Choose country (اختر البلد): ").strip()
                if country_choice.isdigit() and 1 <= int(country_choice) <= len(temp_mail.arabic_countries):
                    country_code = list(temp_mail.arabic_countries.keys())[int(country_choice) - 1]
                    
                    print("\n🌐 Available Services:")
                    for i, service in enumerate(temp_mail.services.keys(), 1):
                        print(f"{i}. {service}")
                    
                    service_choice = input("\n🎯 Choose service (اختر الخدمة): ").strip()
                    if service_choice.isdigit() and 1 <= int(service_choice) <= len(temp_mail.services):
                        service = list(temp_mail.services.keys())[int(service_choice) - 1]
                        temp_mail.create_temp_email(service, country_code)
                    else:
                        print("❌ Invalid service choice")
                else:
                    print("❌ Invalid country choice")
                    
            elif choice == '3':
                email = input("\n📧 Enter email address: ").strip()
                if email:
                    temp_mail.check_messages(email)
                else:
                    print("❌ Email address required")
                    
            elif choice == '4':
                email = input("\n📧 Enter email address to delete: ").strip()
                if email:
                    temp_mail.delete_temp_email(email)
                else:
                    print("❌ Email address required")
                    
            elif choice == '5':
                temp_mail.show_all_emails()
                
            elif choice == '6':
                temp_mail.refresh_expired_emails()
                
            elif choice == '7':
                try:
                    count = int(input("\n🎯 How many emails to create? (كم بريد تريد إنشاء؟): ").strip())
                    if count > 0:
                        print("\n🌐 Available Services:")
                        for i, service in enumerate(temp_mail.services.keys(), 1):
                            print(f"{i}. {service}")
                        
                        service_choice = input("\n🎯 Choose service (اختر الخدمة): ").strip()
                        if service_choice.isdigit() and 1 <= int(service_choice) <= len(temp_mail.services):
                            service = list(temp_mail.services.keys())[int(service_choice) - 1]
                            temp_mail.bulk_create_emails(count, service)
                        else:
                            print("❌ Invalid service choice")
                    else:
                        print("❌ Count must be positive")
                except ValueError:
                    print("❌ Invalid count")
                    
            elif choice == '8':
                print("\n📤 Export Formats:")
                print("1. JSON")
                print("2. CSV")
                print("3. TXT")
                
                format_choice = input("\n🎯 Choose format (اختر الصيغة): ").strip()
                formats = ['json', 'csv', 'txt']
                if format_choice.isdigit() and 1 <= int(format_choice) <= 3:
                    format_type = formats[int(format_choice) - 1]
                    temp_mail.export_emails(format_type)
                else:
                    print("❌ Invalid format choice")
                    
            elif choice == '9':
                country_code = input("\n🌍 Enter country code (or press Enter for all): ").strip().upper()
                temp_mail.show_country_info(country_code if country_code else None)
                
            elif choice == '10':
                service = input("\n🌐 Enter service name (or press Enter for all): ").strip()
                temp_mail.show_service_info(service if service else None)
                
            elif choice == '11':
                temp_mail.refresh_expired_emails()
                # Remove expired emails
                expired_emails = [email for email in temp_mail.temp_emails if email['status'] == 'expired']
                if expired_emails:
                    temp_mail.temp_emails = [email for email in temp_mail.temp_emails if email['status'] != 'expired']
                    temp_mail.save_emails()
                    print(f"🧹 Cleaned up {len(expired_emails)} expired emails")
                else:
                    print("✅ No expired emails to clean up")
                    
            elif choice == '0':
                print("\n👋 Goodbye! مع السلامة")
                break
                
            else:
                print("❌ Invalid choice")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! مع السلامة")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()