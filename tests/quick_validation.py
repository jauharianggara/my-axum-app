#!/usr/bin/env python3
"""
Quick Security & Authentication Validation
==========================================

Quick validation script for essential security and authentication features.
This script runs the most critical tests to ensure the API is secure.

Usage:
    python quick_validation.py
    python quick_validation.py --url http://localhost:8080
"""

import requests
import time
import sys

def test_security_headers(base_url):
    """Test essential security headers"""
    print("🔒 Testing Security Headers...")
    try:
        response = requests.get(f"{base_url}/health")
        headers = response.headers
        
        required_headers = [
            'x-content-type-options',
            'x-frame-options', 
            'x-xss-protection',
            'content-security-policy'
        ]
        
        missing = []
        for header in required_headers:
            if header not in headers:
                missing.append(header)
        
        if missing:
            print(f"❌ Missing security headers: {', '.join(missing)}")
            return False
        else:
            print("✅ All essential security headers present")
            return True
            
    except Exception as e:
        print(f"❌ Security headers test failed: {e}")
        return False

def test_csrf_protection(base_url):
    """Test CSRF protection"""
    print("🛡️ Testing CSRF Protection...")
    try:
        # Test without origin (should fail)
        response = requests.post(
            f"{base_url}/api/auth/register",
            json={"username": "csrf_test", "email": "csrf@test.com", "password": "Test123"},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 403:
            print("✅ CSRF protection is working")
            return True
        else:
            print(f"❌ CSRF protection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ CSRF test failed: {e}")
        return False

def test_authentication(base_url):
    """Test basic authentication"""
    print("🔑 Testing Authentication...")
    try:
        timestamp = int(time.time())
        
        # Register a test user
        response = requests.post(
            f"{base_url}/api/auth/register",
            json={
                "username": f"testuser_{timestamp}",
                "email": f"test_{timestamp}@test.com",
                "password": "SecurePass123"
            },
            headers={
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:3000'
            }
        )
        
        if response.status_code != 200:
            print(f"❌ User registration failed: {response.status_code}")
            return False
        
        # Login with the user
        response = requests.post(
            f"{base_url}/api/auth/login",
            json={
                "username_or_email": f"testuser_{timestamp}",
                "password": "SecurePass123"
            },
            headers={
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:3000'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data.get('data', {}):
                print("✅ Authentication is working")
                return True
            else:
                print("❌ No token in login response")
                return False
        else:
            print(f"❌ Login failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

def test_protected_endpoints(base_url):
    """Test that protected endpoints require authentication"""
    print("🔒 Testing Protected Endpoints...")
    try:
        response = requests.get(f"{base_url}/api/jabatans")
        
        if response.status_code == 401:
            print("✅ Protected endpoints require authentication")
            return True
        else:
            print(f"❌ Protected endpoints accessible without auth: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Protected endpoints test failed: {e}")
        return False

def test_input_validation(base_url):
    """Test basic input validation"""
    print("📝 Testing Input Validation...")
    try:
        # Test with invalid email
        response = requests.post(
            f"{base_url}/api/auth/register",
            json={
                "username": "testuser",
                "email": "invalid-email",
                "password": "SecurePass123"
            },
            headers={
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:3000'
            }
        )
        
        if response.status_code == 400:
            print("✅ Input validation is working")
            return True
        else:
            print(f"❌ Invalid input accepted: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Input validation test failed: {e}")
        return False

def main():
    """Run quick validation tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Quick Security & Authentication Validation')
    parser.add_argument('--url', default='http://localhost:8080', help='Base URL of the API')
    
    args = parser.parse_args()
    
    print("🚀 Quick Security & Authentication Validation")
    print("=" * 50)
    print(f"🌐 Target: {args.url}")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{args.url}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ Server health check failed: {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure the server is running: cargo run")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Security Headers", test_security_headers),
        ("CSRF Protection", test_csrf_protection),
        ("Authentication", test_authentication),
        ("Protected Endpoints", test_protected_endpoints),
        ("Input Validation", test_input_validation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func(args.url):
            passed += 1
        print()
    
    # Summary
    print("=" * 50)
    print("📊 Validation Summary")
    print("=" * 50)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🟢 EXCELLENT: All critical security features are working!")
        print("✅ API is ready for production deployment")
    elif passed >= total * 0.8:
        print("🟡 GOOD: Most security features working, review failed tests")
    else:
        print("🔴 CRITICAL: Major security issues detected!")
        print("❌ DO NOT deploy to production until issues are resolved")
    
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()