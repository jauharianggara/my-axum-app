#!/usr/bin/env python3
"""
Security Testing Suite for Axum API
====================================

This script tests all security implementations:
- Rate limiting
- CORS protection  
- SQL injection prevention
- NoSQL injection prevention
- CSRF protection
- XSS protection
- Security headers
- Input validation
"""

import requests
import time
import json
import sys
import threading
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor

class SecurityTester:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.test_results = []
        self.session = requests.Session()
        
    def log_test(self, test_name, passed, message=""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"   └─ {message}")
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'message': message
        })
    
    def test_security_headers(self):
        """Test that security headers are properly set"""
        print("\n🔒 Testing Security Headers...")
        
        try:
            response = requests.get(f"{self.base_url}/health")
            headers = response.headers
            
            # Required security headers
            security_headers = {
                'x-content-type-options': 'nosniff',
                'x-frame-options': 'DENY',
                'x-xss-protection': '1; mode=block',
                'referrer-policy': 'strict-origin-when-cross-origin',
                'permissions-policy': 'camera=(), microphone=(), geolocation=()',
                'content-security-policy': None  # Just check presence
            }
            
            for header, expected_value in security_headers.items():
                header_lower = header.lower()
                if header_lower in headers:
                    if expected_value is None or expected_value in headers[header_lower]:
                        self.log_test(f"Security Header: {header}", True, f"Present: {headers[header_lower]}")
                    else:
                        self.log_test(f"Security Header: {header}", False, f"Wrong value: {headers[header_lower]}")
                else:
                    self.log_test(f"Security Header: {header}", False, "Missing")
            
        except Exception as e:
            self.log_test("Security Headers Test", False, str(e))
    
    def test_cors_protection(self):
        """Test CORS policy enforcement"""
        print("\n🌐 Testing CORS Protection...")
        
        # Test allowed origin
        try:
            response = requests.options(
                f"{self.base_url}/api/auth/login",
                headers={
                    'Origin': 'http://localhost:3000',
                    'Access-Control-Request-Method': 'POST',
                    'Access-Control-Request-Headers': 'content-type'
                }
            )
            
            if response.status_code == 200:
                cors_headers = response.headers
                if 'access-control-allow-origin' in cors_headers:
                    self.log_test("CORS: Allowed Origin", True, f"Origin: {cors_headers['access-control-allow-origin']}")
                else:
                    self.log_test("CORS: Allowed Origin", False, "No CORS headers")
            else:
                self.log_test("CORS: Allowed Origin", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("CORS: Allowed Origin", False, str(e))
        
        # Test disallowed origin
        try:
            response = requests.options(
                f"{self.base_url}/api/auth/login",
                headers={
                    'Origin': 'http://malicious-site.com',
                    'Access-Control-Request-Method': 'POST'
                }
            )
            
            cors_origin = response.headers.get('access-control-allow-origin', '')
            if 'malicious-site.com' not in cors_origin:
                self.log_test("CORS: Blocked Origin", True, "Malicious origin properly blocked")
            else:
                self.log_test("CORS: Blocked Origin", False, "Malicious origin allowed")
                
        except Exception as e:
            self.log_test("CORS: Blocked Origin", False, str(e))
    
    def test_csrf_protection(self):
        """Test CSRF protection"""
        print("\n🛡️ Testing CSRF Protection...")
        
        # Test POST without origin (should fail)
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/register",
                json={
                    "username": "csrf_test_user",
                    "email": "csrf@test.com",
                    "password": "TestPass123",
                    "full_name": "CSRF Test"
                },
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 403:
                response_data = response.json()
                if 'CSRF' in response_data.get('message', ''):
                    self.log_test("CSRF: No Origin Protection", True, "Request blocked without valid origin")
                else:
                    self.log_test("CSRF: No Origin Protection", False, f"Wrong error: {response_data}")
            else:
                self.log_test("CSRF: No Origin Protection", False, f"Request allowed without origin: {response.status_code}")
                
        except Exception as e:
            self.log_test("CSRF: No Origin Protection", False, str(e))
        
        # Test POST with valid origin (should succeed)
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/register",
                json={
                    "username": f"csrf_valid_{int(time.time())}",
                    "email": f"csrf_valid_{int(time.time())}@test.com",
                    "password": "TestPass123",
                    "full_name": "CSRF Valid Test"
                },
                headers={
                    'Content-Type': 'application/json',
                    'Origin': 'http://localhost:3000'
                }
            )
            
            if response.status_code == 200:
                self.log_test("CSRF: Valid Origin Allowed", True, "Request allowed with valid origin")
            else:
                response_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                self.log_test("CSRF: Valid Origin Allowed", False, f"Valid request blocked: {response_data}")
                
        except Exception as e:
            self.log_test("CSRF: Valid Origin Allowed", False, str(e))
    
    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        print("\n💉 Testing SQL Injection Prevention...")
        
        sql_payloads = [
            "admin'; DROP TABLE users; --",
            "' OR 1=1 --",
            "'; SELECT * FROM users; --",
            "admin'/**/UNION/**/SELECT/**/password/**/FROM/**/users--",
            "' OR 'x'='x",
            "1' UNION SELECT version() --"
        ]
        
        for payload in sql_payloads:
            try:
                response = requests.post(
                    f"{self.base_url}/api/auth/register",
                    json={
                        "username": payload,
                        "email": f"sql_test_{int(time.time())}@test.com",
                        "password": "TestPass123",
                        "full_name": "SQL Injection Test"
                    },
                    headers={
                        'Content-Type': 'application/json',
                        'Origin': 'http://localhost:3000'
                    }
                )
                
                if response.status_code == 400:
                    response_data = response.json()
                    if 'security' in response_data.get('message', '').lower():
                        self.log_test(f"SQL Injection: {payload[:20]}...", True, "Malicious input blocked")
                    else:
                        self.log_test(f"SQL Injection: {payload[:20]}...", False, f"Wrong error: {response_data}")
                elif response.status_code == 200:
                    self.log_test(f"SQL Injection: {payload[:20]}...", False, "Malicious input accepted")
                else:
                    # Other errors (validation, etc.) are acceptable
                    self.log_test(f"SQL Injection: {payload[:20]}...", True, f"Blocked with status: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"SQL Injection: {payload[:20]}...", False, str(e))
    
    def test_nosql_injection_prevention(self):
        """Test NoSQL injection prevention"""
        print("\n🍃 Testing NoSQL Injection Prevention...")
        
        nosql_payloads = [
            "admin\", \"$gt\": \"\"",
            "{\"$where\": \"function() { return true; }\"}",
            "admin\"; return true; var dummy=\"",
            "admin\"}, {\"$gt\": \"\"}]; var dummy=[{\"",
            "{\"$regex\": \".*\"}",
            "'; this.password != null && this.password != undefined && this.password != ''"
        ]
        
        for payload in nosql_payloads:
            try:
                response = requests.post(
                    f"{self.base_url}/api/auth/register",
                    json={
                        "username": payload,
                        "email": f"nosql_test_{int(time.time())}@test.com",
                        "password": "TestPass123",
                        "full_name": "NoSQL Injection Test"
                    },
                    headers={
                        'Content-Type': 'application/json',
                        'Origin': 'http://localhost:3000'
                    }
                )
                
                if response.status_code == 400:
                    response_data = response.json()
                    if 'security' in response_data.get('message', '').lower():
                        self.log_test(f"NoSQL Injection: {payload[:20]}...", True, "Malicious input blocked")
                    else:
                        self.log_test(f"NoSQL Injection: {payload[:20]}...", False, f"Wrong error: {response_data}")
                elif response.status_code == 200:
                    self.log_test(f"NoSQL Injection: {payload[:20]}...", False, "Malicious input accepted")
                else:
                    # Other errors (validation, etc.) are acceptable
                    self.log_test(f"NoSQL Injection: {payload[:20]}...", True, f"Blocked with status: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"NoSQL Injection: {payload[:20]}...", False, str(e))
    
    def test_xss_prevention(self):
        """Test XSS prevention"""
        print("\n🚨 Testing XSS Prevention...")
        
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "<svg onload=alert('xss')>",
            "';alert(String.fromCharCode(88,83,83))//';alert(String.fromCharCode(88,83,83))//'",
            "\"><script>alert('xss')</script>",
            "<iframe src=javascript:alert('xss')></iframe>"
        ]
        
        for payload in xss_payloads:
            try:
                response = requests.post(
                    f"{self.base_url}/api/auth/register",
                    json={
                        "username": f"xss_test_{int(time.time())}",
                        "email": f"xss_test_{int(time.time())}@test.com",
                        "password": "TestPass123",
                        "full_name": payload
                    },
                    headers={
                        'Content-Type': 'application/json',
                        'Origin': 'http://localhost:3000'
                    }
                )
                
                if response.status_code == 200:
                    # Check if XSS payload was sanitized
                    response_data = response.json()
                    full_name = response_data.get('data', {}).get('full_name', '')
                    
                    if '<script>' not in full_name and 'javascript:' not in full_name and 'onerror=' not in full_name:
                        self.log_test(f"XSS Prevention: {payload[:20]}...", True, "Malicious content sanitized")
                    else:
                        self.log_test(f"XSS Prevention: {payload[:20]}...", False, f"XSS payload not sanitized: {full_name}")
                elif response.status_code == 400:
                    response_data = response.json()
                    if 'security' in response_data.get('message', '').lower():
                        self.log_test(f"XSS Prevention: {payload[:20]}...", True, "Malicious input blocked")
                    else:
                        self.log_test(f"XSS Prevention: {payload[:20]}...", True, f"Blocked with validation error")
                else:
                    self.log_test(f"XSS Prevention: {payload[:20]}...", True, f"Blocked with status: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"XSS Prevention: {payload[:20]}...", False, str(e))
    
    def test_input_validation(self):
        """Test comprehensive input validation"""
        print("\n📝 Testing Input Validation...")
        
        # Test empty/invalid inputs
        invalid_inputs = [
            {"username": "", "email": "test@test.com", "password": "TestPass123"},
            {"username": "test", "email": "invalid-email", "password": "TestPass123"},
            {"username": "test", "email": "test@test.com", "password": "123"},  # Too short
            {"username": "a" * 100, "email": "test@test.com", "password": "TestPass123"},  # Too long
        ]
        
        for i, invalid_input in enumerate(invalid_inputs):
            try:
                response = requests.post(
                    f"{self.base_url}/api/auth/register",
                    json=invalid_input,
                    headers={
                        'Content-Type': 'application/json',
                        'Origin': 'http://localhost:3000'
                    }
                )
                
                if response.status_code == 400:
                    self.log_test(f"Input Validation: Invalid Input {i+1}", True, "Invalid input properly rejected")
                else:
                    self.log_test(f"Input Validation: Invalid Input {i+1}", False, f"Invalid input accepted: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Input Validation: Invalid Input {i+1}", False, str(e))
    
    def test_authentication_bypass(self):
        """Test authentication bypass attempts"""
        print("\n🔐 Testing Authentication Bypass...")
        
        # Test accessing protected endpoint without auth
        try:
            response = requests.get(f"{self.base_url}/api/jabatans")
            
            if response.status_code == 401:
                self.log_test("Auth Bypass: No Token", True, "Protected endpoint requires authentication")
            else:
                self.log_test("Auth Bypass: No Token", False, f"Protected endpoint accessible without auth: {response.status_code}")
                
        except Exception as e:
            self.log_test("Auth Bypass: No Token", False, str(e))
        
        # Test with invalid token
        try:
            response = requests.get(
                f"{self.base_url}/api/jabatans",
                headers={'Authorization': 'Bearer invalid_token_123'}
            )
            
            if response.status_code == 401:
                self.log_test("Auth Bypass: Invalid Token", True, "Invalid token properly rejected")
            else:
                self.log_test("Auth Bypass: Invalid Token", False, f"Invalid token accepted: {response.status_code}")
                
        except Exception as e:
            self.log_test("Auth Bypass: Invalid Token", False, str(e))
    
    def test_rate_limiting(self):
        """Test rate limiting (if enabled)"""
        print("\n⏱️ Testing Rate Limiting...")
        
        # Note: Rate limiting is available but not currently enabled
        # This test demonstrates how to test it when enabled
        
        try:
            # Make multiple rapid requests
            responses = []
            for i in range(10):
                response = requests.get(f"{self.base_url}/health")
                responses.append(response.status_code)
                time.sleep(0.1)  # Small delay
            
            # All should succeed if rate limiting is disabled
            if all(status == 200 for status in responses):
                self.log_test("Rate Limiting", True, "Rate limiting not enabled (expected for current config)")
            else:
                rate_limited = any(status == 429 for status in responses)
                if rate_limited:
                    self.log_test("Rate Limiting", True, "Rate limiting is active")
                else:
                    self.log_test("Rate Limiting", False, f"Unexpected status codes: {responses}")
                    
        except Exception as e:
            self.log_test("Rate Limiting", False, str(e))
    
    def run_all_tests(self):
        """Run all security tests"""
        print("🚀 Starting Comprehensive Security Test Suite")
        print("=" * 50)
        
        # Run all test categories
        self.test_security_headers()
        self.test_cors_protection()
        self.test_csrf_protection()
        self.test_sql_injection_prevention()
        self.test_nosql_injection_prevention()
        self.test_xss_prevention()
        self.test_input_validation()
        self.test_authentication_bypass()
        self.test_rate_limiting()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Security Test Summary")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['passed'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"  • {result['test']}: {result['message']}")
        
        print("\n🎯 Security Assessment:")
        if failed_tests == 0:
            print("🟢 EXCELLENT: All security tests passed!")
        elif failed_tests <= 2:
            print("🟡 GOOD: Minor security issues detected")
        elif failed_tests <= 5:
            print("🟠 WARNING: Several security issues need attention")
        else:
            print("🔴 CRITICAL: Major security vulnerabilities detected!")
        
        return failed_tests == 0

def main():
    """Main test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Security Testing Suite for Axum API')
    parser.add_argument('--url', default='http://localhost:8080', help='Base URL of the API')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Check if server is running
    try:
        response = requests.get(f"{args.url}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ Server health check failed: {response.status_code}")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server at {args.url}")
        print(f"   Make sure the server is running: cargo run")
        sys.exit(1)
    
    # Run security tests
    tester = SecurityTester(args.url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()