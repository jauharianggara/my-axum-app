#!/usr/bin/env python3
"""
Simple Test Runner for Photo Upload API
Runs basic functionality tests
"""

import requests
import json
from PIL import Image
import io
import time

BASE_URL = "http://localhost:8080"
API_BASE = f"{BASE_URL}/api"

class SimpleTestRunner:
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = []
    
    def test(self, name, condition, message=""):
        """Run a single test"""
        self.total_tests += 1
        if condition:
            self.passed_tests += 1
            print(f"PASS: {name}")
            if message:
                print(f"      {message}")
        else:
            self.failed_tests.append(name)
            print(f"FAIL: {name}")
            if message:
                print(f"      {message}")
    
    def summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {len(self.failed_tests)}")
        print(f"Success rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        if self.failed_tests:
            print(f"\nFAILED TESTS:")
            for test in self.failed_tests:
                print(f"  - {test}")
        
        return len(self.failed_tests) == 0

def create_test_image(size=(100, 100), format_type='JPEG'):
    """Create test image"""
    img = Image.new('RGB', size, color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=format_type)
    img_bytes.seek(0)
    return img_bytes.getvalue()

def run_tests():
    """Run all photo upload tests"""
    print("PHOTO UPLOAD API TESTING SUITE")
    print("="*60)
    
    runner = SimpleTestRunner()
    
    # Test 1: Check server connectivity
    try:
        response = requests.get(f"{API_BASE}/karyawans", timeout=5)
        runner.test("Server connectivity", 
                   response.status_code == 200,
                   f"Server responded with status {response.status_code}")
    except Exception as e:
        runner.test("Server connectivity", False, f"Connection failed: {str(e)}")
        return False
    
    # Test 2: Create karyawan with photo
    try:
        image_data = create_test_image()
        files = {'foto': ('test.jpg', io.BytesIO(image_data), 'image/jpeg')}
        data = {
            'nama': 'Test Employee',
            'posisi': 'Tester',
            'gaji': '4000000',
            'kantor_id': '2'
        }
        
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            success = result.get('success', False)
            runner.test("Create karyawan with photo", success, 
                       result.get('message', 'No message'))
            
            if success:
                karyawan_id = result.get('data', {}).get('id')
                foto_path = result.get('data', {}).get('foto_path')
                
                runner.test("Photo path assigned", 
                           bool(foto_path),
                           f"Photo path: {foto_path}")
                
                # Test 3: Get karyawan details
                get_response = requests.get(f"{API_BASE}/karyawans/{karyawan_id}")
                if get_response.status_code == 200:
                    get_result = get_response.json()
                    has_photo_info = get_result.get('data', {}).get('foto_path') is not None
                    runner.test("Get karyawan with photo info", has_photo_info,
                               "Photo information included in response")
                else:
                    runner.test("Get karyawan with photo info", False,
                               f"Failed to get karyawan: {get_response.status_code}")
                
                # Test 4: Photo file accessibility
                if foto_path:
                    photo_url = f"{BASE_URL}/{foto_path}"
                    photo_response = requests.get(photo_url)
                    runner.test("Photo file accessible", 
                               photo_response.status_code == 200,
                               f"Photo URL: {photo_url}")
                
                # Test 5: Delete karyawan (cleanup)
                delete_response = requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
                runner.test("Delete karyawan", 
                           delete_response.status_code == 200,
                           "Cleanup successful")
            else:
                runner.test("Create karyawan with photo", False, 
                           result.get('message', 'Unknown error'))
        else:
            runner.test("Create karyawan with photo", False,
                       f"HTTP {response.status_code}: {response.text}")
    
    except Exception as e:
        runner.test("Create karyawan with photo", False, f"Exception: {str(e)}")
    
    # Test 6: Reject invalid file types
    try:
        invalid_file = b"This is not an image"
        files = {'foto': ('test.txt', io.BytesIO(invalid_file), 'text/plain')}
        data = {
            'nama': 'Invalid Test',
            'posisi': 'Tester',
            'gaji': '4000000',
            'kantor_id': '2'
        }
        
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=10)
        
        # Should reject invalid file type
        if response.status_code == 400:
            result = response.json()
            rejected = not result.get('success', True)
            runner.test("Reject invalid file type", rejected,
                       f"Correctly rejected: {result.get('message', '')}")
        elif response.status_code == 200:
            result = response.json()
            if result.get('success'):
                # If it was accepted, we need to clean up
                karyawan_id = result.get('data', {}).get('id')
                if karyawan_id:
                    requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
                runner.test("Reject invalid file type", False,
                           "Invalid file was incorrectly accepted!")
            else:
                runner.test("Reject invalid file type", True,
                           f"Rejected: {result.get('message', '')}")
        else:
            runner.test("Reject invalid file type", True,
                       f"Server rejected with status {response.status_code}")
            
    except Exception as e:
        runner.test("Reject invalid file type", False, f"Exception: {str(e)}")
    
    # Test 7: Test supported image formats
    for format_name in ['JPEG', 'PNG']:
        try:
            image_data = create_test_image(format_type=format_name)
            mime_type = 'image/jpeg' if format_name == 'JPEG' else 'image/png'
            extension = 'jpg' if format_name == 'JPEG' else 'png'
            
            files = {'foto': (f'test.{extension}', io.BytesIO(image_data), mime_type)}
            data = {
                'nama': f'Format Test {format_name}',
                'posisi': 'Tester',
                'gaji': '4000000',
                'kantor_id': '2'
            }
            
            response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                   files=files, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                success = result.get('success', False)
                runner.test(f"Upload {format_name} format", success,
                           f"{format_name} format support")
                
                # Cleanup
                if success:
                    karyawan_id = result.get('data', {}).get('id')
                    if karyawan_id:
                        requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
            else:
                runner.test(f"Upload {format_name} format", False,
                           f"HTTP {response.status_code}")
                
        except Exception as e:
            runner.test(f"Upload {format_name} format", False, f"Exception: {str(e)}")
    
    # Performance test
    try:
        print("\nPerformance test: Multiple uploads...")
        start_time = time.time()
        created_ids = []
        
        for i in range(3):  # Small performance test
            image_data = create_test_image()
            files = {'foto': (f'perf_test_{i}.jpg', io.BytesIO(image_data), 'image/jpeg')}
            data = {
                'nama': f'Perf Test {i}',
                'posisi': 'Performance Tester',
                'gaji': '4000000',
                'kantor_id': '2'
            }
            
            response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                   files=files, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    created_ids.append(result['data']['id'])
        
        end_time = time.time()
        duration = end_time - start_time
        
        runner.test("Performance test", 
                   len(created_ids) == 3,
                   f"3 uploads completed in {duration:.2f} seconds")
        
        # Cleanup performance test data
        for karyawan_id in created_ids:
            requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
            
    except Exception as e:
        runner.test("Performance test", False, f"Exception: {str(e)}")
    
    return runner.summary()

if __name__ == "__main__":
    try:
        success = run_tests()
        print(f"\nTest suite {'PASSED' if success else 'FAILED'}")
        exit(0 if success else 1)
    except Exception as e:
        print(f"Test suite error: {str(e)}")
        exit(1)