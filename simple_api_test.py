#!/usr/bin/env python3
"""
Simple Schemathesis API Testing for Karyawan & Kantor Management API
"""

import requests
import json
import time
import sys

# Configuration
API_BASE_URL = "http://localhost:8080"

def wait_for_api(max_attempts=10):
    """Wait for API to be ready"""
    print(f"🔄 Waiting for API at {API_BASE_URL}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ API is ready! (attempt {attempt + 1})")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"⏳ Attempt {attempt + 1}/{max_attempts} - waiting 2s...")
        time.sleep(2)
    
    print(f"❌ API not ready after {max_attempts} attempts")
    return False

def run_basic_tests():
    """Run basic API tests"""
    print("\n🧪 Running Basic API Tests")
    print("=" * 40)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Health check
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check - PASSED")
            tests_passed += 1
        else:
            print(f"❌ Health check - FAILED (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Health check - ERROR: {e}")
    
    # Test 2: Root endpoint
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint - PASSED")
            tests_passed += 1
        else:
            print(f"❌ Root endpoint - FAILED (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Root endpoint - ERROR: {e}")
    
    # Test 3: Get karyawans list
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/karyawans", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and isinstance(data.get("data"), list):
                print("✅ Karyawans list - PASSED")
                tests_passed += 1
            else:
                print(f"❌ Karyawans list - FAILED (invalid response format)")
        else:
            print(f"❌ Karyawans list - FAILED (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Karyawans list - ERROR: {e}")
    
    # Test 4: Get kantors list
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/kantors", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and isinstance(data.get("data"), list):
                print("✅ Kantors list - PASSED")
                tests_passed += 1
            else:
                print(f"❌ Kantors list - FAILED (invalid response format)")
        else:
            print(f"❌ Kantors list - FAILED (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Kantors list - ERROR: {e}")
    
    # Test 5: Get specific karyawan
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/karyawans/2", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("data"):
                print("✅ Get karyawan by ID - PASSED")
                tests_passed += 1
            else:
                print(f"❌ Get karyawan by ID - FAILED (invalid response)")
        else:
            print(f"❌ Get karyawan by ID - FAILED (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Get karyawan by ID - ERROR: {e}")
    
    # Test 6: Get karyawan with kantor
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/karyawans/2/with-kantor", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("data") and data["data"].get("kantor_nama"):
                print("✅ Get karyawan with kantor - PASSED")
                tests_passed += 1
            else:
                print(f"❌ Get karyawan with kantor - FAILED (no kantor info)")
        else:
            print(f"❌ Get karyawan with kantor - FAILED (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Get karyawan with kantor - ERROR: {e}")
    
    # Test 7: Invalid ID handling
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/karyawans/invalid", timeout=10)
        if response.status_code == 400:
            print("✅ Invalid ID handling - PASSED")
            tests_passed += 1
        else:
            print(f"❌ Invalid ID handling - FAILED (expected 400, got {response.status_code})")
    except Exception as e:
        print(f"❌ Invalid ID handling - ERROR: {e}")
    
    # Test 8: Create karyawan
    tests_total += 1
    try:
        # First, get a kantor ID
        kantor_response = requests.get(f"{API_BASE_URL}/api/kantors", timeout=10)
        if kantor_response.status_code == 200:
            kantors = kantor_response.json().get("data", [])
            if kantors:
                kantor_id = kantors[0]["id"]
                
                # Create test karyawan
                test_data = {
                    "nama": "Test Schemathesis User",
                    "posisi": "Tester",
                    "gaji": "5000000",
                    "kantor_id": str(kantor_id)
                }
                
                response = requests.post(
                    f"{API_BASE_URL}/api/karyawans",
                    json=test_data,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        print("✅ Create karyawan - PASSED")
                        tests_passed += 1
                    else:
                        print(f"❌ Create karyawan - FAILED (API error)")
                else:
                    print(f"❌ Create karyawan - FAILED (status: {response.status_code})")
            else:
                print("❌ Create karyawan - FAILED (no kantors available)")
        else:
            print("❌ Create karyawan - FAILED (cannot get kantors)")
    except Exception as e:
        print(f"❌ Create karyawan - ERROR: {e}")
    
    print(f"\n📊 Basic Tests: {tests_passed}/{tests_total} passed ({tests_passed/tests_total*100:.1f}%)")
    return tests_passed == tests_total

def run_validation_tests():
    """Run validation tests"""
    print("\n🔍 Running Validation Tests")
    print("=" * 40)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Invalid gaji (too low)
    tests_total += 1
    try:
        test_data = {
            "nama": "Test User",
            "posisi": "Tester",
            "gaji": "500000",  # Too low
            "kantor_id": "1"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/karyawans",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 400:
            print("✅ Gaji validation (too low) - PASSED")
            tests_passed += 1
        else:
            print(f"❌ Gaji validation (too low) - FAILED (expected 400, got {response.status_code})")
    except Exception as e:
        print(f"❌ Gaji validation (too low) - ERROR: {e}")
    
    # Test 2: Invalid nama (too short)
    tests_total += 1
    try:
        test_data = {
            "nama": "A",  # Too short
            "posisi": "Tester",
            "gaji": "5000000",
            "kantor_id": "1"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/karyawans",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 400:
            print("✅ Nama validation (too short) - PASSED")
            tests_passed += 1
        else:
            print(f"❌ Nama validation (too short) - FAILED (expected 400, got {response.status_code})")
    except Exception as e:
        print(f"❌ Nama validation (too short) - ERROR: {e}")
    
    # Test 3: Invalid kantor coordinates
    tests_total += 1
    try:
        test_data = {
            "nama": "Test Kantor",
            "alamat": "Test Address",
            "longitude": 200,  # Invalid - outside range
            "latitude": 0
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/kantors",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 400:
            print("✅ Coordinate validation (longitude) - PASSED")
            tests_passed += 1
        else:
            print(f"❌ Coordinate validation (longitude) - FAILED (expected 400, got {response.status_code})")
    except Exception as e:
        print(f"❌ Coordinate validation (longitude) - ERROR: {e}")
    
    print(f"\n📊 Validation Tests: {tests_passed}/{tests_total} passed ({tests_passed/tests_total*100:.1f}%)")
    return tests_passed == tests_total

def run_edge_case_tests():
    """Run edge case tests"""
    print("\n🎯 Running Edge Case Tests")
    print("=" * 40)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Non-existent ID
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/karyawans/99999", timeout=10)
        if response.status_code == 404:
            print("✅ Non-existent ID - PASSED")
            tests_passed += 1
        else:
            print(f"❌ Non-existent ID - FAILED (expected 404, got {response.status_code})")
    except Exception as e:
        print(f"❌ Non-existent ID - ERROR: {e}")
    
    # Test 2: Negative ID
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/karyawans/-1", timeout=10)
        if response.status_code == 400:
            print("✅ Negative ID - PASSED")
            tests_passed += 1
        else:
            print(f"❌ Negative ID - FAILED (expected 400, got {response.status_code})")
    except Exception as e:
        print(f"❌ Negative ID - ERROR: {e}")
    
    # Test 3: Zero ID
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/karyawans/0", timeout=10)
        if response.status_code == 400:
            print("✅ Zero ID - PASSED")
            tests_passed += 1
        else:
            print(f"❌ Zero ID - FAILED (expected 400, got {response.status_code})")
    except Exception as e:
        print(f"❌ Zero ID - ERROR: {e}")
    
    print(f"\n📊 Edge Case Tests: {tests_passed}/{tests_total} passed ({tests_passed/tests_total*100:.1f}%)")
    return tests_passed == tests_total

if __name__ == "__main__":
    print("🧪 Simplified Schemathesis-style API Testing")
    print("=" * 50)
    
    # Wait for API
    if not wait_for_api():
        print("❌ API not available - exiting")
        sys.exit(1)
    
    # Run all test suites
    basic_success = run_basic_tests()
    validation_success = run_validation_tests()
    edge_case_success = run_edge_case_tests()
    
    # Final result
    overall_success = basic_success and validation_success and edge_case_success
    
    print(f"\n🏁 Final Result:")
    print(f"   Basic Tests: {'✅ PASSED' if basic_success else '❌ FAILED'}")
    print(f"   Validation Tests: {'✅ PASSED' if validation_success else '❌ FAILED'}")
    print(f"   Edge Case Tests: {'✅ PASSED' if edge_case_success else '❌ FAILED'}")
    print(f"   Overall: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    # Exit with appropriate code
    sys.exit(0 if overall_success else 1)