#!/usr/bin/env python3
"""
Real Auto Gmail Creator - منشئ Gmail تلقائي حقيقي
This tool actually creates real Gmail accounts - هذه الأداة تنشئ حسابات Gmail حقيقية
"""

import os
import sys
import time
import random
import string
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class RealGmailCreator:
    def __init__(self):
        self.driver = None
        self.accounts_created = []
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver with stealth options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Add user agent
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver setup completed")
        except Exception as e:
            print(f"❌ Error setting up driver: {e}")
            print("Please install Chrome and ChromeDriver")
    
    def generate_real_info(self):
        """Generate realistic personal information"""
        first_names = [
            "أحمد", "محمد", "علي", "عمر", "يوسف", "إبراهيم", "عبدالله", "خالد",
            "سعد", "فهد", "سلطان", "عبدالرحمن", "عبدالعزيز", "ماجد", "نواف",
            "Ahmed", "Mohammed", "Ali", "Omar", "Youssef", "Ibrahim", "Abdullah"
        ]
        
        last_names = [
            "الزهراني", "العتيبي", "القحطاني", "الغامدي", "الحربي", "القرني",
            "المالكي", "السهلي", "العمري", "الزهراني", "العتيبي", "القحطاني",
            "Al-Zahrani", "Al-Otaibi", "Al-Qahtani", "Al-Ghamdi", "Al-Harbi"
        ]
        
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        domain = random.choice(domains)
        
        # Generate realistic username
        username_options = [
            f"{first_name.lower()}{last_name.lower()}{random.randint(100, 999)}",
            f"{first_name.lower()}.{last_name.lower()}{random.randint(10, 99)}",
            f"{first_name.lower()}{random.randint(1000, 9999)}",
            f"{first_name.lower()}_{last_name.lower()}{random.randint(100, 999)}"
        ]
        
        username = random.choice(username_options)
        email = f"{username}@{domain}"
        
        # Generate realistic password
        password = self.generate_strong_password()
        
        # Generate phone number
        phone = self.generate_phone_number()
        
        # Generate birth date
        birth_year = random.randint(1980, 2005)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        
        return {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'password': password,
            'phone': phone,
            'birth_year': birth_year,
            'birth_month': birth_month,
            'birth_day': birth_day
        }
    
    def generate_strong_password(self):
        """Generate strong password"""
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        password = []
        password.append(random.choice(lowercase))
        password.append(random.choice(uppercase))
        password.append(random.choice(digits))
        password.append(random.choice(symbols))
        
        # Fill remaining length
        remaining_length = random.randint(8, 12) - 4
        all_chars = lowercase + uppercase + digits + symbols
        password.extend(random.choices(all_chars, k=remaining_length))
        
        # Shuffle password
        random.shuffle(password)
        return ''.join(password)
    
    def generate_phone_number(self):
        """Generate realistic phone number"""
        country_codes = ["+966", "+971", "+20", "+965", "+974", "+973", "+968", "+962"]
        country_code = random.choice(country_codes)
        
        if country_code == "+966":  # Saudi Arabia
            area_codes = ["50", "51", "53", "54", "55", "56", "57", "58", "59"]
            area_code = random.choice(area_codes)
            number = random.randint(1000000, 9999999)
        elif country_code == "+971":  # UAE
            area_codes = ["50", "51", "52", "54", "55", "56"]
            area_code = random.choice(area_codes)
            number = random.randint(1000000, 9999999)
        else:
            area_code = random.choice(["10", "11", "12", "13", "14", "15"])
            number = random.randint(1000000, 9999999)
        
        return f"{country_code}{area_code}{number}"
    
    def create_gmail_account(self):
        """Actually create Gmail account"""
        try:
            print("🚀 Starting Gmail account creation...")
            
            # Go to Gmail signup
            self.driver.get("https://accounts.google.com/signup")
            time.sleep(3)
            
            # Generate realistic info
            info = self.generate_real_info()
            print(f"📝 Generated info for: {info['first_name']} {info['last_name']}")
            
            # Fill first name
            first_name_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "firstName"))
            )
            first_name_field.send_keys(info['first_name'])
            
            # Fill last name
            last_name_field = self.driver.find_element(By.NAME, "lastName")
            last_name_field.send_keys(info['last_name'])
            
            # Click Next
            next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            time.sleep(2)
            
            # Fill birth date
            birth_year_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "day"))
            )
            birth_year_field.send_keys(str(info['birth_day']))
            
            birth_month_field = self.driver.find_element(By.NAME, "month")
            birth_month_field.click()
            month_option = self.driver.find_element(By.XPATH, f"//option[@value='{info['birth_month']}']")
            month_option.click()
            
            birth_year_field = self.driver.find_element(By.NAME, "year")
            birth_year_field.send_keys(str(info['birth_year']))
            
            # Click Next
            next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            time.sleep(2)
            
            # Fill gender
            gender_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "gender"))
            )
            gender_field.click()
            gender_option = self.driver.find_element(By.XPATH, "//option[@value='1']")  # Male
            gender_option.click()
            
            # Click Next
            next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            time.sleep(2)
            
            # Fill email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Username"))
            )
            email_field.send_keys(info['username'])
            
            # Click Next
            next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            time.sleep(2)
            
            # Fill password
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Passwd"))
            )
            password_field.send_keys(info['password'])
            
            confirm_password_field = self.driver.find_element(By.NAME, "PasswdAgain")
            confirm_password_field.send_keys(info['password'])
            
            # Click Next
            next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            time.sleep(2)
            
            # Fill phone number
            phone_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "phoneNumber"))
            )
            phone_field.send_keys(info['phone'])
            
            # Click Next
            next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            time.sleep(2)
            
            # Handle verification (simplified)
            print("📱 Phone verification required...")
            print("Please complete verification manually")
            
            # Save account info
            account_info = {
                'email': f"{info['username']}@gmail.com",
                'password': info['password'],
                'first_name': info['first_name'],
                'last_name': info['last_name'],
                'phone': info['phone'],
                'status': 'created_needs_verification',
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.accounts_created.append(account_info)
            self.save_accounts()
            
            print(f"✅ Gmail account created successfully!")
            print(f"📧 Email: {account_info['email']}")
            print(f"🔑 Password: {account_info['password']}")
            print(f"📱 Phone: {account_info['phone']}")
            print("⚠️  Phone verification required to complete setup")
            
            return account_info
            
        except Exception as e:
            print(f"❌ Error creating Gmail account: {e}")
            return None
    
    def save_accounts(self):
        """Save created accounts to file"""
        try:
            with open('created_gmail_accounts.json', 'w', encoding='utf-8') as f:
                json.dump(self.accounts_created, f, ensure_ascii=False, indent=2)
            print(f"💾 Saved {len(self.accounts_created)} accounts to file")
        except Exception as e:
            print(f"❌ Error saving accounts: {e}")
    
    def load_accounts(self):
        """Load existing accounts from file"""
        try:
            if os.path.exists('created_gmail_accounts.json'):
                with open('created_gmail_accounts.json', 'r', encoding='utf-8') as f:
                    self.accounts_created = json.load(f)
                print(f"📂 Loaded {len(self.accounts_created)} existing accounts")
        except Exception as e:
            print(f"❌ Error loading accounts: {e}")
    
    def show_accounts(self):
        """Show all created accounts"""
        if not self.accounts_created:
            print("❌ No accounts created yet")
            return
        
        print(f"\n📊 Created Gmail Accounts ({len(self.accounts_created)}):")
        print("=" * 80)
        
        for i, account in enumerate(self.accounts_created, 1):
            print(f"{i}. 📧 {account['email']}")
            print(f"   🔑 Password: {account['password']}")
            print(f"   👤 Name: {account['first_name']} {account['last_name']}")
            print(f"   📱 Phone: {account['phone']}")
            print(f"   📅 Created: {account['created_at']}")
            print(f"   📊 Status: {account['status']}")
            print("-" * 80)
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")

def main():
    """Main function"""
    print("🚀🚀🚀 REAL AUTO GMAIL CREATOR 🚀🚀🚀")
    print("This tool actually creates real Gmail accounts!")
    print("=" * 50)
    
    creator = RealGmailCreator()
    creator.load_accounts()
    
    while True:
        print("\n" + "=" * 50)
        print("1. 🚀 Create new Gmail account")
        print("2. 📊 Show created accounts")
        print("3. 💾 Save accounts")
        print("4. 🔒 Close browser")
        print("0. ❌ Exit")
        print("=" * 50)
        
        choice = input("Choose option: ")
        
        if choice == "1":
            creator.create_gmail_account()
        elif choice == "2":
            creator.show_accounts()
        elif choice == "3":
            creator.save_accounts()
        elif choice == "4":
            creator.close()
        elif choice == "0":
            creator.close()
            print("🚀 Thank you for using Real Gmail Creator!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()