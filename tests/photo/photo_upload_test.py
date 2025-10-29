#!/usr/bin/env python3
"""
Photo Upload Functionality Tests
Tests core photo upload features for karyawan
"""

import requests
import json
import sys
from PIL import Image
import io
import time

API_BASE_URL = "http://localhost:8080"
API_BASE = f"{API_BASE_URL}/api"

class PhotoUploadTester:
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
        
        print(f"\n📊 PHOTO UPLOAD TEST SUMMARY")
        print(f"{'='*40}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total:  {total}")
        print(f"Success Rate: {(self.passed/total)*100:.1f}%")
        
        return self.failed == 0

def create_test_image(size=(100, 100), format_type='JPEG'):
    """Create test image"""
    img = Image.new('RGB', size, color='blue')
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

def test_create_karyawan_with_photo(tester):
    """Test creating karyawan with photo"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    image_data = create_test_image()
    files = {'foto': ('test.jpg', io.BytesIO(image_data), 'image/jpeg')}
    data = {
        'nama': 'Test Employee Photo',
        'posisi': 'Photo Tester',
        'gaji': '4000000',
        'kantor_id': str(kantor_id)
    }
    
    response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                           files=files, data=data, timeout=10)
    
    if response.status_code != 200:
        return False
    
    result = response.json()
    if not result.get('success'):
        return False
    
    # Store ID for cleanup
    karyawan_id = result.get('data', {}).get('id')
    if karyawan_id:
        tester.created_ids.append(karyawan_id)
    
    # Check photo fields
    data = result.get('data', {})
    return (data.get('foto_path') and 
            data.get('foto_original_name') == 'test.jpg' and
            data.get('foto_mime_type') == 'image/jpeg')

def test_photo_file_accessible(tester):
    """Test photo file accessibility"""
    if not tester.created_ids:
        return False
    
    # Get karyawan details
    karyawan_id = tester.created_ids[0]
    response = requests.get(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
    
    if response.status_code != 200:
        return False
    
    data = response.json()
    foto_path = data.get('data', {}).get('foto_path')
    
    if not foto_path:
        return False
    
    # Try to access photo file
    photo_url = f"{API_BASE_URL}/{foto_path}"
    photo_response = requests.get(photo_url, timeout=5)
    
    return photo_response.status_code == 200

def test_upload_photo_to_existing(tester):
    """Test uploading photo to existing karyawan"""
    # First create karyawan without photo
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    create_data = {
        "nama": "Test Without Photo",
        "posisi": "Tester",
        "gaji": "4000000",
        "kantor_id": str(kantor_id)
    }
    
    create_response = requests.post(
        f"{API_BASE}/karyawans",
        json=create_data,
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    
    if create_response.status_code != 200:
        return False
    
    create_result = create_response.json()
    if not create_result.get('success'):
        return False
    
    karyawan_id = create_result.get('data', {}).get('id')
    if not karyawan_id:
        return False
    
    tester.created_ids.append(karyawan_id)
    
    # Now upload photo
    image_data = create_test_image()
    files = {'foto': ('upload.jpg', io.BytesIO(image_data), 'image/jpeg')}
    
    upload_response = requests.put(f"{API_BASE}/karyawans/{karyawan_id}/photo", 
                                 files=files, timeout=10)
    
    if upload_response.status_code != 200:
        return False
    
    upload_result = upload_response.json()
    return upload_result.get('success', False)

def test_delete_photo(tester):
    """Test deleting photo from karyawan"""
    if not tester.created_ids:
        return False
    
    karyawan_id = tester.created_ids[0]
    
    # Delete photo
    response = requests.delete(f"{API_BASE}/karyawans/{karyawan_id}/photo", timeout=5)
    
    if response.status_code != 200:
        return False
    
    result = response.json()
    if not result.get('success'):
        return False
    
    # Verify photo is removed
    get_response = requests.get(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
    if get_response.status_code != 200:
        return False
    
    get_data = get_response.json()
    karyawan_data = get_data.get('data', {})
    
    return karyawan_data.get('foto_path') is None

def test_invalid_file_type(tester):
    """Test rejection of invalid file types"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    # Try to upload text file as photo
    invalid_file = b"This is not an image"
    files = {'foto': ('test.txt', io.BytesIO(invalid_file), 'text/plain')}
    data = {
        'nama': 'Invalid Test',
        'posisi': 'Tester',
        'gaji': '4000000',
        'kantor_id': str(kantor_id)
    }
    
    response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                           files=files, data=data, timeout=10)
    
    # Should reject invalid file type
    if response.status_code == 400:
        return True
    elif response.status_code == 200:
        result = response.json()
        if result.get('success'):
            # Clean up if accidentally accepted
            karyawan_id = result.get('data', {}).get('id')
            if karyawan_id:
                requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
        return not result.get('success')  # Should not succeed
    
    return False

def test_supported_formats(tester):
    """Test supported image formats"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    formats = [
        ('JPEG', 'image/jpeg', 'jpg'),
        ('PNG', 'image/png', 'png')
    ]
    
    for format_name, mime_type, extension in formats:
        image_data = create_test_image(format_type=format_name)
        files = {'foto': (f'test.{extension}', io.BytesIO(image_data), mime_type)}
        data = {
            'nama': f'Format Test {format_name}',
            'posisi': 'Tester',
            'gaji': '4000000',
            'kantor_id': str(kantor_id)
        }
        
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=10)
        
        if response.status_code != 200:
            return False
        
        result = response.json()
        if not result.get('success'):
            return False
        
        # Cleanup
        karyawan_id = result.get('data', {}).get('id')
        if karyawan_id:
            tester.created_ids.append(karyawan_id)
    
    return True

def test_performance_multiple_uploads(tester):
    """Test performance with multiple uploads"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    start_time = time.time()
    
    for i in range(3):  # Test with 3 uploads
        image_data = create_test_image()
        files = {'foto': (f'perf_test_{i}.jpg', io.BytesIO(image_data), 'image/jpeg')}
        data = {
            'nama': f'Perf Test {i}',
            'posisi': 'Performance Tester',
            'gaji': '4000000',
            'kantor_id': str(kantor_id)
        }
        
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=10)
        
        if response.status_code != 200:
            return False
        
        result = response.json()
        if not result.get('success'):
            return False
        
        karyawan_id = result.get('data', {}).get('id')
        if karyawan_id:
            tester.created_ids.append(karyawan_id)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"      3 uploads completed in {duration:.2f} seconds")
    return duration < 30  # Should complete within 30 seconds

def run_tests():
    """Run all photo upload tests"""
    print("🧪 PHOTO UPLOAD FUNCTIONALITY TESTS")
    print("="*50)
    
    tester = PhotoUploadTester()
    
    try:
        # Core functionality tests
        tester.test("Create karyawan with photo", lambda: test_create_karyawan_with_photo(tester))
        tester.test("Photo file accessible", lambda: test_photo_file_accessible(tester))
        tester.test("Upload photo to existing", lambda: test_upload_photo_to_existing(tester))
        tester.test("Delete photo", lambda: test_delete_photo(tester))
        
        # Validation tests
        tester.test("Reject invalid file type", lambda: test_invalid_file_type(tester))
        tester.test("Support image formats", lambda: test_supported_formats(tester))
        
        # Performance test
        tester.test("Performance multiple uploads", lambda: test_performance_multiple_uploads(tester))
        
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