#!/usr/bin/env python3
"""
Real DNS Checker Tool - أداة فحص DNS الحقيقية
This tool actually checks real DNS records - هذه الأداة تفحص سجلات DNS حقيقية
"""

import os
import sys
import time
import json
import requests
import dns.resolver
import dns.reversename
import socket
import whois
from datetime import datetime
import concurrent.futures

class RealDNSChecker:
    def __init__(self):
        self.results = []
        self.load_results()
        
        # DNS servers for different regions
        self.dns_servers = {
            'google': ['8.8.8.8', '8.8.4.4'],
            'cloudflare': ['1.1.1.1', '1.0.0.1'],
            'opendns': ['208.67.222.222', '208.67.220.220'],
            'quad9': ['9.9.9.9', '149.112.112.112'],
            'saudi': ['212.26.0.1', '212.26.0.2'],
            'uae': ['193.227.99.1', '193.227.99.2'],
            'egypt': ['156.192.1.1', '156.192.1.2']
        }
        
        # Common record types
        self.record_types = [
            'A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS', 'PTR', 'SOA', 'SRV', 'CAA'
        ]
    
    def load_results(self):
        """Load previous DNS check results"""
        try:
            if os.path.exists('dns_check_results.json'):
                with open('dns_check_results.json', 'r', encoding='utf-8') as f:
                    self.results = json.load(f)
                print(f"📂 Loaded {len(self.results)} previous DNS check results")
        except Exception as e:
            print(f"❌ Error loading results: {e}")
    
    def save_results(self):
        """Save DNS check results to file"""
        try:
            with open('dns_check_results.json', 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"💾 Saved {len(self.results)} DNS check results")
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def check_dns_record(self, domain, record_type, dns_server=None):
        """Check specific DNS record type"""
        try:
            resolver = dns.resolver.Resolver()
            
            if dns_server:
                resolver.nameservers = [dns_server]
            
            answers = resolver.resolve(domain, record_type)
            
            results = []
            for answer in answers:
                if record_type == 'A':
                    results.append(str(answer))
                elif record_type == 'AAAA':
                    results.append(str(answer))
                elif record_type == 'CNAME':
                    results.append(str(answer))
                elif record_type == 'MX':
                    results.append(f"{answer.preference} {answer.exchange}")
                elif record_type == 'TXT':
                    results.append(str(answer))
                elif record_type == 'NS':
                    results.append(str(answer))
                elif record_type == 'SOA':
                    results.append(f"{answer.mname} {answer.rname} {answer.serial} {answer.refresh} {answer.retry} {answer.expire} {answer.minimum}")
                else:
                    results.append(str(answer))
            
            return {
                'type': record_type,
                'values': results,
                'count': len(results),
                'status': 'success'
            }
            
        except dns.resolver.NXDOMAIN:
            return {
                'type': record_type,
                'values': [],
                'count': 0,
                'status': 'NXDOMAIN',
                'error': 'Domain does not exist'
            }
        except dns.resolver.NoAnswer:
            return {
                'type': record_type,
                'values': [],
                'count': 0,
                'status': 'NoAnswer',
                'error': 'No records found'
            }
        except Exception as e:
            return {
                'type': record_type,
                'values': [],
                'count': 0,
                'status': 'error',
                'error': str(e)
            }
    
    def check_all_records(self, domain, dns_server=None):
        """Check all common DNS record types"""
        print(f"🔍 Checking DNS records for: {domain}")
        print(f"🌐 Using DNS server: {dns_server if dns_server else 'Default'}")
        
        results = {}
        total_records = 0
        
        for record_type in self.record_types:
            print(f"  📋 Checking {record_type} records...")
            result = self.check_dns_record(domain, record_type, dns_server)
            results[record_type] = result
            
            if result['status'] == 'success':
                total_records += result['count']
                print(f"    ✅ Found {result['count']} {record_type} records")
            else:
                print(f"    ❌ {record_type}: {result.get('error', 'No records')}")
            
            time.sleep(0.5)  # Small delay between requests
        
        return {
            'domain': domain,
            'dns_server': dns_server,
            'timestamp': datetime.now().isoformat(),
            'total_records': total_records,
            'records': results
        }
    
    def check_multiple_dns_servers(self, domain):
        """Check DNS records using multiple DNS servers"""
        print(f"🌐 Checking {domain} with multiple DNS servers...")
        
        results = {}
        
        for server_name, servers in self.dns_servers.items():
            print(f"\n🔍 Checking with {server_name} DNS servers...")
            server_result = self.check_all_records(domain, servers[0])
            results[server_name] = server_result
            
            # Compare results
            if len(results) > 1:
                self.compare_dns_results(domain, results)
        
        return results
    
    def compare_dns_results(self, domain, results):
        """Compare DNS results from different servers"""
        print(f"\n📊 DNS Results Comparison for {domain}:")
        print("=" * 80)
        
        # Get all record types
        all_record_types = set()
        for server_result in results.values():
            all_record_types.update(server_result['records'].keys())
        
        # Compare each record type
        for record_type in sorted(all_record_types):
            print(f"\n📋 {record_type} Records:")
            print("-" * 40)
            
            for server_name, server_result in results.items():
                record_data = server_result['records'].get(record_type, {})
                status = record_data.get('status', 'unknown')
                count = record_data.get('count', 0)
                
                if status == 'success':
                    print(f"  {server_name:12} ✅ {count:2} records")
                else:
                    print(f"  {server_name:12} ❌ {record_data.get('error', 'Error')}")
    
    def reverse_dns_lookup(self, ip_address):
        """Perform reverse DNS lookup"""
        try:
            print(f"🔍 Performing reverse DNS lookup for: {ip_address}")
            
            # Reverse DNS using dns.reversename
            reverse_name = dns.reversename.from_address(ip_address)
            resolver = dns.resolver.Resolver()
            
            try:
                answers = resolver.resolve(reverse_name, 'PTR')
                ptr_records = [str(answer) for answer in answers]
                
                print(f"✅ Reverse DNS results:")
                for ptr in ptr_records:
                    print(f"  📋 {ptr}")
                
                return {
                    'ip': ip_address,
                    'ptr_records': ptr_records,
                    'status': 'success'
                }
                
            except dns.resolver.NXDOMAIN:
                print(f"❌ No PTR records found")
                return {
                    'ip': ip_address,
                    'ptr_records': [],
                    'status': 'NXDOMAIN'
                }
                
        except Exception as e:
            print(f"❌ Error in reverse DNS lookup: {e}")
            return {
                'ip': ip_address,
                'ptr_records': [],
                'status': 'error',
                'error': str(e)
            }
    
    def check_domain_info(self, domain):
        """Get comprehensive domain information"""
        print(f"🌐 Getting comprehensive information for: {domain}")
        
        domain_info = {
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'dns_records': {},
            'whois_info': {},
            'ip_info': {},
            'ssl_info': {}
        }
        
        # Check DNS records
        print("  📋 Checking DNS records...")
        domain_info['dns_records'] = self.check_all_records(domain)
        
        # Get WHOIS information
        print("  📊 Getting WHOIS information...")
        try:
            w = whois.whois(domain)
            domain_info['whois_info'] = {
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'status': w.status,
                'name_servers': w.name_servers
            }
            print("    ✅ WHOIS information retrieved")
        except Exception as e:
            print(f"    ❌ WHOIS error: {e}")
            domain_info['whois_info'] = {'error': str(e)}
        
        # Get IP information
        print("  🌍 Getting IP information...")
        try:
            ip_addresses = []
            for record_type in ['A', 'AAAA']:
                result = self.check_dns_record(domain, record_type)
                if result['status'] == 'success':
                    ip_addresses.extend(result['values'])
            
            if ip_addresses:
                domain_info['ip_info'] = {
                    'ip_addresses': ip_addresses,
                    'primary_ip': ip_addresses[0] if ip_addresses else None
                }
                print(f"    ✅ Found {len(ip_addresses)} IP addresses")
            else:
                print("    ❌ No IP addresses found")
                
        except Exception as e:
            print(f"    ❌ IP info error: {e}")
            domain_info['ip_info'] = {'error': str(e)}
        
        # Check SSL certificate
        print("  🔐 Checking SSL certificate...")
        try:
            ssl_info = self.check_ssl_certificate(domain)
            domain_info['ssl_info'] = ssl_info
            if ssl_info['status'] == 'success':
                print("    ✅ SSL certificate information retrieved")
            else:
                print(f"    ❌ SSL error: {ssl_info.get('error', 'Unknown')}")
        except Exception as e:
            print(f"    ❌ SSL check error: {e}")
            domain_info['ssl_info'] = {'error': str(e)}
        
        return domain_info
    
    def check_ssl_certificate(self, domain):
        """Check SSL certificate information"""
        try:
            import ssl
            import socket
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        'status': 'success',
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': cert['version'],
                        'serial_number': cert['serialNumber'],
                        'not_before': cert['notBefore'],
                        'not_after': cert['notAfter'],
                        'san': cert.get('subjectAltName', [])
                    }
                    
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def bulk_dns_check(self, domains, record_types=None):
        """Check DNS records for multiple domains"""
        if record_types is None:
            record_types = ['A', 'MX', 'TXT', 'NS']
        
        print(f"🚀 Starting bulk DNS check for {len(domains)} domains...")
        
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_domain = {
                executor.submit(self.check_all_records, domain): domain 
                for domain in domains
            }
            
            for future in concurrent.futures.as_completed(future_to_domain):
                domain = future_to_domain[future]
                try:
                    result = future.result()
                    results.append(result)
                    print(f"✅ Completed DNS check for {domain}")
                except Exception as e:
                    print(f"❌ Error checking {domain}: {e}")
                    results.append({
                        'domain': domain,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
        
        return results
    
    def export_results(self, format='json'):
        """Export DNS check results"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if format == 'json':
                filename = f"dns_check_results_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.results, f, ensure_ascii=False, indent=2)
                print(f"💾 Exported to {filename}")
            
            elif format == 'csv':
                filename = f"dns_check_results_{timestamp}.csv"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Domain,Record Type,Status,Count,Values,Timestamp\n")
                    for result in self.results:
                        domain = result.get('domain', 'Unknown')
                        timestamp = result.get('timestamp', 'Unknown')
                        
                        for record_type, record_data in result.get('records', {}).items():
                            status = record_data.get('status', 'Unknown')
                            count = record_data.get('count', 0)
                            values = '; '.join(record_data.get('values', []))
                            
                            f.write(f'"{domain}","{record_type}","{status}",{count},"{values}","{timestamp}"\n')
                print(f"💾 Exported to {filename}")
            
            elif format == 'txt':
                filename = f"dns_check_results_{timestamp}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    for result in self.results:
                        f.write(f"Domain: {result.get('domain', 'Unknown')}\n")
                        f.write(f"Timestamp: {result.get('timestamp', 'Unknown')}\n")
                        f.write(f"Total Records: {result.get('total_records', 0)}\n")
                        f.write("-" * 50 + "\n")
                        
                        for record_type, record_data in result.get('records', {}).items():
                            f.write(f"{record_type} Records:\n")
                            if record_data['status'] == 'success':
                                for value in record_data['values']:
                                    f.write(f"  {value}\n")
                            else:
                                f.write(f"  Error: {record_data.get('error', 'Unknown')}\n")
                            f.write("\n")
                        
                        f.write("=" * 50 + "\n\n")
                print(f"💾 Exported to {filename}")
            
            else:
                print(f"❌ Format {format} not supported")
                
        except Exception as e:
            print(f"❌ Error exporting results: {e}")
    
    def show_results(self):
        """Show all DNS check results"""
        if not self.results:
            print("❌ No DNS check results found")
            return
        
        print(f"\n📊 DNS Check Results ({len(self.results)}):")
        print("=" * 100)
        
        for i, result in enumerate(self.results, 1):
            domain = result.get('domain', 'Unknown')
            timestamp = result.get('timestamp', 'Unknown')
            total_records = result.get('total_records', 0)
            
            print(f"{i}. 🌐 {domain}")
            print(f"   📅 {timestamp[:19]}")
            print(f"   📊 Total Records: {total_records}")
            
            if 'records' in result:
                for record_type, record_data in result['records'].items():
                    status = "✅" if record_data['status'] == 'success' else "❌"
                    count = record_data['count']
                    print(f"   {status} {record_type}: {count} records")
            
            print("-" * 100)

def main():
    """Main function"""
    print("🚀🚀🚀 REAL DNS CHECKER TOOL 🚀🚀🚀")
    print("This tool actually checks real DNS records!")
    print("=" * 50)
    
    checker = RealDNSChecker()
    
    while True:
        print("\n" + "=" * 50)
        print("1. 🔍 Check single domain DNS")
        print("2. 🌐 Check with multiple DNS servers")
        print("3. 🔄 Reverse DNS lookup")
        print("4. 📊 Comprehensive domain check")
        print("5. 🚀 Bulk DNS check")
        print("6. 📋 Show all results")
        print("7. 💾 Export results")
        print("8. 🗑️  Clear results")
        print("0. ❌ Exit")
        print("=" * 50)
        
        choice = input("Choose option: ")
        
        if choice == "1":
            domain = input("Enter domain: ").strip()
            if domain:
                result = checker.check_all_records(domain)
                checker.results.append(result)
                checker.save_results()
        
        elif choice == "2":
            domain = input("Enter domain: ").strip()
            if domain:
                results = checker.check_multiple_dns_servers(domain)
                for result in results.values():
                    checker.results.append(result)
                checker.save_results()
        
        elif choice == "3":
            ip_address = input("Enter IP address: ").strip()
            if ip_address:
                checker.reverse_dns_lookup(ip_address)
        
        elif choice == "4":
            domain = input("Enter domain: ").strip()
            if domain:
                result = checker.check_domain_info(domain)
                checker.results.append(result)
                checker.save_results()
        
        elif choice == "5":
            domains_input = input("Enter domains (comma-separated): ").strip()
            if domains_input:
                domains = [d.strip() for d in domains_input.split(',')]
                results = checker.bulk_dns_check(domains)
                checker.results.extend(results)
                checker.save_results()
        
        elif choice == "6":
            checker.show_results()
        
        elif choice == "7":
            print("Available formats: json, csv, txt")
            format_type = input("Choose format: ").strip()
            checker.export_results(format_type)
        
        elif choice == "8":
            checker.results.clear()
            checker.save_results()
            print("🗑️  All results cleared")
        
        elif choice == "0":
            print("🚀 Thank you for using Real DNS Checker Tool!")
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()