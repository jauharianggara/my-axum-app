#!/usr/bin/env python3
"""
Authentication & Authorization Testing Suite
============================================

This script tests all authentication and authorization features:
- User registration with security validation
- User login functionality
- JWT token validation
- Protected endpoint access
- Role-based access control
- Session management
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin

class AuthTester:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.test_results = []
        self.session = requests.Session()
        self.admin_token = None
        self.user_token = None
        
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
    
    def test_user_registration(self):
        """Test user registration with security validation"""
        print("\n📝 Testing User Registration...")
        
        # Test successful registration
        try:
            timestamp = int(time.time())
            response = requests.post(
                f"{self.base_url}/api/auth/register",
                json={
                    "username": f"testuser_{timestamp}",
                    "email": f"testuser_{timestamp}@test.com",
                    "password": "SecurePass123",
                    "full_name": "Test User"
                },
                headers={
                    'Content-Type': 'application/json',
                    'Origin': 'http://localhost:3000'
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'data' in data:
                    user_data = data['data']
                    if 'id' in user_data and 'username' in user_data:
                        self.log_test("Registration: Valid Input", True, f"User created with ID: {user_data['id']}")
                    else:
                        self.log_test("Registration: Valid Input", False, "Missing user data in response")
                else:
                    self.log_test("Registration: Valid Input", False, "Invalid response format")
            else:
                self.log_test("Registration: Valid Input", False, f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            self.log_test("Registration: Valid Input", False, str(e))
        
        # Test duplicate username
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/register",
                json={
                    "username": f"testuser_{timestamp}",  # Same username
                    "email": f"different_{timestamp}@test.com",
                    "password": "SecurePass123",
                    "full_name": "Another User"
                },
                headers={
                    'Content-Type': 'application/json',
                    'Origin': 'http://localhost:3000'
                }
            )
            
            if response.status_code == 409:  # Conflict
                self.log_test("Registration: Duplicate Username", True, "Duplicate username properly rejected")
            else:
                self.log_test("Registration: Duplicate Username", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Registration: Duplicate Username", False, str(e))
        
        # Test invalid email format
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/register",
                json={
                    "username": f"invaliduser_{timestamp}",
                    "email": "invalid-email-format",
                    "password": "SecurePass123",
                    "full_name": "Invalid User"
                },
                headers={
                    'Content-Type': 'application/json',
                    'Origin': 'http://localhost:3000'
                }
            )
            
            if response.status_code == 400:
                self.log_test("Registration: Invalid Email", True, "Invalid email format rejected")
            else:
                self.log_test("Registration: Invalid Email", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Registration: Invalid Email", False, str(e))
    
    def test_user_login(self):
        """Test user login functionality"""
        print("\n🔑 Testing User Login...")
        
        # First, create a test user for login
        timestamp = int(time.time())
        test_username = f"loginuser_{timestamp}"
        test_email = f"loginuser_{timestamp}@test.com"
        test_password = "LoginPass123"
        
        try:
            # Register test user
            reg_response = requests.post(
                f"{self.base_url}/api/auth/register",
                json={
                    "username": test_username,
                    "email": test_email,
                    "password": test_password,
                    "full_name": "Login Test User"
                },
                headers={
                    'Content-Type': 'application/json',
                    'Origin': 'http://localhost:3000'
                }
            )
            
            if reg_response.status_code != 200:
                self.log_test("Login Setup", False, f"Failed to create test user: {reg_response.status_code}")
                return
                
        except Exception as e:
            self.log_test("Login Setup", False, str(e))
            return
        
        # Test successful login with username
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "username_or_email": test_username,
                    "password": test_password
                },
                headers={
                    'Content-Type': 'application/json',
                    'Origin': 'http://localhost:3000'
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'token' in data.get('data', {}):
                    self.user_token = data['data']['token']
                    self.log_test("Login: Valid Credentials (Username)", True, "Login successful with token")
                else:
                    self.log_test("Login: Valid Credentials (Username)", False, "No token in response")
            else:
                self.log_test("Login: Valid Credentials (Username)", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Login: Valid Credentials (Username)", False, str(e))
        
        # Test successful login with email
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "username_or_email": test_email,
                    "password": test_password
                },
                headers={
                    'Content-Type': 'application/json',
                    'Origin': 'http://localhost:3000'
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'token' in data.get('data', {}):
                    self.log_test("Login: Valid Credentials (Email)", True, "Login successful with email")
                else:
                    self.log_test("Login: Valid Credentials (Email)", False, "No token in response")
            else:
                self.log_test("Login: Valid Credentials (Email)", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Login: Valid Credentials (Email)", False, str(e))
        
        # Test invalid password
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "username_or_email": test_username,
                    "password": "WrongPassword123"
                },
                headers={
                    'Content-Type': 'application/json',
                    'Origin': 'http://localhost:3000'
                }
            )
            
            if response.status_code == 401:
                self.log_test("Login: Invalid Password", True, "Invalid password properly rejected")
            else:
                self.log_test("Login: Invalid Password", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Login: Invalid Password", False, str(e))
        
        # Test non-existent user
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "username_or_email": "nonexistent_user",
                    "password": "SomePassword123"
                },
                headers={
                    'Content-Type': 'application/json',
                    'Origin': 'http://localhost:3000'
                }
            )
            
            if response.status_code == 401:
                self.log_test("Login: Non-existent User", True, "Non-existent user properly rejected")
            else:
                self.log_test("Login: Non-existent User", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Login: Non-existent User", False, str(e))
    
    def test_jwt_token_validation(self):
        """Test JWT token validation"""
        print("\n🎫 Testing JWT Token Validation...")
        
        if not self.user_token:
            self.log_test("JWT: Token Available", False, "No valid token from previous tests")
            return
        
        # Test accessing protected endpoint with valid token
        try:
            response = requests.get(
                f"{self.base_url}/api/user/me",
                headers={'Authorization': f'Bearer {self.user_token}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'data' in data:
                    self.log_test("JWT: Valid Token Access", True, "Protected endpoint accessible with valid token")
                else:
                    self.log_test("JWT: Valid Token Access", False, "Invalid response format")
            else:
                self.log_test("JWT: Valid Token Access", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("JWT: Valid Token Access", False, str(e))
        
        # Test accessing protected endpoint with invalid token
        try:
            response = requests.get(
                f"{self.base_url}/api/user/me",
                headers={'Authorization': 'Bearer invalid_token_123'}
            )
            
            if response.status_code == 401:
                self.log_test("JWT: Invalid Token Rejection", True, "Invalid token properly rejected")
            else:
                self.log_test("JWT: Invalid Token Rejection", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("JWT: Invalid Token Rejection", False, str(e))
        
        # Test accessing protected endpoint without token
        try:
            response = requests.get(f"{self.base_url}/api/user/me")
            
            if response.status_code == 401:
                self.log_test("JWT: Missing Token Rejection", True, "Missing token properly rejected")
            else:
                self.log_test("JWT: Missing Token Rejection", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("JWT: Missing Token Rejection", False, str(e))
    
    def test_protected_endpoints(self):
        """Test access to protected endpoints"""
        print("\n🔒 Testing Protected Endpoints...")
        
        # Test accessing karyawan list without authentication
        try:
            response = requests.get(f"{self.base_url}/api/karyawans")
            
            if response.status_code == 401:
                self.log_test("Protected: Karyawan List (No Auth)", True, "Karyawan endpoint requires authentication")
            else:
                self.log_test("Protected: Karyawan List (No Auth)", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Protected: Karyawan List (No Auth)", False, str(e))
        
        # Test accessing kantor list without authentication
        try:
            response = requests.get(f"{self.base_url}/api/kantors")
            
            if response.status_code == 401:
                self.log_test("Protected: Kantor List (No Auth)", True, "Kantor endpoint requires authentication")
            else:
                self.log_test("Protected: Kantor List (No Auth)", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Protected: Kantor List (No Auth)", False, str(e))
        
        # Test accessing jabatan list without authentication
        try:
            response = requests.get(f"{self.base_url}/api/jabatans")
            
            if response.status_code == 401:
                self.log_test("Protected: Jabatan List (No Auth)", True, "Jabatan endpoint requires authentication")
            else:
                self.log_test("Protected: Jabatan List (No Auth)", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Protected: Jabatan List (No Auth)", False, str(e))
        
        # Test accessing with valid token
        if self.user_token:
            try:
                response = requests.get(
                    f"{self.base_url}/api/jabatans",
                    headers={'Authorization': f'Bearer {self.user_token}'}
                )
                
                if response.status_code == 200:
                    self.log_test("Protected: Jabatan List (With Auth)", True, "Jabatan endpoint accessible with valid token")
                else:
                    self.log_test("Protected: Jabatan List (With Auth)", False, f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log_test("Protected: Jabatan List (With Auth)", False, str(e))
    
    def test_admin_functionality(self):
        """Test admin-specific functionality"""
        print("\n👑 Testing Admin Functionality...")
        
        # Try to login as admin (if testuser exists)
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "username_or_email": "testuser",
                    "password": "password123"
                },
                headers={
                    'Content-Type': 'application/json',
                    'Origin': 'http://localhost:3000'
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'token' in data.get('data', {}):
                    self.admin_token = data['data']['token']
                    self.log_test("Admin: Login", True, "Admin login successful")
                else:
                    self.log_test("Admin: Login", False, "No token in admin login response")
            else:
                self.log_test("Admin: Login", False, f"Admin login failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Admin: Login", False, str(e))
        
        # Test creating karyawan (admin function)
        if self.admin_token:
            try:
                timestamp = int(time.time())
                response = requests.post(
                    f"{self.base_url}/api/karyawans",
                    json={
                        "nama": f"Test Employee {timestamp}",
                        "jabatan_id": 1,
                        "gaji": "5000000",
                        "kantor_id": 1
                    },
                    headers={
                        'Authorization': f'Bearer {self.admin_token}',
                        'Content-Type': 'application/json',
                        'Origin': 'http://localhost:3000'
                    }
                )
                
                if response.status_code == 200 or response.status_code == 201:
                    self.log_test("Admin: Create Karyawan", True, "Admin can create karyawan")
                else:
                    self.log_test("Admin: Create Karyawan", False, f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log_test("Admin: Create Karyawan", False, str(e))
    
    def test_session_management(self):
        """Test session management"""
        print("\n⏰ Testing Session Management...")
        
        # Test token expiration (if implemented)
        if self.user_token:
            # For now, just verify token is still valid
            try:
                response = requests.get(
                    f"{self.base_url}/api/user/me",
                    headers={'Authorization': f'Bearer {self.user_token}'}
                )
                
                if response.status_code == 200:
                    self.log_test("Session: Token Validity", True, "Token remains valid during session")
                else:
                    self.log_test("Session: Token Validity", False, f"Token invalid: {response.status_code}")
                    
            except Exception as e:
                self.log_test("Session: Token Validity", False, str(e))
        
        # Test malformed Authorization header
        try:
            response = requests.get(
                f"{self.base_url}/api/user/me",
                headers={'Authorization': 'InvalidFormat token123'}
            )
            
            if response.status_code == 401:
                self.log_test("Session: Malformed Header", True, "Malformed Authorization header rejected")
            else:
                self.log_test("Session: Malformed Header", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Session: Malformed Header", False, str(e))
    
    def run_all_tests(self):
        """Run all authentication tests"""
        print("🚀 Starting Authentication & Authorization Test Suite")
        print("=" * 60)
        
        # Run all test categories
        self.test_user_registration()
        self.test_user_login()
        self.test_jwt_token_validation()
        self.test_protected_endpoints()
        self.test_admin_functionality()
        self.test_session_management()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Authentication Test Summary")
        print("=" * 60)
        
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
        
        print("\n🎯 Authentication Assessment:")
        if failed_tests == 0:
            print("🟢 EXCELLENT: All authentication tests passed!")
        elif failed_tests <= 2:
            print("🟡 GOOD: Minor authentication issues detected")
        elif failed_tests <= 5:
            print("🟠 WARNING: Several authentication issues need attention")
        else:
            print("🔴 CRITICAL: Major authentication vulnerabilities detected!")
        
        return failed_tests == 0

def main():
    """Main test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Authentication Testing Suite for Axum API')
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
    
    # Run authentication tests
    tester = AuthTester(args.url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()