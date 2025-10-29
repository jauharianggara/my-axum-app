#!/usr/bin/env python3
"""
Test Utilities
Common utilities for all test suites
"""

import requests
import json
from PIL import Image
import io
import time

API_BASE_URL = "http://localhost:8080"
API_BASE = f"{API_BASE_URL}/api"

def wait_for_server(max_attempts=10, delay=2):
    """Wait for server to be available"""
    print(f"🔄 Waiting for server at {API_BASE_URL}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ Server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if attempt < max_attempts - 1:
            print(f"⏳ Attempt {attempt + 1}/{max_attempts} - waiting {delay}s...")
            time.sleep(delay)
    
    print(f"❌ Server not ready after {max_attempts} attempts")
    return False

def check_server_health():
    """Check if server is healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_valid_kantor_id():
    """Get a valid kantor ID for testing"""
    try:
        response = requests.get(f"{API_BASE}/kantors", timeout=5)
        if response.status_code != 200:
            return None
        
        data = response.json()
        kantors = data.get("data", [])
        return kantors[0]["id"] if kantors else None
    except:
        return None

def create_test_image(size=(100, 100), format_type='JPEG', color='blue'):
    """Create test image"""
    img = Image.new('RGB', size, color=color)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=format_type)
    img_bytes.seek(0)
    return img_bytes.getvalue()

def cleanup_test_karyawans(karyawan_ids):
    """Clean up test karyawans"""
    if not karyawan_ids:
        return
    
    print(f"🧹 Cleaning up {len(karyawan_ids)} test karyawans...")
    cleaned = 0
    
    for karyawan_id in karyawan_ids:
        try:
            response = requests.delete(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
            if response.status_code == 200:
                cleaned += 1
        except:
            pass
    
    print(f"✅ Cleaned up {cleaned}/{len(karyawan_ids)} karyawans")

def cleanup_test_kantors(kantor_ids):
    """Clean up test kantors"""
    if not kantor_ids:
        return
    
    print(f"🧹 Cleaning up {len(kantor_ids)} test kantors...")
    cleaned = 0
    
    for kantor_id in kantor_ids:
        try:
            response = requests.delete(f"{API_BASE}/kantors/{kantor_id}", timeout=5)
            if response.status_code == 200:
                cleaned += 1
        except:
            pass
    
    print(f"✅ Cleaned up {cleaned}/{len(kantor_ids)} kantors")

def print_test_header(title):
    """Print formatted test header"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def print_test_summary(passed, failed, title="TEST SUMMARY"):
    """Print formatted test summary"""
    total = passed + failed
    if total == 0:
        return False
    
    print(f"\n📊 {title}")
    print(f"{'='*40}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    return failed == 0

class TestRunner:
    """Base test runner class"""
    
    def __init__(self, test_name):
        self.test_name = test_name
        self.passed = 0
        self.failed = 0
        self.created_karyawan_ids = []
        self.created_kantor_ids = []
    
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
        """Clean up created resources"""
        cleanup_test_karyawans(self.created_karyawan_ids)
        cleanup_test_kantors(self.created_kantor_ids)
    
    def summary(self):
        """Print test summary"""
        return print_test_summary(self.passed, self.failed, f"{self.test_name} SUMMARY")

def validate_api_response(response, expected_status=200, should_succeed=True):
    """Validate API response format"""
    if response.status_code != expected_status:
        return False
    
    try:
        data = response.json()
        success = data.get("success", False)
        
        if should_succeed and not success:
            return False
        elif not should_succeed and success:
            return False
        
        return True
    except json.JSONDecodeError:
        return False

def create_test_karyawan_data(nama="Test User", kantor_id=None):
    """Create test karyawan data"""
    if kantor_id is None:
        kantor_id = get_valid_kantor_id()
    
    return {
        "nama": nama,
        "posisi": "Software Tester",
        "gaji": "5000000",
        "kantor_id": str(kantor_id)
    }

def create_test_kantor_data(nama="Test Kantor"):
    """Create test kantor data"""
    return {
        "nama": nama,
        "alamat": "Jl. Test No. 123, Jakarta",
        "longitude": "106.8271530",
        "latitude": "-6.1751100"
    }