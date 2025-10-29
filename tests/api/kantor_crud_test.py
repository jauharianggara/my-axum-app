#!/usr/bin/env python3
"""
Kantor CRUD Operations Test
Tests Create, Read, Update, Delete operations for Kantor
"""

import requests
import json
import sys

API_BASE_URL = "http://localhost:8080"
API_BASE = f"{API_BASE_URL}/api"

class KantorCRUDTester:
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
        """Clean up created kantors"""
        print(f"\n🧹 Cleaning up {len(self.created_ids)} test kantors...")
        for kantor_id in self.created_ids:
            try:
                requests.delete(f"{API_BASE}/kantors/{kantor_id}", timeout=5)
            except:
                pass
    
    def summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        if total == 0:
            return False
        
        print(f"\n📊 KANTOR CRUD TEST SUMMARY")
        print(f"{'='*40}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total:  {total}")
        print(f"Success Rate: {(self.passed/total)*100:.1f}%")
        
        return self.failed == 0

def test_create_kantor(tester):
    """Test creating a new kantor"""
    test_data = {
        "nama": "Test Kantor CRUD",
        "alamat": "Jl. Test No. 123, Jakarta",
        "longitude": "106.8271530",
        "latitude": "-6.1751100"
    }
    
    response = requests.post(
        f"{API_BASE}/kantors",
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
    kantor_id = data.get("data", {}).get("id")
    if kantor_id:
        tester.created_ids.append(kantor_id)
    
    return True

def test_read_kantor(tester):
    """Test reading kantor data"""
    if not tester.created_ids:
        return False
    
    kantor_id = tester.created_ids[0]
    response = requests.get(f"{API_BASE}/kantors/{kantor_id}", timeout=5)
    
    if response.status_code != 200:
        return False
    
    data = response.json()
    return data.get("success") and data.get("data", {}).get("nama") == "Test Kantor CRUD"

def test_update_kantor(tester):
    """Test updating kantor data"""
    if not tester.created_ids:
        return False
    
    kantor_id = tester.created_ids[0]
    
    update_data = {
        "nama": "Updated Test Kantor",
        "alamat": "Jl. Updated No. 456, Jakarta",
        "longitude": "106.8000000",
        "latitude": "-6.2000000"
    }
    
    response = requests.put(
        f"{API_BASE}/kantors/{kantor_id}",
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
    get_response = requests.get(f"{API_BASE}/kantors/{kantor_id}", timeout=5)
    if get_response.status_code != 200:
        return False
    
    get_data = get_response.json()
    updated_kantor = get_data.get("data", {})
    
    return (updated_kantor.get("nama") == "Updated Test Kantor" and
            updated_kantor.get("alamat") == "Jl. Updated No. 456, Jakarta")

def test_delete_kantor(tester):
    """Test deleting kantor"""
    if not tester.created_ids:
        return False
    
    kantor_id = tester.created_ids.pop()  # Remove from list so it won't be cleaned up again
    
    response = requests.delete(f"{API_BASE}/kantors/{kantor_id}", timeout=5)
    
    if response.status_code != 200:
        return False
    
    # Verify deletion
    get_response = requests.get(f"{API_BASE}/kantors/{kantor_id}", timeout=5)
    return get_response.status_code == 404

def test_create_with_invalid_data(tester):
    """Test creating kantor with invalid data"""
    invalid_cases = [
        {
            "nama": "A",  # Too short
            "alamat": "Test Address",
            "longitude": "106.8271530",
            "latitude": "-6.1751100"
        },
        {
            "nama": "Test Kantor",
            "alamat": "A",  # Too short
            "longitude": "106.8271530",
            "latitude": "-6.1751100"
        },
        {
            "nama": "Test Kantor",
            "alamat": "Test Address",
            "longitude": "200",  # Invalid longitude (outside range)
            "latitude": "-6.1751100"
        },
        {
            "nama": "Test Kantor",
            "alamat": "Test Address",
            "longitude": "106.8271530",
            "latitude": "100"  # Invalid latitude (outside range)
        }
    ]
    
    for i, invalid_data in enumerate(invalid_cases):
        response = requests.post(
            f"{API_BASE}/kantors",
            json=invalid_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code != 400:
            print(f"   Invalid case {i+1} should return 400 but got {response.status_code}")
            return False
    
    return True

def test_update_nonexistent(tester):
    """Test updating non-existent kantor"""
    update_data = {
        "nama": "Non-existent Kantor",
        "alamat": "Test Address",
        "longitude": "106.8271530",
        "latitude": "-6.1751100"
    }
    
    response = requests.put(
        f"{API_BASE}/kantors/99999",
        json=update_data,
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    
    return response.status_code == 404

def test_delete_nonexistent(tester):
    """Test deleting non-existent kantor"""
    response = requests.delete(f"{API_BASE}/kantors/99999", timeout=5)
    return response.status_code == 404

def test_kantor_with_karyawans(tester):
    """Test getting kantor with karyawans"""
    # Get existing kantor
    response = requests.get(f"{API_BASE}/kantors", timeout=5)
    if response.status_code != 200:
        return False
    
    data = response.json()
    kantors = data.get("data", [])
    if not kantors:
        return False
    
    kantor_id = kantors[0]["id"]
    
    # Get kantor with karyawans
    response = requests.get(f"{API_BASE}/kantors/{kantor_id}/with-karyawans", timeout=5)
    if response.status_code != 200:
        return False
    
    data = response.json()
    return data.get("success") and "karyawans" in data.get("data", {})

def run_tests():
    """Run all kantor CRUD tests"""
    print("🧪 KANTOR CRUD OPERATIONS TESTS")
    print("="*50)
    
    tester = KantorCRUDTester()
    
    try:
        # Create operations
        tester.test("Create kantor", lambda: test_create_kantor(tester))
        tester.test("Create kantor (second)", lambda: test_create_kantor(tester))
        
        # Read operations
        tester.test("Read kantor", lambda: test_read_kantor(tester))
        
        # Update operations
        tester.test("Update kantor", lambda: test_update_kantor(tester))
        
        # Delete operations
        tester.test("Delete kantor", lambda: test_delete_kantor(tester))
        
        # Validation tests
        tester.test("Create with invalid data", lambda: test_create_with_invalid_data(tester))
        tester.test("Update non-existent", lambda: test_update_nonexistent(tester))
        tester.test("Delete non-existent", lambda: test_delete_nonexistent(tester))
        
        # Relationship tests
        tester.test("Kantor with karyawans", lambda: test_kantor_with_karyawans(tester))
        
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