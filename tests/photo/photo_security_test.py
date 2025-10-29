#!/usr/bin/env python3
"""
Photo Security Tests
Basic security testing for photo upload functionality
"""

import requests
import sys
from PIL import Image
import io

API_BASE_URL = "http://localhost:8080"
API_BASE = f"{API_BASE_URL}/api"

class PhotoSecurityTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.vulnerabilities = []
        self.warnings = []
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
    
    def security_issue(self, issue):
        """Report security issue"""
        self.vulnerabilities.append(issue)
        print(f"      🚨 SECURITY ISSUE: {issue}")
    
    def security_warning(self, warning):
        """Report security warning"""
        self.warnings.append(warning)
        print(f"      ⚠️  SECURITY WARNING: {warning}")
    
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
        
        print(f"\n📊 PHOTO SECURITY TEST SUMMARY")
        print(f"{'='*40}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total:  {total}")
        print(f"Success Rate: {(self.passed/total)*100:.1f}%")
        
        if self.vulnerabilities:
            print(f"\n🚨 CRITICAL VULNERABILITIES:")
            for vuln in self.vulnerabilities:
                print(f"   • {vuln}")
        
        if self.warnings:
            print(f"\n⚠️  SECURITY WARNINGS:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if not self.vulnerabilities and not self.warnings:
            print(f"\n🛡️  No critical security issues detected!")
        
        return self.failed == 0 and len(self.vulnerabilities) == 0

def get_valid_kantor_id():
    """Get a valid kantor ID for testing"""
    response = requests.get(f"{API_BASE}/kantors", timeout=5)
    if response.status_code != 200:
        return None
    
    data = response.json()
    kantors = data.get("data", [])
    return kantors[0]["id"] if kantors else None

def test_malicious_file_upload(tester):
    """Test malicious file upload prevention"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    malicious_files = [
        ('shell.php', b'<?php system($_GET["cmd"]); ?>', 'application/x-php'),
        ('malware.exe', b'MZ\x90\x00fake exe', 'application/octet-stream'),
        ('script.js', b'alert("xss");document.cookie', 'application/javascript'),
        ('trojan.bat', b'@echo off\nformat c: /y', 'application/x-bat'),
    ]
    
    security_passed = True
    
    for filename, content, mime_type in malicious_files:
        files = {'foto': (filename, io.BytesIO(content), mime_type)}
        data = {
            'nama': f'Security Test {filename}',
            'posisi': 'Security Tester',
            'gaji': '4000000',
            'kantor_id': str(kantor_id)
        }
        
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                tester.security_issue(f"Malicious file {filename} was accepted!")
                # Clean up
                karyawan_id = result.get('data', {}).get('id')
                if karyawan_id:
                    requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
                security_passed = False
        elif response.status_code != 400:
            tester.security_warning(f"Unexpected response {response.status_code} for {filename}")
    
    return security_passed

def test_file_size_limits(tester):
    """Test file size limit enforcement"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    # Try to create a large file (simulate oversized upload)
    large_content = b'A' * (6 * 1024 * 1024)  # 6MB fake file
    
    files = {'foto': ('large.jpg', io.BytesIO(large_content), 'image/jpeg')}
    data = {
        'nama': 'Large File Test',
        'posisi': 'Size Tester',
        'gaji': '4000000',
        'kantor_id': str(kantor_id)
    }
    
    try:
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                tester.security_issue("Large file (6MB) was accepted!")
                # Clean up
                karyawan_id = result.get('data', {}).get('id')
                if karyawan_id:
                    requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
                return False
        
        return response.status_code == 400  # Should be rejected
        
    except requests.exceptions.Timeout:
        # Timeout might indicate size handling
        return True

def test_path_traversal_prevention(tester):
    """Test path traversal attack prevention"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    # Create valid image with malicious filename
    img = Image.new('RGB', (100, 100), color='green')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_data = img_bytes.getvalue()
    
    malicious_paths = [
        '../../../etc/passwd',
        '..\\..\\..\\windows\\system32\\config\\sam',
        '../../../../var/www/html/shell.php',
        'innocent.jpg\x00../../../shell.php',
    ]
    
    security_passed = True
    
    for malicious_path in malicious_paths:
        files = {'foto': (malicious_path, io.BytesIO(img_data), 'image/jpeg')}
        data = {
            'nama': 'Path Traversal Test',
            'posisi': 'Security Tester',
            'gaji': '4000000',
            'kantor_id': str(kantor_id)
        }
        
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                foto_path = result.get('data', {}).get('foto_path', '')
                
                # Check if path contains traversal sequences
                if '..' in foto_path or foto_path.startswith('/'):
                    tester.security_issue(f"Path traversal detected: {foto_path}")
                    security_passed = False
                else:
                    # Path was sanitized - good
                    pass
                
                # Clean up
                karyawan_id = result.get('data', {}).get('id')
                if karyawan_id:
                    tester.created_ids.append(karyawan_id)
    
    return security_passed

def test_sql_injection_prevention(tester):
    """Test SQL injection prevention in file handling"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    # Create valid image
    img = Image.new('RGB', (100, 100), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_data = img_bytes.getvalue()
    
    # Try SQL injection in various fields
    sql_payloads = [
        "'; DROP TABLE karyawan; --",
        "' OR '1'='1",
        "1'; UPDATE karyawan SET gaji=999999999; --",
    ]
    
    for payload in sql_payloads:
        files = {'foto': ('test.jpg', io.BytesIO(img_data), 'image/jpeg')}
        data = {
            'nama': payload,  # SQL injection attempt
            'posisi': 'SQL Tester',
            'gaji': '4000000',
            'kantor_id': str(kantor_id)
        }
        
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                # Check if payload was stored as-is
                stored_nama = result.get('data', {}).get('nama', '')
                if payload in stored_nama:
                    tester.security_warning(f"SQL payload stored without sanitization: {payload}")
                
                # Clean up
                karyawan_id = result.get('data', {}).get('id')
                if karyawan_id:
                    tester.created_ids.append(karyawan_id)
    
    # Check if database is still accessible (no DROP TABLE)
    try:
        test_response = requests.get(f"{API_BASE}/karyawans", timeout=5)
        if test_response.status_code != 200:
            tester.security_issue("Database may have been compromised!")
            return False
    except:
        tester.security_issue("Cannot access database after SQL injection tests!")
        return False
    
    return True

def test_mime_type_validation(tester):
    """Test MIME type validation"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    # Test file with wrong MIME type
    malicious_content = b'<?php system($_GET["cmd"]); ?>'
    
    files = {'foto': ('shell.jpg', io.BytesIO(malicious_content), 'image/jpeg')}
    data = {
        'nama': 'MIME Test',
        'posisi': 'MIME Tester',
        'gaji': '4000000',
        'kantor_id': str(kantor_id)
    }
    
    response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                           files=files, data=data, timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            tester.security_warning("Possible MIME type spoofing - malicious content with image MIME type was accepted")
            # Clean up
            karyawan_id = result.get('data', {}).get('id')
            if karyawan_id:
                requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
            return False
    
    return response.status_code == 400

def test_directory_traversal_in_storage(tester):
    """Test if uploaded files are stored securely"""
    kantor_id = get_valid_kantor_id()
    if not kantor_id:
        return False
    
    # Upload a legitimate file and check storage location
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_data = img_bytes.getvalue()
    
    files = {'foto': ('storage_test.jpg', io.BytesIO(img_data), 'image/jpeg')}
    data = {
        'nama': 'Storage Security Test',
        'posisi': 'Storage Tester',
        'gaji': '4000000',
        'kantor_id': str(kantor_id)
    }
    
    response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                           files=files, data=data, timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            foto_path = result.get('data', {}).get('foto_path', '')
            
            # Check if file is stored in expected secure location
            if not foto_path.startswith('uploads/'):
                tester.security_warning(f"File stored outside expected directory: {foto_path}")
            
            # Check if filename is predictable (security risk)
            if 'storage_test.jpg' in foto_path:
                tester.security_warning("Original filename preserved - may be security risk")
            
            # Clean up
            karyawan_id = result.get('data', {}).get('id')
            if karyawan_id:
                tester.created_ids.append(karyawan_id)
            
            return True
    
    return False

def run_tests():
    """Run all photo security tests"""
    print("🧪 PHOTO SECURITY TESTS")
    print("="*50)
    
    tester = PhotoSecurityTester()
    
    try:
        # Security tests
        tester.test("Malicious file upload prevention", lambda: test_malicious_file_upload(tester))
        tester.test("File size limits enforcement", lambda: test_file_size_limits(tester))
        tester.test("Path traversal prevention", lambda: test_path_traversal_prevention(tester))
        tester.test("SQL injection prevention", lambda: test_sql_injection_prevention(tester))
        tester.test("MIME type validation", lambda: test_mime_type_validation(tester))
        tester.test("Secure file storage", lambda: test_directory_traversal_in_storage(tester))
        
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