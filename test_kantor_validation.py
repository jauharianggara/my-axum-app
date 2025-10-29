#!/usr/bin/env python3
"""
Test script untuk menguji validasi kantor_id
"""

import requests
import json

BASE_URL = "http://localhost:8080/api"

def test_kantor_validation():
    print("🧪 Testing kantor_id validation...")
    print("=" * 50)
    
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

    # Test 2: Create karyawan dengan kantor_id = 0 (freelancer)
    print("\n2. 👤 Testing freelancer (kantor_id = 0):")
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
        if result.get("success"):
            print(f"   ✅ SUCCESS: {result.get('message')}")
            freelancer_id = result["data"]["id"]
        else:
            print(f"   ❌ FAILED: {result.get('message')}")
            print(f"   Errors: {result.get('errors', [])}")
            freelancer_id = None
    except:
        print(f"   ❌ FAILED: Invalid response format")
        freelancer_id = None

    # Test 3: Create karyawan dengan valid kantor_id
    if valid_kantor_id:
        print(f"\n3. 🏢 Testing valid kantor_id ({valid_kantor_id}):")
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

    # Test 4: Create karyawan dengan invalid kantor_id (not exists)
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
            print(f"   ✅ VALIDATION WORKING: {result.get('message')}")
            print(f"   Errors: {result.get('errors', [])}")
        else:
            print(f"   ❌ VALIDATION FAILED: Should have rejected invalid kantor_id")
    except:
        print(f"   ❌ FAILED: Invalid response format")

    # Test 5: Create karyawan dengan negative kantor_id
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
            print(f"   ✅ VALIDATION WORKING: {result.get('message')}")
            print(f"   Errors: {result.get('errors', [])}")
        else:
            print(f"   ❌ VALIDATION FAILED: Should have rejected negative kantor_id")
    except:
        print(f"   ❌ FAILED: Invalid response format")

    # Test 6: Create karyawan dengan invalid string kantor_id
    print("\n6. ❌ Testing invalid string kantor_id ('abc'):")
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
            print(f"   ✅ VALIDATION WORKING: {result.get('message')}")
            print(f"   Errors: {result.get('errors', [])}")
        else:
            print(f"   ❌ VALIDATION FAILED: Should have rejected string kantor_id")
    except:
        print(f"   ❌ FAILED: Invalid response format")

    # Cleanup: Delete test data
    print("\n🧹 Cleaning up test data...")
    cleanup_ids = []
    if freelancer_id:
        cleanup_ids.append(freelancer_id)
    if employee_id:
        cleanup_ids.append(employee_id)
    
    for test_id in cleanup_ids:
        delete_response = requests.delete(f"{BASE_URL}/karyawans/{test_id}")
        if delete_response.status_code == 200:
            print(f"   ✅ Deleted karyawan ID {test_id}")
        else:
            print(f"   ⚠️ Failed to delete karyawan ID {test_id}")

    print("\n" + "=" * 50)
    print("🎯 Kantor ID validation test completed!")

if __name__ == "__main__":
    test_kantor_validation()