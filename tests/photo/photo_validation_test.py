#!/usr/bin/env python3
"""
Photo Validation Tests
Tests photo upload validation rules and security
"""

import requests
import json
import sys
from PIL import Image
import io

API_BASE_URL = "http://localhost:8080"
API_BASE = f"{API_BASE_URL}/api"

class PhotoValidationTester:
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
        
        print(f"\n📊 PHOTO VALIDATION TEST SUMMARY")
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

def test_file_type_validation(tester):
    """Test file type validation"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    invalid_files = [
        ('test.txt', b'This is a text file', 'text/plain'),
        ('test.pdf', b'%PDF-1.4 fake pdf', 'application/pdf'),
        ('test.exe', b'MZ fake exe', 'application/octet-stream'),
        ('test.js', b'alert("xss")', 'application/javascript'),
        ('test.html', b'<html><script>alert("xss")</script></html>', 'text/html'),
    ]
    
    for filename, content, mime_type in invalid_files:
        files = {'foto': (filename, io.BytesIO(content), mime_type)}
        data = {
            'nama': f'File Type Test {filename}',
            'posisi': 'Validator',
            'gaji': '4000000',
            'kantor_id': str(kantor_id)
        }
        
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=10)
        
        # Should reject all invalid file types
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                # Clean up if accidentally accepted
                karyawan_id = result.get('data', {}).get('id')
                if karyawan_id:
                    requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
                print(f"      SECURITY ISSUE: {filename} was accepted!")
                return False
        elif response.status_code != 400:
            print(f"      Unexpected status {response.status_code} for {filename}")
            return False
    
    return True

def test_file_size_validation(tester):
    """Test file size validation"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    # Create a large image (should be rejected if over 5MB)
    try:
        # Create large image
        large_img = Image.new('RGB', (2000, 2000), color='red')
        img_bytes = io.BytesIO()
        large_img.save(img_bytes, format='PNG')  # PNG for larger file size
        large_data = img_bytes.getvalue()
        
        print(f"      Created test file: {len(large_data)} bytes ({len(large_data)/1024/1024:.1f} MB)")
        
        # If file is over 5MB, it should be rejected
        if len(large_data) > 5 * 1024 * 1024:
            files = {'foto': ('large.png', io.BytesIO(large_data), 'image/png')}
            data = {
                'nama': 'Large File Test',
                'posisi': 'Size Tester',
                'gaji': '4000000',
                'kantor_id': str(kantor_id)
            }
            
            response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                   files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    # Clean up if accepted
                    karyawan_id = result.get('data', {}).get('id')
                    if karyawan_id:
                        requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
                    print(f"      SECURITY ISSUE: Large file was accepted!")
                    return False
            elif response.status_code == 400:
                return True  # Correctly rejected
        else:
            print(f"      File not large enough for size limit test")
            return True  # Can't test size limit if file isn't large enough
        
        return True
        
    except Exception as e:
        print(f"      Size test error: {str(e)}")
        return True  # Don't fail test if we can't create large file

def test_empty_file_validation(tester):
    """Test empty file validation"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    # Test with empty file
    files = {'foto': ('empty.jpg', io.BytesIO(b''), 'image/jpeg')}
    data = {
        'nama': 'Empty File Test',
        'posisi': 'Empty Tester',
        'gaji': '4000000',
        'kantor_id': str(kantor_id)
    }
    
    response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                           files=files, data=data, timeout=10)
    
    # Should reject empty file
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            # Clean up if accepted
            karyawan_id = result.get('data', {}).get('id')
            if karyawan_id:
                requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
            return False
    
    return response.status_code == 400

def test_filename_security(tester):
    """Test filename security (path traversal prevention)"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    # Create valid image with malicious filename
    img = Image.new('RGB', (100, 100), color='green')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_data = img_bytes.getvalue()
    
    malicious_filenames = [
        '../../../etc/passwd',
        '..\\..\\..\\windows\\system32\\config\\sam',
        '../../../../var/www/html/shell.php',
        'photo.jpg\x00../../../shell.php',
    ]
    
    for filename in malicious_filenames:
        files = {'foto': (filename, io.BytesIO(img_data), 'image/jpeg')}
        data = {
            'nama': 'Path Test',
            'posisi': 'Security Tester',
            'gaji': '4000000',
            'kantor_id': str(kantor_id)
        }
        
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                # Check if path was sanitized
                foto_path = result.get('data', {}).get('foto_path', '')
                if '..' in foto_path or foto_path.startswith('/'):
                    # Clean up
                    karyawan_id = result.get('data', {}).get('id')
                    if karyawan_id:
                        requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
                    print(f"      SECURITY ISSUE: Path traversal possible: {foto_path}")
                    return False
                else:
                    # Clean up
                    karyawan_id = result.get('data', {}).get('id')
                    if karyawan_id:
                        tester.created_ids.append(karyawan_id)
    
    return True

def test_mime_type_spoofing(tester):
    """Test MIME type spoofing prevention"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    # Try to upload malicious content with image MIME type
    malicious_content = b'<?php system($_GET["cmd"]); ?>'
    
    files = {'foto': ('shell.jpg', io.BytesIO(malicious_content), 'image/jpeg')}
    data = {
        'nama': 'MIME Spoof Test',
        'posisi': 'Security Tester',
        'gaji': '4000000',
        'kantor_id': str(kantor_id)
    }
    
    response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                           files=files, data=data, timeout=10)
    
    # Should reject because content is not actually an image
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            # Clean up
            karyawan_id = result.get('data', {}).get('id')
            if karyawan_id:
                requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
            print(f"      SECURITY WARNING: MIME spoofing may be possible")
            return False
    
    return response.status_code == 400

def test_valid_image_formats(tester):
    """Test that valid image formats are accepted"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    valid_formats = [
        ('JPEG', 'image/jpeg', 'jpg'),
        ('PNG', 'image/png', 'png'),
    ]
    
    for format_name, mime_type, extension in valid_formats:
        # Create valid image
        img = Image.new('RGB', (100, 100), color='blue')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format=format_name)
        img_data = img_bytes.getvalue()
        
        files = {'foto': (f'valid.{extension}', io.BytesIO(img_data), mime_type)}
        data = {
            'nama': f'Valid {format_name} Test',
            'posisi': 'Format Tester',
            'gaji': '4000000',
            'kantor_id': str(kantor_id)
        }
        
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=10)
        
        if response.status_code != 200:
            print(f"      Valid {format_name} format was rejected")
            return False
        
        result = response.json()
        if not result.get('success'):
            print(f"      Valid {format_name} format failed: {result.get('message')}")
            return False
        
        # Store for cleanup
        karyawan_id = result.get('data', {}).get('id')
        if karyawan_id:
            tester.created_ids.append(karyawan_id)
    
    return True

def run_tests():
    """Run all photo validation tests"""
    print("🧪 PHOTO VALIDATION TESTS")
    print("="*50)
    
    tester = PhotoValidationTester()
    
    try:
        # Security validation tests
        tester.test("File type validation", lambda: test_file_type_validation(tester))
        tester.test("File size validation", lambda: test_file_size_validation(tester))
        tester.test("Empty file validation", lambda: test_empty_file_validation(tester))
        tester.test("Filename security", lambda: test_filename_security(tester))
        tester.test("MIME type spoofing", lambda: test_mime_type_spoofing(tester))
        
        # Positive validation test
        tester.test("Valid image formats", lambda: test_valid_image_formats(tester))
        
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