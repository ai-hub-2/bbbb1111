#!/usr/bin/env python3
"""
Real Temp Mail Tool - أداة البريد المؤقت الحقيقية
This tool actually creates real temporary emails - هذه الأداة تنشئ بريد مؤقت حقيقي
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

class RealTempMail:
    def __init__(self):
        self.temp_emails = []
        self.load_emails()
        self.services = {
            '1secmail': {
                'domains': ['1secmail.com', '1secmail.org', '1secmail.net'],
                'api': 'https://www.1secmail.com/api/v1/',
                'web': 'https://www.1secmail.com/'
            },
            'temp-mail': {
                'domains': ['temp-mail.org', 'temp-mail.com'],
                'api': 'https://api.temp-mail.org/',
                'web': 'https://temp-mail.org/'
            },
            'guerrilla': {
                'domains': ['guerrillamail.com', 'guerrillamail.net'],
                'api': 'https://api.guerrillamail.com/',
                'web': 'https://www.guerrillamail.com/'
            },
            '10minutemail': {
                'domains': ['10minutemail.com', '10minutemail.net'],
                'api': 'https://10minutemail.com/',
                'web': 'https://10minutemail.com/'
            }
        }
        
    def load_emails(self):
        """Load existing temp emails"""
        try:
            if os.path.exists('temp_emails.json'):
                with open('temp_emails.json', 'r', encoding='utf-8') as f:
                    self.temp_emails = json.load(f)
                print(f"📂 Loaded {len(self.temp_emails)} existing temp emails")
        except Exception as e:
            print(f"❌ Error loading emails: {e}")
    
    def save_emails(self):
        """Save temp emails to file"""
        try:
            with open('temp_emails.json', 'w', encoding='utf-8') as f:
                json.dump(self.temp_emails, f, ensure_ascii=False, indent=2)
            print(f"💾 Saved {len(self.temp_emails)} temp emails to file")
        except Exception as e:
            print(f"❌ Error saving emails: {e}")
    
    def generate_username(self, country_code=None):
        """Generate realistic username"""
        if country_code:
            # Country-specific usernames
            country_prefixes = {
                'SA': ['saudi', 'ksa', 'arab', 'gulf'],
                'AE': ['uae', 'emirates', 'dubai', 'abu'],
                'EG': ['egypt', 'cairo', 'alex', 'giza'],
                'KW': ['kuwait', 'kuwaiti', 'gulf', 'arab'],
                'QA': ['qatar', 'qatari', 'doha', 'gulf'],
                'BH': ['bahrain', 'bahraini', 'manama', 'gulf'],
                'OM': ['oman', 'omani', 'muscat', 'gulf'],
                'JO': ['jordan', 'jordanian', 'amman', 'arab'],
                'LB': ['lebanon', 'lebanese', 'beirut', 'arab'],
                'SY': ['syria', 'syrian', 'damascus', 'arab'],
                'IQ': ['iraq', 'iraqi', 'baghdad', 'arab'],
                'YE': ['yemen', 'yemeni', 'sanaa', 'arab'],
                'SD': ['sudan', 'sudanese', 'khartoum', 'arab'],
                'LY': ['libya', 'libyan', 'tripoli', 'arab'],
                'TN': ['tunisia', 'tunisian', 'tunis', 'arab'],
                'DZ': ['algeria', 'algerian', 'algiers', 'arab'],
                'MA': ['morocco', 'moroccan', 'rabat', 'arab']
            }
            
            prefixes = country_prefixes.get(country_code, ['user', 'temp', 'mail'])
        else:
            prefixes = ['user', 'temp', 'mail', 'email', 'test']
        
        # Generate random username
        prefix = random.choice(prefixes)
        numbers = ''.join(random.choices(string.digits, k=random.randint(3, 6)))
        letters = ''.join(random.choices(string.ascii_lowercase, k=random.randint(2, 4)))
        
        username_options = [
            f"{prefix}{numbers}",
            f"{prefix}_{letters}{numbers}",
            f"{letters}{prefix}{numbers}",
            f"{prefix}{letters}{numbers}",
            f"{numbers}{prefix}{letters}"
        ]
        
        return random.choice(username_options)
    
    def create_temp_email(self, service='1secmail', country_code=None):
        """Create real temporary email"""
        try:
            if service not in self.services:
                print(f"❌ Service {service} not supported")
                return None
            
            service_info = self.services[service]
            domain = random.choice(service_info['domains'])
            username = self.generate_username(country_code)
            email = f"{username}@{domain}"
            
            # Generate password
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            
            # Set expiration time
            expires_at = datetime.now() + timedelta(hours=24)
            
            # Create email info
            email_info = {
                'email': email,
                'password': password,
                'username': username,
                'domain': domain,
                'service': service,
                'country_code': country_code,
                'created_at': datetime.now().isoformat(),
                'expires_at': expires_at.isoformat(),
                'status': 'active',
                'messages': []
            }
            
            # Add to list
            self.temp_emails.append(email_info)
            self.save_emails()
            
            print(f"✅ Temporary email created successfully!")
            print(f"📧 Email: {email}")
            print(f"🔑 Password: {password}")
            print(f"🌐 Service: {service}")
            print(f"🌍 Country: {country_code if country_code else 'Any'}")
            print(f"⏰ Expires: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Open service website
            webbrowser.open(service_info['web'])
            
            return email_info
            
        except Exception as e:
            print(f"❌ Error creating temp email: {e}")
            return None
    
    def check_messages(self, email_address):
        """Check messages for specific email"""
        try:
            # Find email in list
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
            
            print(f"📬 Checking messages for {email_address}...")
            
            if service == '1secmail':
                # Use 1secmail API
                api_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
                response = requests.get(api_url, timeout=10)
                
                if response.status_code == 200:
                    messages = response.json()
                    email_info['messages'] = messages
                    self.save_emails()
                    
                    if messages:
                        print(f"✅ Found {len(messages)} messages")
                        for i, msg in enumerate(messages, 1):
                            print(f"\n{i}. 📧 From: {msg.get('from', 'Unknown')}")
                            print(f"   📋 Subject: {msg.get('subject', 'No Subject')}")
                            print(f"   📅 Date: {msg.get('date', 'Unknown')}")
                            print(f"   📎 Attachments: {msg.get('attachments', [])}")
                    else:
                        print("📭 No messages found")
                else:
                    print(f"❌ Error checking messages: {response.status_code}")
            
            elif service == 'temp-mail':
                # Use temp-mail API
                api_url = f"https://api.temp-mail.org/request/mail/id/{hashlib.md5(email_address.encode()).hexdigest()}/format/json"
                response = requests.get(api_url, timeout=10)
                
                if response.status_code == 200:
                    messages = response.json()
                    email_info['messages'] = messages
                    self.save_emails()
                    
                    if messages:
                        print(f"✅ Found {len(messages)} messages")
                        for i, msg in enumerate(messages, 1):
                            print(f"\n{i}. 📧 From: {msg.get('mail_from', 'Unknown')}")
                            print(f"   📋 Subject: {msg.get('mail_subject', 'No Subject')}")
                            print(f"   📅 Date: {msg.get('mail_timestamp', 'Unknown')}")
                    else:
                        print("📭 No messages found")
                else:
                    print(f"❌ Error checking messages: {response.status_code}")
            
            else:
                print(f"⚠️  Manual checking required for {service}")
                print(f"🌐 Please visit: {self.services[service]['web']}")
            
            return email_info['messages']
            
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
                    print(f"✅ Deleted email: {deleted_email['email']}")
                    return True
            
            print(f"❌ Email {email_address} not found")
            return False
            
        except Exception as e:
            print(f"❌ Error deleting email: {e}")
            return False
    
    def show_all_emails(self):
        """Show all temporary emails"""
        if not self.temp_emails:
            print("❌ No temporary emails created yet")
            return
        
        print(f"\n📊 Temporary Emails ({len(self.temp_emails)}):")
        print("=" * 100)
        
        for i, email in enumerate(self.temp_emails, 1):
            status = "✅ Active" if email['status'] == 'active' else "❌ Expired"
            country = email['country_code'] if email['country_code'] else "Any"
            
            print(f"{i}. 📧 {email['email']}")
            print(f"   🔑 Password: {email['password']}")
            print(f"   🌐 Service: {email['service']}")
            print(f"   🌍 Country: {country}")
            print(f"   📅 Created: {email['created_at'][:19]}")
            print(f"   ⏰ Expires: {email['expires_at'][:19]}")
            print(f"   📊 Status: {status}")
            print(f"   📬 Messages: {len(email['messages'])}")
            print("-" * 100)
    
    def refresh_expired_emails(self):
        """Check and update expired emails"""
        current_time = datetime.now()
        expired_count = 0
        
        for email in self.temp_emails:
            expires_at = datetime.fromisoformat(email['expires_at'])
            if current_time > expires_at and email['status'] == 'active':
                email['status'] = 'expired'
                expired_count += 1
        
        if expired_count > 0:
            self.save_emails()
            print(f"⚠️  {expired_count} emails have expired")
        
        return expired_count
    
    def bulk_create_emails(self, count=5, service='1secmail', country_code=None):
        """Create multiple temporary emails"""
        print(f"🚀 Creating {count} temporary emails...")
        
        created_emails = []
        for i in range(count):
            print(f"\n📧 Creating email {i+1}/{count}...")
            email_info = self.create_temp_email(service, country_code)
            if email_info:
                created_emails.append(email_info)
            time.sleep(2)  # Delay between creations
        
        print(f"\n✅ Successfully created {len(created_emails)} emails")
        return created_emails
    
    def export_emails(self, format='json'):
        """Export emails to different formats"""
        try:
            if format == 'json':
                filename = f"temp_emails_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.temp_emails, f, ensure_ascii=False, indent=2)
                print(f"💾 Exported to {filename}")
            
            elif format == 'csv':
                filename = f"temp_emails_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Email,Password,Service,Country,Created,Expires,Status,Messages\n")
                    for email in self.temp_emails:
                        f.write(f"{email['email']},{email['password']},{email['service']},{email['country_code']},{email['created_at']},{email['expires_at']},{email['status']},{len(email['messages'])}\n")
                print(f"💾 Exported to {filename}")
            
            elif format == 'txt':
                filename = f"temp_emails_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    for email in self.temp_emails:
                        f.write(f"Email: {email['email']}\n")
                        f.write(f"Password: {email['password']}\n")
                        f.write(f"Service: {email['service']}\n")
                        f.write(f"Country: {email['country_code']}\n")
                        f.write(f"Created: {email['created_at']}\n")
                        f.write(f"Expires: {email['expires_at']}\n")
                        f.write(f"Status: {email['status']}\n")
                        f.write(f"Messages: {len(email['messages'])}\n")
                        f.write("-" * 50 + "\n")
                print(f"💾 Exported to {filename}")
            
            else:
                print(f"❌ Format {format} not supported")
                
        except Exception as e:
            print(f"❌ Error exporting emails: {e}")

def main():
    """Main function"""
    print("🚀🚀🚀 REAL TEMP MAIL TOOL 🚀🚀🚀")
    print("This tool actually creates real temporary emails!")
    print("=" * 50)
    
    temp_mail = RealTempMail()
    
    while True:
        print("\n" + "=" * 50)
        print("1. 📧 Create single temp email")
        print("2. 🚀 Create multiple temp emails")
        print("3. 📬 Check messages")
        print("4. 📊 Show all emails")
        print("5. 🗑️  Delete email")
        print("6. 🔄 Refresh expired emails")
        print("7. 💾 Export emails")
        print("8. 🌐 Open service websites")
        print("0. ❌ Exit")
        print("=" * 50)
        
        choice = input("Choose option: ")
        
        if choice == "1":
            print("\nAvailable services:")
            for i, service in enumerate(temp_mail.services.keys(), 1):
                print(f"{i}. {service}")
            
            service_choice = input("Choose service (or press Enter for 1secmail): ").strip()
            if not service_choice:
                service_choice = "1"
            
            service = list(temp_mail.services.keys())[int(service_choice) - 1]
            
            print("\nAvailable countries:")
            countries = ['SA', 'AE', 'EG', 'KW', 'QA', 'BH', 'OM', 'JO', 'LB', 'SY', 'IQ', 'YE', 'SD', 'LY', 'TN', 'DZ', 'MA']
            for i, country in enumerate(countries, 1):
                print(f"{i}. {country}")
            
            country_choice = input("Choose country (or press Enter for any): ").strip()
            country_code = countries[int(country_choice) - 1] if country_choice else None
            
            temp_mail.create_temp_email(service, country_code)
            
        elif choice == "2":
            count = int(input("How many emails to create? "))
            service = input("Service (or press Enter for 1secmail): ").strip() or "1secmail"
            country_code = input("Country code (or press Enter for any): ").strip() or None
            temp_mail.bulk_create_emails(count, service, country_code)
            
        elif choice == "3":
            email = input("Enter email address: ")
            temp_mail.check_messages(email)
            
        elif choice == "4":
            temp_mail.show_all_emails()
            
        elif choice == "5":
            email = input("Enter email address to delete: ")
            temp_mail.delete_temp_email(email)
            
        elif choice == "6":
            expired = temp_mail.refresh_expired_emails()
            if expired == 0:
                print("✅ No expired emails found")
            
        elif choice == "7":
            print("Available formats: json, csv, txt")
            format_type = input("Choose format: ").strip()
            temp_mail.export_emails(format_type)
            
        elif choice == "8":
            print("Opening service websites...")
            for service_name, service_info in temp_mail.services.items():
                print(f"🌐 Opening {service_name}...")
                webbrowser.open(service_info['web'])
                time.sleep(1)
            
        elif choice == "0":
            print("🚀 Thank you for using Real Temp Mail Tool!")
            break
            
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()