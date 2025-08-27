#!/usr/bin/env python3
"""
Production Testing Script - سكريبت اختبار الإنتاج
Real API testing - اختبار APIs حقيقي
"""

import asyncio
import aiohttp
import requests
import json
import time
import sys
from datetime import datetime

class ProductionTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.results = {}
        self.start_time = time.time()
        
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    def print_result(self, test_name, success, details=""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
        if details:
            print(f"    Details: {details}")
        self.results[test_name] = success
    
    async def test_health_endpoint(self):
        """Test application health endpoint"""
        self.print_header("Testing Health Endpoint")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health") as response:
                    if response.status == 200:
                        content = await response.text()
                        self.print_result("Health Check", True, f"Status: {response.status}")
                    else:
                        self.print_result("Health Check", False, f"Status: {response.status}")
        except Exception as e:
            self.print_result("Health Check", False, f"Error: {str(e)}")
    
    async def test_google_merchant_api(self):
        """Test Google Merchant Center API integration"""
        self.print_header("Testing Google Merchant Center API")
        
        try:
            # Test API endpoint
            test_data = {
                "email": "test@example.com",
                "business_name": "Test Business",
                "website": "https://testbusiness.com"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/api/merchant/create", json=test_data) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        self.print_result("Merchant API Integration", True, f"Response: {result}")
                    else:
                        self.print_result("Merchant API Integration", False, f"Status: {response.status}")
        except Exception as e:
            self.print_result("Merchant API Integration", False, f"Error: {str(e)}")
    
    async def test_openai_document_generation(self):
        """Test OpenAI document generation API"""
        self.print_header("Testing OpenAI Document Generation")
        
        try:
            test_data = {
                "document_type": "business_plan",
                "content": "Create a business plan for an e-commerce store",
                "language": "ar"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/api/documents/generate", json=test_data) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        self.print_result("OpenAI Document Generation", True, f"Response: {result}")
                    else:
                        self.print_result("OpenAI Document Generation", False, f"Status: {response.status}")
        except Exception as e:
            self.print_result("OpenAI Document Generation", False, f"Error: {str(e)}")
    
    async def test_temp_mail_service(self):
        """Test temporary email service"""
        self.print_header("Testing Temporary Email Service")
        
        try:
            test_data = {
                "country": "SA",
                "service": "1secmail"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/api/temp-mail/create", json=test_data) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        self.print_result("Temp Mail Service", True, f"Response: {result}")
                    else:
                        self.print_result("Temp Mail Service", False, f"Status: {response.status}")
        except Exception as e:
            self.print_result("Temp Mail Service", False, f"Error: {str(e)}")
    
    async def test_dns_check(self):
        """Test DNS checking service"""
        self.print_header("Testing DNS Check Service")
        
        try:
            test_data = {
                "domain": "google.com",
                "record_type": "A"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/api/dns/check", json=test_data) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        self.print_result("DNS Check Service", True, f"Response: {result}")
                    else:
                        self.print_result("DNS Check Service", False, f"Status: {response.status}")
        except Exception as e:
            self.print_result("DNS Check Service", False, f"Error: {str(e)}")
    
    async def test_ssl_check(self):
        """Test SSL checking service"""
        self.print_header("Testing SSL Check Service")
        
        try:
            test_data = {
                "domain": "google.com"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/api/ssl/check", json=test_data) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        self.print_result("SSL Check Service", True, f"Response: {result}")
                    else:
                        self.print_result("SSL Check Service", False, f"Status: {response.status}")
        except Exception as e:
            self.print_result("SSL Check Service", False, f"Error: {str(e)}")
    
    async def test_country_info(self):
        """Test Arabic countries information service"""
        self.print_header("Testing Arabic Countries Information")
        
        try:
            test_data = {
                "country_code": "SA"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/api/countries/info", json=test_data) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        self.print_result("Country Information Service", True, f"Response: {result}")
                    else:
                        self.print_result("Country Information Service", False, f"Status: {response.status}")
        except Exception as e:
            self.print_result("Country Information Service", False, f"Error: {str(e)}")
    
    async def test_database_connection(self):
        """Test database connectivity"""
        self.print_header("Testing Database Connection")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/database/status") as response:
                    if response.status == 200:
                        result = await response.json()
                        self.print_result("Database Connection", True, f"Response: {result}")
                    else:
                        self.print_result("Database Connection", False, f"Status: {response.status}")
        except Exception as e:
            self.print_result("Database Connection", False, f"Error: {str(e)}")
    
    async def test_redis_connection(self):
        """Test Redis connectivity"""
        self.print_header("Testing Redis Connection")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/redis/status") as response:
                    if response.status == 200:
                        result = await response.json()
                        self.print_result("Redis Connection", True, f"Response: {result}")
                    else:
                        self.print_result("Redis Connection", False, f"Status: {response.status}")
        except Exception as e:
            self.print_result("Redis Connection", False, f"Error: {str(e)}")
    
    async def test_rate_limiting(self):
        """Test API rate limiting"""
        self.print_header("Testing Rate Limiting")
        
        try:
            # Make multiple rapid requests to test rate limiting
            async with aiohttp.ClientSession() as session:
                responses = []
                for i in range(15):  # Exceed rate limit
                    async with session.get(f"{self.base_url}/health") as response:
                        responses.append(response.status)
                
                # Check if rate limiting is working
                if 429 in responses:  # 429 = Too Many Requests
                    self.print_result("Rate Limiting", True, "Rate limiting is working")
                else:
                    self.print_result("Rate Limiting", False, "Rate limiting not working")
        except Exception as e:
            self.print_result("Rate Limiting", False, f"Error: {str(e)}")
    
    async def test_security_headers(self):
        """Test security headers"""
        self.print_header("Testing Security Headers")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/") as response:
                    headers = response.headers
                    
                    security_headers = [
                        'X-Frame-Options',
                        'X-Content-Type-Options',
                        'X-XSS-Protection',
                        'Strict-Transport-Security'
                    ]
                    
                    missing_headers = []
                    for header in security_headers:
                        if header not in headers:
                            missing_headers.append(header)
                    
                    if not missing_headers:
                        self.print_result("Security Headers", True, "All security headers present")
                    else:
                        self.print_result("Security Headers", False, f"Missing: {missing_headers}")
        except Exception as e:
            self.print_result("Security Headers", False, f"Error: {str(e)}")
    
    async def test_performance(self):
        """Test application performance"""
        self.print_header("Testing Performance")
        
        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health") as response:
                    response_time = time.time() - start_time
                    
                    if response_time < 0.5:  # Less than 500ms
                        self.print_result("Response Time", True, f"Response time: {response_time:.3f}s")
                    else:
                        self.print_result("Response Time", False, f"Response time: {response_time:.3f}s (too slow)")
        except Exception as e:
            self.print_result("Response Time", False, f"Error: {str(e)}")
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("Test Summary")
        
        total_tests = len(self.results)
        passed_tests = sum(self.results.values())
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\nFailed Tests:")
            for test_name, success in self.results.items():
                if not success:
                    print(f"  ❌ {test_name}")
        
        total_time = time.time() - self.start_time
        print(f"\nTotal Test Time: {total_time:.2f} seconds")
        
        if failed_tests == 0:
            print(f"\n🎉 ALL TESTS PASSED! Your application is production-ready! 🎉")
        else:
            print(f"\n⚠️  Some tests failed. Please review and fix issues before production deployment.")
    
    async def run_all_tests(self):
        """Run all production tests"""
        print("🚀 Starting Production Testing Suite")
        print(f"Testing Application: {self.base_url}")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all tests
        await self.test_health_endpoint()
        await self.test_google_merchant_api()
        await self.test_openai_document_generation()
        await self.test_temp_mail_service()
        await self.test_dns_check()
        await self.test_ssl_check()
        await self.test_country_info()
        await self.test_database_connection()
        await self.test_redis_connection()
        await self.test_rate_limiting()
        await self.test_security_headers()
        await self.test_performance()
        
        # Print summary
        self.print_summary()

async def main():
    """Main function"""
    tester = ProductionTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    # Run the test suite
    asyncio.run(main())