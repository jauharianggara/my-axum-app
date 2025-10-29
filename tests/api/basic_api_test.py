#!/usr/bin/env python3
"""
Basic API Functionality Tests
Tests core API endpoints and basic functionality
"""

import requests
import json
import time
import sys

API_BASE_URL = "http://localhost:8080"
API_BASE = f"{API_BASE_URL}/api"

class BasicAPITester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test(self, name, test_func):
        """Run a single test"""
        try:
            result = test_func()
            if result:
                print(f"✅ {name}")
                self.passed += 1
            else:
                print(f"❌ {name}")
                self.failed += 1
        except Exception as e:
            print(f"❌ {name} - ERROR: {str(e)}")
            self.failed += 1
    
    def summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        if total == 0:
            return False
        
        print(f"\n📊 BASIC API TEST SUMMARY")
        print(f"{'='*40}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total:  {total}")
        print(f"Success Rate: {(self.passed/total)*100:.1f}%")
        
        return self.failed == 0

def test_health_endpoint():
    """Test health endpoint"""
    response = requests.get(f"{API_BASE_URL}/health", timeout=5)
    return response.status_code == 200

def test_root_endpoint():
    """Test root endpoint"""
    response = requests.get(f"{API_BASE_URL}/", timeout=5)
    return response.status_code == 200

def test_karyawan_list():
    """Test karyawan list endpoint"""
    response = requests.get(f"{API_BASE}/karyawans", timeout=5)
    if response.status_code != 200:
        return False
    
    data = response.json()
    return data.get("success") and isinstance(data.get("data"), list)

def test_kantor_list():
    """Test kantor list endpoint"""
    response = requests.get(f"{API_BASE}/kantors", timeout=5)
    if response.status_code != 200:
        return False
    
    data = response.json()
    return data.get("success") and isinstance(data.get("data"), list)

def test_karyawan_by_id():
    """Test get karyawan by ID"""
    # Get list first to find a valid ID
    response = requests.get(f"{API_BASE}/karyawans", timeout=5)
    if response.status_code != 200:
        return False
    
    data = response.json()
    karyawans = data.get("data", [])
    if not karyawans:
        return False  # No karyawans to test with
    
    # Test with first karyawan ID
    karyawan_id = karyawans[0]["id"]
    response = requests.get(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
    if response.status_code != 200:
        return False
    
    data = response.json()
    return data.get("success") and data.get("data")

def test_karyawan_with_kantor():
    """Test get karyawan with kantor info"""
    # Get list first to find a valid ID
    response = requests.get(f"{API_BASE}/karyawans", timeout=5)
    if response.status_code != 200:
        return False
    
    data = response.json()
    karyawans = data.get("data", [])
    if not karyawans:
        return False
    
    # Test with first karyawan ID
    karyawan_id = karyawans[0]["id"]
    response = requests.get(f"{API_BASE}/karyawans/{karyawan_id}/with-kantor", timeout=5)
    if response.status_code != 200:
        return False
    
    data = response.json()
    return data.get("success") and data.get("data")

def test_invalid_id_handling():
    """Test invalid ID handling"""
    response = requests.get(f"{API_BASE}/karyawans/invalid", timeout=5)
    return response.status_code == 400

def test_nonexistent_id():
    """Test non-existent ID"""
    response = requests.get(f"{API_BASE}/karyawans/99999", timeout=5)
    return response.status_code == 404

def run_tests():
    """Run all basic API tests"""
    print("🧪 BASIC API FUNCTIONALITY TESTS")
    print("="*50)
    
    tester = BasicAPITester()
    
    # Run tests
    tester.test("Health endpoint", test_health_endpoint)
    tester.test("Root endpoint", test_root_endpoint)
    tester.test("Karyawan list", test_karyawan_list)
    tester.test("Kantor list", test_kantor_list)
    tester.test("Karyawan by ID", test_karyawan_by_id)
    tester.test("Karyawan with kantor", test_karyawan_with_kantor)
    tester.test("Invalid ID handling", test_invalid_id_handling)
    tester.test("Non-existent ID", test_nonexistent_id)
    
    return tester.summary()

if __name__ == "__main__":
    try:
        # Check server availability
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server not available")
            sys.exit(1)
        
        success = run_tests()
        sys.exit(0 if success else 1)
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server at http://localhost:8080")
        print("   Please start the server first: cargo run")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test suite failed: {str(e)}")
        sys.exit(1)