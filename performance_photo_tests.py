#!/usr/bin/env python3
"""
API Performance Testing for Karyawan Photo Upload
Tests load, stress, and performance characteristics
"""

import requests
import json
import time
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile
import os
from PIL import Image
import io

BASE_URL = "http://localhost:8080"
API_BASE = f"{BASE_URL}/api"

class PerformanceMetrics:
    """Class to track performance metrics"""
    
    def __init__(self):
        self.response_times = []
        self.success_count = 0
        self.error_count = 0
        self.errors = []
        self.start_time = None
        self.end_time = None
    
    def add_result(self, response_time: float, success: bool, error_msg: str = None):
        """Add a test result"""
        self.response_times.append(response_time)
        if success:
            self.success_count += 1
        else:
            self.error_count += 1
            if error_msg:
                self.errors.append(error_msg)
    
    def get_stats(self):
        """Get performance statistics"""
        if not self.response_times:
            return {}
        
        total_time = self.end_time - self.start_time if self.end_time and self.start_time else 0
        
        return {
            'total_requests': len(self.response_times),
            'success_count': self.success_count,
            'error_count': self.error_count,
            'success_rate': (self.success_count / len(self.response_times)) * 100,
            'avg_response_time': statistics.mean(self.response_times),
            'min_response_time': min(self.response_times),
            'max_response_time': max(self.response_times),
            'median_response_time': statistics.median(self.response_times),
            'p95_response_time': self.percentile(self.response_times, 95),
            'p99_response_time': self.percentile(self.response_times, 99),
            'requests_per_second': len(self.response_times) / total_time if total_time > 0 else 0,
            'total_duration': total_time
        }
    
    @staticmethod
    def percentile(data, percentile):
        """Calculate percentile"""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))

def create_test_image(size=(200, 200), format='JPEG', quality=85):
    """Create test image in memory"""
    img = Image.new('RGB', size, color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=format, quality=quality)
    img_bytes.seek(0)
    return img_bytes.getvalue()

def single_photo_upload_test(test_id: int, image_data: bytes) -> tuple:
    """Single photo upload test"""
    start_time = time.time()
    
    try:
        files = {
            'foto': (f'perf_test_{test_id}.jpg', io.BytesIO(image_data), 'image/jpeg')
        }
        
        data = {
            'nama': f'Performance Test {test_id}',
            'posisi': 'Load Tester',
            'gaji': '3000000',
            'kantor_id': '2'
        }
        
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=30)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                return response_time, True, None, result['data']['id']
            else:
                return response_time, False, result['message'], None
        else:
            return response_time, False, f"HTTP {response.status_code}", None
            
    except Exception as e:
        end_time = time.time()
        response_time = end_time - start_time
        return response_time, False, str(e), None

def load_test_photo_upload(num_requests: int = 50, num_workers: int = 10):
    """Load test for photo upload endpoint"""
    print(f"\n🔥 LOAD TEST: {num_requests} photo uploads with {num_workers} workers")
    print("=" * 60)
    
    # Pre-create image data
    image_data = create_test_image()
    print(f"📷 Image size: {len(image_data)} bytes")
    
    metrics = PerformanceMetrics()
    created_ids = []
    
    metrics.start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Submit all tasks
        futures = [
            executor.submit(single_photo_upload_test, i, image_data)
            for i in range(num_requests)
        ]
        
        # Collect results
        for i, future in enumerate(as_completed(futures)):
            try:
                response_time, success, error_msg, karyawan_id = future.result()
                metrics.add_result(response_time, success, error_msg)
                
                if karyawan_id:
                    created_ids.append(karyawan_id)
                
                # Progress indicator
                if (i + 1) % 10 == 0:
                    print(f"⏳ Completed {i + 1}/{num_requests} requests")
                    
            except Exception as e:
                metrics.add_result(30.0, False, f"Future error: {str(e)}")
    
    metrics.end_time = time.time()
    
    # Print results
    stats = metrics.get_stats()
    print(f"\n📊 LOAD TEST RESULTS")
    print("=" * 30)
    print(f"Total Requests:      {stats['total_requests']}")
    print(f"Successful:          {stats['success_count']} ({stats['success_rate']:.1f}%)")
    print(f"Failed:              {stats['error_count']}")
    print(f"Average Response:    {stats['avg_response_time']:.3f}s")
    print(f"Min Response:        {stats['min_response_time']:.3f}s")
    print(f"Max Response:        {stats['max_response_time']:.3f}s")
    print(f"Median Response:     {stats['median_response_time']:.3f}s")
    print(f"95th Percentile:     {stats['p95_response_time']:.3f}s")
    print(f"99th Percentile:     {stats['p99_response_time']:.3f}s")
    print(f"Requests/sec:        {stats['requests_per_second']:.2f}")
    print(f"Total Duration:      {stats['total_duration']:.2f}s")
    
    if metrics.errors:
        print(f"\n❌ ERRORS:")
        error_summary = {}
        for error in metrics.errors:
            error_summary[error] = error_summary.get(error, 0) + 1
        
        for error, count in error_summary.items():
            print(f"  {error}: {count} times")
    
    # Cleanup created karyawans
    print(f"\n🧹 Cleaning up {len(created_ids)} test karyawans...")
    cleanup_count = 0
    for karyawan_id in created_ids:
        try:
            response = requests.delete(f"{API_BASE}/karyawans/{karyawan_id}", timeout=10)
            if response.status_code == 200:
                cleanup_count += 1
        except:
            pass
    
    print(f"✅ Cleaned up {cleanup_count}/{len(created_ids)} test karyawans")
    
    return stats

def stress_test_photo_upload(duration_seconds: int = 60, max_workers: int = 20):
    """Stress test for photo upload endpoint"""
    print(f"\n⚡ STRESS TEST: {duration_seconds}s duration with up to {max_workers} workers")
    print("=" * 60)
    
    image_data = create_test_image()
    metrics = PerformanceMetrics()
    created_ids = []
    test_counter = 0
    
    metrics.start_time = time.time()
    end_time = metrics.start_time + duration_seconds
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = set()
        
        while time.time() < end_time:
            # Add new requests if we have capacity
            while len(futures) < max_workers and time.time() < end_time:
                future = executor.submit(single_photo_upload_test, test_counter, image_data)
                futures.add(future)
                test_counter += 1
            
            # Check completed requests
            completed_futures = set()
            for future in futures:
                if future.done():
                    try:
                        response_time, success, error_msg, karyawan_id = future.result()
                        metrics.add_result(response_time, success, error_msg)
                        
                        if karyawan_id:
                            created_ids.append(karyawan_id)
                            
                    except Exception as e:
                        metrics.add_result(30.0, False, f"Future error: {str(e)}")
                    
                    completed_futures.add(future)
            
            # Remove completed futures
            futures -= completed_futures
            
            # Progress update every 10 seconds
            elapsed = time.time() - metrics.start_time
            if int(elapsed) % 10 == 0 and len(metrics.response_times) > 0:
                current_rps = len(metrics.response_times) / elapsed
                print(f"⏱️  {elapsed:.0f}s: {len(metrics.response_times)} requests, {current_rps:.1f} RPS")
            
            time.sleep(0.1)  # Small delay to prevent busy waiting
        
        # Wait for remaining futures
        for future in futures:
            try:
                response_time, success, error_msg, karyawan_id = future.result(timeout=30)
                metrics.add_result(response_time, success, error_msg)
                if karyawan_id:
                    created_ids.append(karyawan_id)
            except:
                metrics.add_result(30.0, False, "Timeout")
    
    metrics.end_time = time.time()
    
    # Print results
    stats = metrics.get_stats()
    print(f"\n📊 STRESS TEST RESULTS")
    print("=" * 30)
    print(f"Duration:            {stats['total_duration']:.2f}s")
    print(f"Total Requests:      {stats['total_requests']}")
    print(f"Successful:          {stats['success_count']} ({stats['success_rate']:.1f}%)")
    print(f"Failed:              {stats['error_count']}")
    print(f"Requests/sec:        {stats['requests_per_second']:.2f}")
    print(f"Average Response:    {stats['avg_response_time']:.3f}s")
    print(f"95th Percentile:     {stats['p95_response_time']:.3f}s")
    print(f"99th Percentile:     {stats['p99_response_time']:.3f}s")
    
    # Cleanup
    print(f"\n🧹 Cleaning up {len(created_ids)} test karyawans...")
    cleanup_count = 0
    for karyawan_id in created_ids:
        try:
            response = requests.delete(f"{API_BASE}/karyawans/{karyawan_id}", timeout=10)
            if response.status_code == 200:
                cleanup_count += 1
        except:
            pass
    
    print(f"✅ Cleaned up {cleanup_count}/{len(created_ids)} test karyawans")
    
    return stats

def test_different_file_sizes():
    """Test performance with different file sizes"""
    print(f"\n📏 FILE SIZE PERFORMANCE TEST")
    print("=" * 40)
    
    file_configs = [
        (100, 100, 'JPEG', 50, "Small JPEG (low quality)"),
        (200, 200, 'JPEG', 85, "Medium JPEG (good quality)"),
        (500, 500, 'JPEG', 95, "Large JPEG (high quality)"),
        (200, 200, 'PNG', None, "Medium PNG"),
        (100, 100, 'PNG', None, "Small PNG"),
    ]
    
    results = []
    
    for width, height, format_type, quality, description in file_configs:
        print(f"\n🔍 Testing {description}")
        
        # Create image
        img = Image.new('RGB', (width, height), color='blue')
        img_bytes = io.BytesIO()
        
        if format_type == 'JPEG':
            img.save(img_bytes, format=format_type, quality=quality)
        else:
            img.save(img_bytes, format=format_type)
        
        image_data = img_bytes.getvalue()
        file_size = len(image_data)
        
        print(f"   📊 File size: {file_size} bytes ({file_size/1024:.1f} KB)")
        
        # Test upload performance
        response_times = []
        created_ids = []
        
        for i in range(5):  # 5 tests per file size
            response_time, success, error_msg, karyawan_id = single_photo_upload_test(
                f"size_test_{i}", image_data
            )
            
            if success and karyawan_id:
                response_times.append(response_time)
                created_ids.append(karyawan_id)
            else:
                print(f"   ❌ Upload failed: {error_msg}")
        
        if response_times:
            avg_time = statistics.mean(response_times)
            throughput = file_size / avg_time  # bytes per second
            
            print(f"   ⏱️  Average time: {avg_time:.3f}s")
            print(f"   🚀 Throughput: {throughput/1024:.1f} KB/s")
            
            results.append({
                'description': description,
                'file_size': file_size,
                'avg_response_time': avg_time,
                'throughput_kbps': throughput/1024
            })
        
        # Cleanup
        for karyawan_id in created_ids:
            try:
                requests.delete(f"{API_BASE}/karyawans/{karyawan_id}", timeout=10)
            except:
                pass
    
    # Summary
    print(f"\n📊 FILE SIZE PERFORMANCE SUMMARY")
    print("=" * 50)
    print(f"{'Description':<25} {'Size (KB)':<10} {'Time (s)':<10} {'KB/s':<10}")
    print("-" * 50)
    
    for result in results:
        print(f"{result['description']:<25} "
              f"{result['file_size']/1024:<10.1f} "
              f"{result['avg_response_time']:<10.3f} "
              f"{result['throughput_kbps']:<10.1f}")

def run_all_performance_tests():
    """Run all performance tests"""
    print(f"\n{'='*80}")
    print("🚀 COMPREHENSIVE PERFORMANCE TESTING SUITE")
    print(f"{'='*80}")
    
    # Check server availability
    try:
        response = requests.get(f"{API_BASE}/karyawans", timeout=5)
        print(f"✅ Server is available at {BASE_URL}")
    except:
        print(f"❌ Server not available at {BASE_URL}")
        return False
    
    try:
        # Test 1: Different file sizes
        test_different_file_sizes()
        
        # Test 2: Load test
        load_stats = load_test_photo_upload(num_requests=25, num_workers=5)
        
        # Test 3: Stress test (shorter duration for demo)
        stress_stats = stress_test_photo_upload(duration_seconds=30, max_workers=10)
        
        # Overall assessment
        print(f"\n{'='*80}")
        print("🎯 PERFORMANCE ASSESSMENT")
        print(f"{'='*80}")
        
        load_rps = load_stats['requests_per_second']
        stress_rps = stress_stats['requests_per_second']
        load_success = load_stats['success_rate']
        stress_success = stress_stats['success_rate']
        
        print(f"Load Test RPS:       {load_rps:.2f}")
        print(f"Stress Test RPS:     {stress_rps:.2f}")
        print(f"Load Success Rate:   {load_success:.1f}%")
        print(f"Stress Success Rate: {stress_success:.1f}%")
        
        # Performance rating
        if load_rps >= 10 and stress_rps >= 5 and load_success >= 95:
            print(f"\n🏆 EXCELLENT PERFORMANCE!")
            print("   Your photo upload API can handle production load well.")
        elif load_rps >= 5 and stress_rps >= 2 and load_success >= 90:
            print(f"\n✅ GOOD PERFORMANCE!")
            print("   Your API performs well under normal conditions.")
        elif load_rps >= 2 and load_success >= 80:
            print(f"\n⚠️  MODERATE PERFORMANCE")
            print("   API works but may need optimization for high load.")
        else:
            print(f"\n❌ PERFORMANCE ISSUES DETECTED")
            print("   Consider optimizing your API for better performance.")
        
        return True
        
    except Exception as e:
        print(f"\n💥 Performance tests failed: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        success = run_all_performance_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Performance tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n💥 Performance test suite failed: {str(e)}")
        exit(1)
