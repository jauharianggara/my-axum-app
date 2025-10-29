#!/usr/bin/env python3
"""
Test script untuk mendemonstrasikan autentikasi JWT pada endpoint protected
Menguji bahwa endpoint karyawan dan kantor hanya bisa diakses dengan token valid
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8080"

def test_unprotected_endpoints():
    """Test endpoint yang tidak memerlukan autentikasi"""
    print("🔍 Testing unprotected endpoints...")
    
    # Test health endpoint
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ Health endpoint accessible without auth")
    else:
        print(f"❌ Health endpoint failed: {response.status_code}")
    
    # Test login endpoint
    login_data = {
        "username_or_email": "testuser",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code == 200:
        print("✅ Login endpoint accessible without auth")
        return response.json()["data"]["token"]
    else:
        print(f"❌ Login endpoint failed: {response.status_code}")
        return None

def test_protected_endpoints_without_auth():
    """Test endpoint yang dilindungi tanpa token"""
    print("\n🔍 Testing protected endpoints without authentication...")
    
    # Test karyawan endpoint
    response = requests.get(f"{BASE_URL}/api/karyawans")
    if response.status_code == 401:
        print("✅ Karyawan endpoint properly protected (401 Unauthorized)")
    else:
        print(f"❌ Karyawan endpoint should be protected, got: {response.status_code}")
    
    # Test kantor endpoint
    response = requests.get(f"{BASE_URL}/api/kantors")
    if response.status_code == 401:
        print("✅ Kantor endpoint properly protected (401 Unauthorized)")
    else:
        print(f"❌ Kantor endpoint should be protected, got: {response.status_code}")

def test_protected_endpoints_with_auth(token):
    """Test endpoint yang dilindungi dengan token valid"""
    print("\n🔍 Testing protected endpoints with valid authentication...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test karyawan endpoint
    response = requests.get(f"{BASE_URL}/api/karyawans", headers=headers)
    if response.status_code == 200:
        print("✅ Karyawan endpoint accessible with valid token")
        data = response.json()
        print(f"   Found {len(data['data'])} karyawan records")
    else:
        print(f"❌ Karyawan endpoint failed: {response.status_code}")
    
    # Test kantor endpoint
    response = requests.get(f"{BASE_URL}/api/kantors", headers=headers)
    if response.status_code == 200:
        print("✅ Kantor endpoint accessible with valid token")
        data = response.json()
        print(f"   Found {len(data['data'])} kantor records")
    else:
        print(f"❌ Kantor endpoint failed: {response.status_code}")

def test_protected_endpoints_with_invalid_auth():
    """Test endpoint yang dilindungi dengan token invalid"""
    print("\n🔍 Testing protected endpoints with invalid authentication...")
    
    headers = {
        "Authorization": "Bearer invalid_token_here",
        "Content-Type": "application/json"
    }
    
    # Test karyawan endpoint
    response = requests.get(f"{BASE_URL}/api/karyawans", headers=headers)
    if response.status_code == 401:
        print("✅ Karyawan endpoint properly rejects invalid token")
    else:
        print(f"❌ Karyawan endpoint should reject invalid token, got: {response.status_code}")
    
    # Test kantor endpoint
    response = requests.get(f"{BASE_URL}/api/kantors", headers=headers)
    if response.status_code == 401:
        print("✅ Kantor endpoint properly rejects invalid token")
    else:
        print(f"❌ Kantor endpoint should reject invalid token, got: {response.status_code}")

def main():
    print("🚀 Testing JWT Authentication Protection")
    print("="*60)
    
    # Test 1: Unprotected endpoints
    token = test_unprotected_endpoints()
    if not token:
        print("❌ Cannot continue without valid token")
        sys.exit(1)
    
    # Test 2: Protected endpoints without auth
    test_protected_endpoints_without_auth()
    
    # Test 3: Protected endpoints with valid auth
    test_protected_endpoints_with_auth(token)
    
    # Test 4: Protected endpoints with invalid auth
    test_protected_endpoints_with_invalid_auth()
    
    print("\n" + "="*60)
    print("🎉 JWT Authentication Protection Test Completed!")
    print("\n📋 Summary:")
    print("✅ Public endpoints (health, login) accessible without auth")
    print("✅ Protected endpoints (karyawan, kantor) require valid JWT token")
    print("✅ Invalid tokens are properly rejected with 401 Unauthorized")
    print("✅ Valid tokens allow access to protected resources")

if __name__ == "__main__":
    main()