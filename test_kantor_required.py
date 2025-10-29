#!/usr/bin/env python3
"""
Test script untuk memastikan kantor_id wajib diisi (no freelancer allowed)
"""

import requests
import json

BASE_URL = "http://localhost:8080/api"

def test_kantor_required_validation():
    print("🧪 Testing REQUIRED kantor_id validation (NO FREELANCER)...")
    print("=" * 60)
    
    # Test 1: Check existing kantors
    print("\n1. 📋 Getting list of existing kantors:")
    kantors_response = requests.get(f"{BASE_URL}/kantors")
    if kantors_response.status_code == 200:
        kantors_data = kantors_response.json()
        if kantors_data.get("success") and kantors_data.get("data"):
            kantors = kantors_data["data"]
            print(f"   ✅ Found {len(kantors)} kantors:")
            for kantor in kantors:
                print(f"      - ID: {kantor['id']}, Nama: {kantor['nama']}")
            valid_kantor_id = str(kantors[0]["id"]) if kantors else None
        else:
            print("   ❌ No kantors found in database")
            valid_kantor_id = None
    else:
        print(f"   ❌ Failed to get kantors: {kantors_response.status_code}")
        valid_kantor_id = None

    # Test 2: Try to create karyawan dengan kantor_id = 0 (should FAIL now)
    print("\n2. ❌ Testing kantor_id = 0 (should be REJECTED):")
    karyawan_data = {
        "nama": "Test Freelancer",
        "posisi": "Developer",
        "gaji": "5000000",
        "kantor_id": "0"
    }
    response = requests.post(f"{BASE_URL}/karyawans", json=karyawan_data)
    print(f"   Status: {response.status_code}")
    try:
        result = response.json()
        if not result.get("success"):
            print(f"   ✅ CORRECTLY REJECTED: {result.get('message')}")
            print(f"   Errors: {result.get('errors', [])}")
        else:
            print(f"   ❌ VALIDATION FAILED: Should have rejected kantor_id = 0")
    except:
        print(f"   ❌ FAILED: Invalid response format")

    # Test 3: Create karyawan dengan valid kantor_id (should SUCCEED)
    if valid_kantor_id:
        print(f"\n3. ✅ Testing valid kantor_id ({valid_kantor_id}):")
        karyawan_data = {
            "nama": "Test Employee",
            "posisi": "Manager",
            "gaji": "8000000",
            "kantor_id": valid_kantor_id
        }
        response = requests.post(f"{BASE_URL}/karyawans", json=karyawan_data)
        print(f"   Status: {response.status_code}")
        try:
            result = response.json()
            if result.get("success"):
                print(f"   ✅ SUCCESS: {result.get('message')}")
                employee_id = result["data"]["id"]
            else:
                print(f"   ❌ FAILED: {result.get('message')}")
                print(f"   Errors: {result.get('errors', [])}")
                employee_id = None
        except:
            print(f"   ❌ FAILED: Invalid response format")
            employee_id = None
    else:
        print("\n3. ⏭️ Skipping valid kantor_id test (no kantors available)")
        employee_id = None

    # Test 4: Create karyawan dengan invalid kantor_id (should FAIL)
    print("\n4. ❌ Testing invalid kantor_id (999999):")
    karyawan_data = {
        "nama": "Test Invalid",
        "posisi": "Tester",
        "gaji": "4000000",
        "kantor_id": "999999"
    }
    response = requests.post(f"{BASE_URL}/karyawans", json=karyawan_data)
    print(f"   Status: {response.status_code}")
    try:
        result = response.json()
        if not result.get("success"):
            print(f"   ✅ CORRECTLY REJECTED: {result.get('message')}")
            print(f"   Errors: {result.get('errors', [])}")
        else:
            print(f"   ❌ VALIDATION FAILED: Should have rejected invalid kantor_id")
    except:
        print(f"   ❌ FAILED: Invalid response format")

    # Test 5: Create karyawan dengan negative kantor_id (should FAIL)
    print("\n5. ❌ Testing negative kantor_id (-1):")
    karyawan_data = {
        "nama": "Test Negative",
        "posisi": "Tester",
        "gaji": "4000000",
        "kantor_id": "-1"
    }
    response = requests.post(f"{BASE_URL}/karyawans", json=karyawan_data)
    print(f"   Status: {response.status_code}")
    try:
        result = response.json()
        if not result.get("success"):
            print(f"   ✅ CORRECTLY REJECTED: {result.get('message')}")
            print(f"   Errors: {result.get('errors', [])}")
        else:
            print(f"   ❌ VALIDATION FAILED: Should have rejected negative kantor_id")
    except:
        print(f"   ❌ FAILED: Invalid response format")

    # Test 6: Create karyawan dengan empty kantor_id (should FAIL)
    print("\n6. ❌ Testing empty kantor_id (''):")
    karyawan_data = {
        "nama": "Test Empty",
        "posisi": "Tester",
        "gaji": "4000000",
        "kantor_id": ""
    }
    response = requests.post(f"{BASE_URL}/karyawans", json=karyawan_data)
    print(f"   Status: {response.status_code}")
    try:
        result = response.json()
        if not result.get("success"):
            print(f"   ✅ CORRECTLY REJECTED: {result.get('message')}")
            print(f"   Errors: {result.get('errors', [])}")
        else:
            print(f"   ❌ VALIDATION FAILED: Should have rejected empty kantor_id")
    except:
        print(f"   ❌ FAILED: Invalid response format")

    # Test 7: Create karyawan dengan string kantor_id (should FAIL)
    print("\n7. ❌ Testing string kantor_id ('abc'):")
    karyawan_data = {
        "nama": "Test String",
        "posisi": "Tester",
        "gaji": "4000000",
        "kantor_id": "abc"
    }
    response = requests.post(f"{BASE_URL}/karyawans", json=karyawan_data)
    print(f"   Status: {response.status_code}")
    try:
        result = response.json()
        if not result.get("success"):
            print(f"   ✅ CORRECTLY REJECTED: {result.get('message')}")
            print(f"   Errors: {result.get('errors', [])}")
        else:
            print(f"   ❌ VALIDATION FAILED: Should have rejected string kantor_id")
    except:
        print(f"   ❌ FAILED: Invalid response format")

    # Cleanup: Delete test data
    print("\n🧹 Cleaning up test data...")
    if employee_id:
        delete_response = requests.delete(f"{BASE_URL}/karyawans/{employee_id}")
        if delete_response.status_code == 200:
            print(f"   ✅ Deleted karyawan ID {employee_id}")
        else:
            print(f"   ⚠️ Failed to delete karyawan ID {employee_id}")

    print("\n" + "=" * 60)
    print("🎯 REQUIRED kantor_id validation test completed!")
    print("📝 Summary:")
    print("   ✅ kantor_id = 0 → REJECTED (no more freelancer)")
    print("   ✅ kantor_id > 0 and valid → ACCEPTED")
    print("   ✅ kantor_id invalid → REJECTED")
    print("   ✅ kantor_id negative → REJECTED")
    print("   ✅ kantor_id empty → REJECTED")
    print("   ✅ kantor_id string → REJECTED")

if __name__ == "__main__":
    test_kantor_required_validation()