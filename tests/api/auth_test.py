#!/usr/bin/env python3
"""
JWT Authentication Test Script
Tests the registration, login, and protected endpoint functionality
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8080"

def test_registration():
    """Test user registration"""
    print("🔍 Testing user registration...")
    
    # Use a unique username with timestamp
    import time
    timestamp = int(time.time())
    
    registration_data = {
        "username": f"testuser{timestamp}",
        "email": f"test{timestamp}@example.com",
        "password": "password123",
        "full_name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=registration_data)
    
    if response.status_code == 201:
        print("✅ Registration successful")
        return registration_data  # Return data for login test
    else:
        print(f"❌ Registration failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_login(user_data=None):
    """Test user login and get JWT token"""
    print("🔍 Testing user login...")
    
    if user_data:
        login_data = {
            "username_or_email": user_data["username"],
            "password": user_data["password"]
        }
    else:
        login_data = {
            "username_or_email": "testuser",
            "password": "password123"
        }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("data", {}).get("token")
        if token:
            print("✅ Login successful, token received")
            return token
        else:
            print("❌ Login successful but no token received")
            return None
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_protected_endpoint(token):
    """Test protected /me endpoint"""
    print("🔍 Testing protected endpoint (/me)...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/api/user/me", headers=headers)
    
    if response.status_code == 200:
        print("✅ Protected endpoint accessible with valid token")
        user_data = response.json()
        print(f"User data: {json.dumps(user_data, indent=2)}")
        return True
    else:
        print(f"❌ Protected endpoint failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_protected_endpoint_without_token():
    """Test protected endpoint without token"""
    print("🔍 Testing protected endpoint without token...")
    
    response = requests.get(f"{BASE_URL}/api/user/me")
    
    if response.status_code == 401:
        print("✅ Protected endpoint properly rejected request without token")
        return True
    else:
        print(f"❌ Protected endpoint should have returned 401, got: {response.status_code}")
        return False

def main():
    print("🚀 Starting JWT Authentication Tests")
    print("-" * 50)
    
    # Test registration
    user_data = test_registration()
    if not user_data:
        # Maybe user already exists, try to continue with default login
        print("⚠️  Registration failed, trying with default credentials...")
        user_data = None
    
    # Test login
    token = test_login(user_data)
    if not token:
        print("❌ Cannot continue without token")
        sys.exit(1)
    
    # Test protected endpoint with token
    test_protected_endpoint(token)
    
    # Test protected endpoint without token
    test_protected_endpoint_without_token()
    
    print("-" * 50)
    print("🎉 JWT Authentication tests completed!")

if __name__ == "__main__":
    main()