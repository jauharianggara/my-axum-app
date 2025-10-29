#!/usr/bin/env python3
"""
Photo Performance Tests
Basic performance testing for photo upload functionality
"""

import requests
import sys
import time
import threading
from PIL import Image
import io

API_BASE_URL = "http://localhost:8080"
API_BASE = f"{API_BASE_URL}/api"

class PhotoPerformanceTester:
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
        if self.created_ids:
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
        
        print(f"\n📊 PHOTO PERFORMANCE TEST SUMMARY")
        print(f"{'='*40}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total:  {total}")
        print(f"Success Rate: {(self.passed/total)*100:.1f}%")
        
        return self.failed == 0

def create_test_image(size=(200, 200), format_type='JPEG'):
    """Create test image"""
    img = Image.new('RGB', size, color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=format_type)
    img_bytes.seek(0)
    return img_bytes.getvalue()

def get_valid_kantor_id():
    """Get a valid kantor ID for testing"""
    response = requests.get(f"{API_BASE}/kantors", timeout=5)
    if response.status_code != 200:
        return None
    
    data = response.json()
    kantors = data.get("data", [])
    return kantors[0]["id"] if kantors else None

def single_upload_test(test_id, image_data, kantor_id):
    """Single upload test for performance measurement"""
    files = {'foto': (f'perf_{test_id}.jpg', io.BytesIO(image_data), 'image/jpeg')}
    data = {
        'nama': f'Performance Test {test_id}',
        'posisi': 'Perf Tester',
        'gaji': '3000000',
        'kantor_id': str(kantor_id)
    }
    
    start_time = time.time()
    
    try:
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=15)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                karyawan_id = result.get('data', {}).get('id')
                return True, duration, karyawan_id
        
        return False, duration, None
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        return False, duration, None

def test_single_upload_performance(tester):
    """Test single upload performance"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    image_data = create_test_image()
    print(f"      Image size: {len(image_data)} bytes")
    
    success, duration, karyawan_id = single_upload_test(1, image_data, kantor_id)
    
    if karyawan_id:
        tester.created_ids.append(karyawan_id)
    
    if success:
        print(f"      Upload time: {duration:.3f} seconds")
        return duration < 5.0  # Should complete within 5 seconds
    
    return False

def test_multiple_uploads_performance(tester):
    """Test multiple sequential uploads"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    image_data = create_test_image()
    num_uploads = 5
    
    start_time = time.time()
    successful_uploads = 0
    
    for i in range(num_uploads):
        success, duration, karyawan_id = single_upload_test(i, image_data, kantor_id)
        
        if success:
            successful_uploads += 1
            if karyawan_id:
                tester.created_ids.append(karyawan_id)
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    print(f"      {successful_uploads}/{num_uploads} uploads successful")
    print(f"      Total time: {total_duration:.2f} seconds")
    print(f"      Average per upload: {total_duration/num_uploads:.2f} seconds")
    
    return successful_uploads >= num_uploads * 0.8  # 80% success rate required

def test_concurrent_uploads_performance(tester):
    """Test concurrent uploads performance"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    image_data = create_test_image()
    num_concurrent = 3
    results = []
    
    def upload_worker(worker_id):
        success, duration, karyawan_id = single_upload_test(f"concurrent_{worker_id}", image_data, kantor_id)
        results.append((success, duration, karyawan_id))
    
    # Start concurrent uploads
    threads = []
    start_time = time.time()
    
    for i in range(num_concurrent):
        thread = threading.Thread(target=upload_worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join(timeout=30)  # 30 second timeout per thread
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Collect results
    successful_uploads = 0
    for success, duration, karyawan_id in results:
        if success:
            successful_uploads += 1
            if karyawan_id:
                tester.created_ids.append(karyawan_id)
    
    print(f"      {successful_uploads}/{num_concurrent} concurrent uploads successful")
    print(f"      Total time: {total_duration:.2f} seconds")
    
    return successful_uploads >= num_concurrent * 0.6  # 60% success rate for concurrent

def test_file_size_performance(tester):
    """Test performance with different file sizes"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    file_sizes = [
        (100, 100, "Small"),
        (300, 300, "Medium"),
        (500, 500, "Large")
    ]
    
    all_tests_passed = True
    
    for width, height, size_name in file_sizes:
        image_data = create_test_image(size=(width, height))
        file_size = len(image_data)
        
        success, duration, karyawan_id = single_upload_test(size_name.lower(), image_data, kantor_id)
        
        if karyawan_id:
            tester.created_ids.append(karyawan_id)
        
        print(f"      {size_name} ({file_size} bytes): {duration:.3f}s - {'✅' if success else '❌'}")
        
        if not success:
            all_tests_passed = False
    
    return all_tests_passed

def test_upload_throughput(tester):
    """Test upload throughput"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    image_data = create_test_image()
    file_size = len(image_data)
    
    success, duration, karyawan_id = single_upload_test("throughput", image_data, kantor_id)
    
    if karyawan_id:
        tester.created_ids.append(karyawan_id)
    
    if success:
        throughput = file_size / duration  # bytes per second
        throughput_kb = throughput / 1024  # KB per second
        
        print(f"      File size: {file_size} bytes")
        print(f"      Upload time: {duration:.3f} seconds")
        print(f"      Throughput: {throughput_kb:.1f} KB/s")
        
        return throughput_kb > 10  # Should be faster than 10 KB/s
    
    return False

def run_tests():
    """Run all photo performance tests"""
    print("🧪 PHOTO PERFORMANCE TESTS")
    print("="*50)
    
    tester = PhotoPerformanceTester()
    
    try:
        # Performance tests
        tester.test("Single upload performance", lambda: test_single_upload_performance(tester))
        tester.test("Multiple uploads performance", lambda: test_multiple_uploads_performance(tester))
        tester.test("Concurrent uploads performance", lambda: test_concurrent_uploads_performance(tester))
        tester.test("File size performance", lambda: test_file_size_performance(tester))
        tester.test("Upload throughput", lambda: test_upload_throughput(tester))
        
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