#!/usr/bin/env python3
"""
Corrected API Testing for Karyawan & Kantor Management API
This version properly handles the API's JSON-based error responses
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

def check_api_error(response, test_name):
    """Check if API response indicates an error (JSON-based error handling)"""
    if response.status_code != 200:
        return True, f"HTTP {response.status_code}"
    
    try:
        data = response.json()
        if not data.get("success", True):
            return True, f"API Error: {data.get('message', 'Unknown error')}"
    except:
        pass
    
    return False, "Success"

def run_comprehensive_tests():
    """Run comprehensive API tests with proper error handling"""
    print("\n🧪 Running Comprehensive API Tests")
    print("=" * 50)
    
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
    
    # Test 7: Invalid ID handling (JSON-based error)
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/karyawans/invalid", timeout=10)
        is_error, error_msg = check_api_error(response, "Invalid ID")
        if is_error:
            print("✅ Invalid ID handling - PASSED (JSON error response)")
            tests_passed += 1
        else:
            print(f"❌ Invalid ID handling - FAILED (expected error response)")
    except Exception as e:
        print(f"❌ Invalid ID handling - ERROR: {e}")
    
    # Test 8: Create karyawan with valid data
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
                    "nama": "Test Comprehensive User",
                    "posisi": "API Tester",
                    "gaji": "7500000",
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
                        print("✅ Create karyawan (valid) - PASSED")
                        tests_passed += 1
                    else:
                        print(f"❌ Create karyawan (valid) - FAILED: {data.get('message')}")
                else:
                    print(f"❌ Create karyawan (valid) - FAILED (status: {response.status_code})")
            else:
                print("❌ Create karyawan (valid) - FAILED (no kantors available)")
        else:
            print("❌ Create karyawan (valid) - FAILED (cannot get kantors)")
    except Exception as e:
        print(f"❌ Create karyawan (valid) - ERROR: {e}")
    
    print(f"\n📊 Comprehensive Tests: {tests_passed}/{tests_total} passed ({tests_passed/tests_total*100:.1f}%)")
    return tests_passed, tests_total

def run_validation_tests():
    """Run validation tests with JSON error checking"""
    print("\n🔍 Running Validation Tests (JSON Error Format)")
    print("=" * 50)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Invalid gaji (too low) - should return JSON error
    tests_total += 1
    try:
        test_data = {
            "nama": "Test User",
            "posisi": "Tester",
            "gaji": "500000",  # Too low (minimum 1,000,000)
            "kantor_id": "1"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/karyawans",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        is_error, error_msg = check_api_error(response, "Low gaji")
        if is_error:
            print(f"✅ Gaji validation (too low) - PASSED: {error_msg}")
            tests_passed += 1
        else:
            print(f"❌ Gaji validation (too low) - FAILED (should reject low gaji)")
    except Exception as e:
        print(f"❌ Gaji validation (too low) - ERROR: {e}")
    
    # Test 2: Invalid nama (too short) - should return JSON error
    tests_total += 1
    try:
        test_data = {
            "nama": "A",  # Too short (minimum 2 chars)
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
        
        is_error, error_msg = check_api_error(response, "Short nama")
        if is_error:
            print(f"✅ Nama validation (too short) - PASSED: {error_msg}")
            tests_passed += 1
        else:
            print(f"❌ Nama validation (too short) - FAILED (should reject short nama)")
    except Exception as e:
        print(f"❌ Nama validation (too short) - ERROR: {e}")
    
    # Test 3: Invalid kantor coordinates - should return JSON error
    tests_total += 1
    try:
        test_data = {
            "nama": "Test Kantor Invalid",
            "alamat": "Test Address for Invalid Coordinates",
            "longitude": 200,  # Invalid - outside range (-180 to 180)
            "latitude": 0
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/kantors",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        is_error, error_msg = check_api_error(response, "Invalid longitude")
        if is_error:
            print(f"✅ Coordinate validation (longitude) - PASSED: {error_msg}")
            tests_passed += 1
        else:
            print(f"❌ Coordinate validation (longitude) - FAILED (should reject invalid longitude)")
    except Exception as e:
        print(f"❌ Coordinate validation (longitude) - ERROR: {e}")
    
    # Test 4: Invalid kantor_id reference
    tests_total += 1
    try:
        test_data = {
            "nama": "Test User Invalid Kantor",
            "posisi": "Tester",
            "gaji": "5000000",
            "kantor_id": "99999"  # Non-existent kantor
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/karyawans",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        is_error, error_msg = check_api_error(response, "Invalid kantor_id")
        if is_error:
            print(f"✅ Foreign key validation - PASSED: {error_msg}")
            tests_passed += 1
        else:
            print(f"❌ Foreign key validation - FAILED (should reject invalid kantor_id)")
    except Exception as e:
        print(f"❌ Foreign key validation - ERROR: {e}")
    
    print(f"\n📊 Validation Tests: {tests_passed}/{tests_total} passed ({tests_passed/tests_total*100:.1f}%)")
    return tests_passed, tests_total

def run_edge_case_tests():
    """Run edge case tests with JSON error checking"""
    print("\n🎯 Running Edge Case Tests (JSON Error Format)")
    print("=" * 50)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Non-existent ID - should return JSON error or 404
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/karyawans/99999", timeout=10)
        is_error, error_msg = check_api_error(response, "Non-existent ID")
        if is_error or response.status_code == 404:
            print(f"✅ Non-existent ID - PASSED: {error_msg}")
            tests_passed += 1
        else:
            print(f"❌ Non-existent ID - FAILED (should return error)")
    except Exception as e:
        print(f"❌ Non-existent ID - ERROR: {e}")
    
    # Test 2: Negative ID - should return JSON error
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/karyawans/-1", timeout=10)
        is_error, error_msg = check_api_error(response, "Negative ID")
        if is_error:
            print(f"✅ Negative ID - PASSED: {error_msg}")
            tests_passed += 1
        else:
            print(f"❌ Negative ID - FAILED (should reject negative ID)")
    except Exception as e:
        print(f"❌ Negative ID - ERROR: {e}")
    
    # Test 3: Zero ID - should return JSON error
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/karyawans/0", timeout=10)
        is_error, error_msg = check_api_error(response, "Zero ID")
        if is_error:
            print(f"✅ Zero ID - PASSED: {error_msg}")
            tests_passed += 1
        else:
            print(f"❌ Zero ID - FAILED (should reject zero ID)")
    except Exception as e:
        print(f"❌ Zero ID - ERROR: {e}")
    
    # Test 4: Very large gaji (boundary test)
    tests_total += 1
    try:
        test_data = {
            "nama": "Test High Salary",
            "posisi": "CEO",
            "gaji": "150000000",  # Above maximum (100,000,000)
            "kantor_id": "1"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/karyawans",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        is_error, error_msg = check_api_error(response, "High gaji")
        if is_error:
            print(f"✅ High gaji boundary test - PASSED: {error_msg}")
            tests_passed += 1
        else:
            print(f"❌ High gaji boundary test - FAILED (should reject very high gaji)")
    except Exception as e:
        print(f"❌ High gaji boundary test - ERROR: {e}")
    
    print(f"\n📊 Edge Case Tests: {tests_passed}/{tests_total} passed ({tests_passed/tests_total*100:.1f}%)")
    return tests_passed, tests_total

if __name__ == "__main__":
    print("🧪 Comprehensive API Testing (Schemathesis-style)")
    print("=" * 55)
    print("📋 This test correctly handles JSON-based error responses")
    
    # Wait for API
    if not wait_for_api():
        print("❌ API not available - exiting")
        sys.exit(1)
    
    # Run all test suites
    comp_passed, comp_total = run_comprehensive_tests()
    val_passed, val_total = run_validation_tests()
    edge_passed, edge_total = run_edge_case_tests()
    
    # Calculate totals
    total_passed = comp_passed + val_passed + edge_passed
    total_tests = comp_total + val_total + edge_total
    success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    # Final result
    print(f"\n🏁 Final Test Summary:")
    print(f"   Comprehensive Tests: {comp_passed}/{comp_total} passed")
    print(f"   Validation Tests: {val_passed}/{val_total} passed")
    print(f"   Edge Case Tests: {edge_passed}/{edge_total} passed")
    print(f"   Overall: {total_passed}/{total_tests} passed ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print(f"   Status: ✅ EXCELLENT ({success_rate:.1f}% pass rate)")
    elif success_rate >= 60:
        print(f"   Status: ⚠️  GOOD ({success_rate:.1f}% pass rate)")
    else:
        print(f"   Status: ❌ NEEDS IMPROVEMENT ({success_rate:.1f}% pass rate)")
    
    # Exit with appropriate code
    sys.exit(0 if success_rate >= 80 else 1)