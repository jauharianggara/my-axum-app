#!/usr/bin/env python3
"""
Karyawan CRUD Operations Test
Tests Create, Read, Update, Delete operations for Karyawan
"""

import requests
import json
import sys

API_BASE_URL = "http://localhost:8080"
API_BASE = f"{API_BASE_URL}/api"

class KaryawanCRUDTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.created_ids = []
    
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
            return result
        except Exception as e:
            print(f"❌ {name} - ERROR: {str(e)}")
            self.failed += 1
            return False
    
    def cleanup(self):
        """Clean up created karyawans"""
        print(f"\n🧹 Cleaning up {len(self.created_ids)} test karyawans...")
        for karyawan_id in self.created_ids:
            try:
                requests.delete(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
            except:
                pass
    
    def summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        if total == 0:
            return False
        
        print(f"\n📊 KARYAWAN CRUD TEST SUMMARY")
        print(f"{'='*40}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total:  {total}")
        print(f"Success Rate: {(self.passed/total)*100:.1f}%")
        
        return self.failed == 0

def get_valid_kantor_id():
    """Get a valid kantor ID for testing"""
    response = requests.get(f"{API_BASE}/kantors", timeout=5)
    if response.status_code != 200:
        return None
    
    data = response.json()
    kantors = data.get("data", [])
    return kantors[0]["id"] if kantors else None

def test_create_karyawan(tester):
    """Test creating a new karyawan"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    test_data = {
        "nama": "Test Karyawan CRUD",
        "posisi": "Software Tester",
        "gaji": "5000000",
        "kantor_id": str(kantor_id)
    }
    
    response = requests.post(
        f"{API_BASE}/karyawans",
        json=test_data,
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    
    if response.status_code != 200:
        return False
    
    data = response.json()
    if not data.get("success"):
        return False
    
    # Store ID for cleanup
    karyawan_id = data.get("data", {}).get("id")
    if karyawan_id:
        tester.created_ids.append(karyawan_id)
    
    return True

def test_read_karyawan(tester):
    """Test reading karyawan data"""
    if not tester.created_ids:
        return False
    
    karyawan_id = tester.created_ids[0]
    response = requests.get(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
    
    if response.status_code != 200:
        return False
    
    data = response.json()
    return data.get("success") and data.get("data", {}).get("nama") == "Test Karyawan CRUD"

def test_update_karyawan(tester):
    """Test updating karyawan data"""
    if not tester.created_ids:
        return False
    
    karyawan_id = tester.created_ids[0]
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    update_data = {
        "nama": "Updated Test Karyawan",
        "posisi": "Senior Tester",
        "gaji": "6000000",
        "kantor_id": str(kantor_id)
    }
    
    response = requests.put(
        f"{API_BASE}/karyawans/{karyawan_id}",
        json=update_data,
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    
    if response.status_code != 200:
        return False
    
    data = response.json()
    if not data.get("success"):
        return False
    
    # Verify update
    get_response = requests.get(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
    if get_response.status_code != 200:
        return False
    
    get_data = get_response.json()
    updated_karyawan = get_data.get("data", {})
    
    return (updated_karyawan.get("nama") == "Updated Test Karyawan" and
            updated_karyawan.get("posisi") == "Senior Tester")

def test_delete_karyawan(tester):
    """Test deleting karyawan"""
    if not tester.created_ids:
        return False
    
    karyawan_id = tester.created_ids.pop()  # Remove from list so it won't be cleaned up again
    
    response = requests.delete(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
    
    if response.status_code != 200:
        return False
    
    # Verify deletion
    get_response = requests.get(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
    return get_response.status_code == 404

def test_create_with_invalid_data(tester):
    """Test creating karyawan with invalid data"""
    invalid_cases = [
        {
            "nama": "A",  # Too short
            "posisi": "Tester",
            "gaji": "5000000",
            "kantor_id": "1"
        },
        {
            "nama": "Test User",
            "posisi": "T",  # Too short
            "gaji": "5000000",
            "kantor_id": "1"
        },
        {
            "nama": "Test User",
            "posisi": "Tester",
            "gaji": "500000",  # Too low
            "kantor_id": "1"
        },
        {
            "nama": "Test User",
            "posisi": "Tester",
            "gaji": "5000000",
            "kantor_id": "99999"  # Non-existent kantor
        }
    ]
    
    for i, invalid_data in enumerate(invalid_cases):
        response = requests.post(
            f"{API_BASE}/karyawans",
            json=invalid_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code != 400:
            print(f"   Invalid case {i+1} should return 400 but got {response.status_code}")
            return False
    
    return True

def test_update_nonexistent(tester):
    """Test updating non-existent karyawan"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    update_data = {
        "nama": "Non-existent",
        "posisi": "Tester",
        "gaji": "5000000",
        "kantor_id": str(kantor_id)
    }
    
    response = requests.put(
        f"{API_BASE}/karyawans/99999",
        json=update_data,
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    
    return response.status_code == 404

def test_delete_nonexistent(tester):
    """Test deleting non-existent karyawan"""
    response = requests.delete(f"{API_BASE}/karyawans/99999", timeout=5)
    return response.status_code == 404

def run_tests():
    """Run all karyawan CRUD tests"""
    print("🧪 KARYAWAN CRUD OPERATIONS TESTS")
    print("="*50)
    
    tester = KaryawanCRUDTester()
    
    try:
        # Create operations
        tester.test("Create karyawan", lambda: test_create_karyawan(tester))
        tester.test("Create karyawan (second)", lambda: test_create_karyawan(tester))
        
        # Read operations
        tester.test("Read karyawan", lambda: test_read_karyawan(tester))
        
        # Update operations
        tester.test("Update karyawan", lambda: test_update_karyawan(tester))
        
        # Delete operations
        tester.test("Delete karyawan", lambda: test_delete_karyawan(tester))
        
        # Validation tests
        tester.test("Create with invalid data", lambda: test_create_with_invalid_data(tester))
        tester.test("Update non-existent", lambda: test_update_nonexistent(tester))
        tester.test("Delete non-existent", lambda: test_delete_nonexistent(tester))
        
        return tester.summary()
        
    finally:
        tester.cleanup()

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