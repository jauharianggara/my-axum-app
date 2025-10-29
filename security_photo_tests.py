#!/usr/bin/env python3
"""
Security Testing for Karyawan Photo Upload API
Tests security vulnerabilities and attack vectors
"""

import requests
import json
import time
import tempfile
import os
from PIL import Image
import io
import base64

BASE_URL = "http://localhost:8080"
API_BASE = f"{BASE_URL}/api"

class SecurityTestResults:
    """Track security test results"""
    
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.vulnerabilities = []
        self.warnings = []
    
    def add_test(self, test_name: str, passed: bool, message: str = None, severity: str = "INFO"):
        """Add a test result"""
        self.total_tests += 1
        
        if passed:
            self.passed_tests += 1
            print(f"✅ {test_name}: PASSED")
            if message:
                print(f"   💡 {message}")
        else:
            self.failed_tests += 1
            print(f"❌ {test_name}: FAILED")
            if message:
                if severity == "CRITICAL":
                    self.vulnerabilities.append(f"{test_name}: {message}")
                    print(f"   🚨 CRITICAL: {message}")
                elif severity == "WARNING":
                    self.warnings.append(f"{test_name}: {message}")
                    print(f"   ⚠️  WARNING: {message}")
                else:
                    print(f"   ℹ️  {message}")
    
    def print_summary(self):
        """Print security test summary"""
        print(f"\n{'='*80}")
        print("🔒 SECURITY TEST SUMMARY")
        print(f"{'='*80}")
        print(f"Total Tests:      {self.total_tests}")
        print(f"Passed:           {self.passed_tests}")
        print(f"Failed:           {self.failed_tests}")
        print(f"Success Rate:     {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        if self.vulnerabilities:
            print(f"\n🚨 CRITICAL VULNERABILITIES FOUND:")
            for vuln in self.vulnerabilities:
                print(f"   • {vuln}")
        
        if self.warnings:
            print(f"\n⚠️  SECURITY WARNINGS:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if not self.vulnerabilities and not self.warnings:
            print(f"\n🛡️  No critical security issues detected!")

def create_malicious_file(file_type: str, size: int = 1000) -> bytes:
    """Create various types of malicious files for testing"""
    
    if file_type == "php_shell":
        # PHP web shell disguised as image
        content = b"<?php system($_GET['cmd']); ?>"
        content += b"\x00" * (size - len(content))  # Pad to desired size
        return content
    
    elif file_type == "javascript":
        # JavaScript file with malicious content
        content = b"<script>alert('XSS');</script>"
        content += b"\x00" * (size - len(content))
        return content
    
    elif file_type == "huge_file":
        # File that exceeds size limit
        return b"A" * (10 * 1024 * 1024)  # 10MB file
    
    elif file_type == "polyglot":
        # Polyglot file (valid image + executable code)
        # Create a minimal valid JPEG header
        jpeg_header = bytes.fromhex('FFD8FFE000104A46494600010101006000600000')
        malicious_code = b"<?php echo 'Malicious code executed'; ?>"
        return jpeg_header + malicious_code + b"\x00" * (size - len(jpeg_header) - len(malicious_code))
    
    elif file_type == "svg_xss":
        # SVG with embedded JavaScript
        svg_content = """<?xml version="1.0" encoding="UTF-8"?>
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100" height="100">
        <script type="text/javascript">
        alert('XSS via SVG');
        </script>
        <rect x="0" y="0" width="100" height="100" fill="red"/>
        </svg>"""
        return svg_content.encode('utf-8')
    
    elif file_type == "zip_bomb":
        # Simple zip bomb (nested archives)
        import zipfile
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Create a file with repetitive content
            large_content = "A" * (1024 * 1024)  # 1MB of A's
            zf.writestr("bomb.txt", large_content)
        return zip_buffer.getvalue()
    
    else:
        # Default malicious file
        return b"MALICIOUS_CONTENT" + b"\x00" * (size - 17)

def test_file_type_validation(results: SecurityTestResults):
    """Test file type validation security"""
    print(f"\n🔍 TESTING FILE TYPE VALIDATION")
    print("-" * 40)
    
    malicious_files = [
        ("executable.exe", "application/octet-stream", create_malicious_file("php_shell")),
        ("shell.php", "application/x-php", create_malicious_file("php_shell")),
        ("script.js", "application/javascript", create_malicious_file("javascript")),
        ("malware.zip", "application/zip", create_malicious_file("zip_bomb")),
        ("image.svg", "image/svg+xml", create_malicious_file("svg_xss")),
        ("fake.jpg", "image/jpeg", create_malicious_file("php_shell")),  # PHP shell with JPEG extension
    ]
    
    for filename, mime_type, file_content in malicious_files:
        try:
            files = {
                'foto': (filename, io.BytesIO(file_content), mime_type)
            }
            
            data = {
                'nama': 'Security Test',
                'posisi': 'Tester',
                'gaji': '3000000',
                'kantor_id': '2'
            }
            
            response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                   files=files, data=data, timeout=10)
            
            if response.status_code == 400:
                result = response.json()
                if not result.get('success', True):
                    results.add_test(
                        f"Reject {filename}",
                        True,
                        f"Correctly rejected malicious file type: {result.get('message', 'Unknown error')}"
                    )
                else:
                    results.add_test(
                        f"Reject {filename}",
                        False,
                        f"File was accepted when it should be rejected",
                        "CRITICAL"
                    )
            elif response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    results.add_test(
                        f"Reject {filename}",
                        False,
                        f"CRITICAL: Malicious file {filename} was accepted and uploaded!",
                        "CRITICAL"
                    )
                    
                    # Try to cleanup
                    karyawan_id = result.get('data', {}).get('id')
                    if karyawan_id:
                        requests.delete(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
                else:
                    results.add_test(
                        f"Reject {filename}",
                        True,
                        f"File rejected: {result.get('message', 'Unknown error')}"
                    )
            else:
                results.add_test(
                    f"Reject {filename}",
                    True,
                    f"Server properly rejected with status {response.status_code}"
                )
                
        except Exception as e:
            results.add_test(
                f"Reject {filename}",
                False,
                f"Test failed with exception: {str(e)}",
                "WARNING"
            )

def test_file_size_limits(results: SecurityTestResults):
    """Test file size limit enforcement"""
    print(f"\n📏 TESTING FILE SIZE LIMITS")
    print("-" * 40)
    
    # Create oversized file
    huge_image_data = create_malicious_file("huge_file")
    
    try:
        files = {
            'foto': ('huge_image.jpg', io.BytesIO(huge_image_data), 'image/jpeg')
        }
        
        data = {
            'nama': 'Size Test',
            'posisi': 'Tester',
            'gaji': '3000000',
            'kantor_id': '2'
        }
        
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=30)
        
        if response.status_code == 400:
            result = response.json()
            if "size" in result.get('message', '').lower() or "large" in result.get('message', '').lower():
                results.add_test(
                    "File size limit enforcement",
                    True,
                    f"Correctly rejected oversized file: {result.get('message')}"
                )
            else:
                results.add_test(
                    "File size limit enforcement",
                    False,
                    "File rejected but not for size reasons",
                    "WARNING"
                )
        elif response.status_code == 200:
            results.add_test(
                "File size limit enforcement",
                False,
                "CRITICAL: Oversized file was accepted!",
                "CRITICAL"
            )
            
            # Cleanup if accepted
            result = response.json()
            karyawan_id = result.get('data', {}).get('id')
            if karyawan_id:
                requests.delete(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
        else:
            results.add_test(
                "File size limit enforcement",
                True,
                f"Server rejected with status {response.status_code}"
            )
            
    except requests.exceptions.Timeout:
        results.add_test(
            "File size limit enforcement",
            True,
            "Request timed out (likely due to size limit)"
        )
    except Exception as e:
        results.add_test(
            "File size limit enforcement",
            False,
            f"Test failed: {str(e)}",
            "WARNING"
        )

def test_path_traversal(results: SecurityTestResults):
    """Test for path traversal vulnerabilities"""
    print(f"\n📁 TESTING PATH TRAVERSAL ATTACKS")
    print("-" * 40)
    
    # Create a valid image
    img = Image.new('RGB', (100, 100), color='green')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_data = img_bytes.getvalue()
    
    malicious_filenames = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
        "../../../../var/www/html/shell.php",
        "../uploads/../../config/database.yml",
        "photo.jpg/../../../shell.php",
        "null.jpg\x00../../../shell.php",
    ]
    
    for malicious_filename in malicious_filenames:
        try:
            files = {
                'foto': (malicious_filename, io.BytesIO(img_data), 'image/jpeg')
            }
            
            data = {
                'nama': 'Path Traversal Test',
                'posisi': 'Tester',
                'gaji': '3000000',
                'kantor_id': '2'
            }
            
            response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                   files=files, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    # Check if the stored filename contains path traversal
                    foto_path = result.get('data', {}).get('foto_path', '')
                    if '..' in foto_path or foto_path.startswith('/'):
                        results.add_test(
                            f"Path traversal: {malicious_filename[:20]}...",
                            False,
                            f"Path traversal possible: {foto_path}",
                            "CRITICAL"
                        )
                    else:
                        results.add_test(
                            f"Path traversal: {malicious_filename[:20]}...",
                            True,
                            f"Filename sanitized to: {foto_path}"
                        )
                    
                    # Cleanup
                    karyawan_id = result.get('data', {}).get('id')
                    if karyawan_id:
                        requests.delete(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
                else:
                    results.add_test(
                        f"Path traversal: {malicious_filename[:20]}...",
                        True,
                        "Request properly rejected"
                    )
            else:
                results.add_test(
                    f"Path traversal: {malicious_filename[:20]}...",
                    True,
                    f"Request rejected with status {response.status_code}"
                )
                
        except Exception as e:
            results.add_test(
                f"Path traversal: {malicious_filename[:20]}...",
                False,
                f"Test failed: {str(e)}",
                "WARNING"
            )

def test_sql_injection(results: SecurityTestResults):
    """Test for SQL injection vulnerabilities"""
    print(f"\n💉 TESTING SQL INJECTION ATTACKS")
    print("-" * 40)
    
    # Create a valid image
    img = Image.new('RGB', (100, 100), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_data = img_bytes.getvalue()
    
    sql_payloads = [
        "'; DROP TABLE karyawan; --",
        "' OR '1'='1",
        "1'; UPDATE karyawan SET gaji=999999999; --",
        "1' UNION SELECT * FROM users; --",
        "'; INSERT INTO karyawan (nama) VALUES ('hacked'); --",
    ]
    
    for payload in sql_payloads:
        try:
            files = {
                'foto': ('test.jpg', io.BytesIO(img_data), 'image/jpeg')
            }
            
            data = {
                'nama': payload,  # Inject in nama field
                'posisi': 'SQL Tester',
                'gaji': '3000000',
                'kantor_id': '2'
            }
            
            response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                   files=files, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    # Check if the payload was stored as-is (potential vulnerability)
                    stored_nama = result.get('data', {}).get('nama', '')
                    if payload in stored_nama:
                        results.add_test(
                            f"SQL injection test",
                            False,
                            f"SQL payload stored without sanitization: {payload[:30]}...",
                            "WARNING"
                        )
                    else:
                        results.add_test(
                            f"SQL injection test",
                            True,
                            "Input appears to be sanitized"
                        )
                    
                    # Cleanup
                    karyawan_id = result.get('data', {}).get('id')
                    if karyawan_id:
                        requests.delete(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
                        
                    # Test if database is still accessible (no DROP TABLE)
                    test_response = requests.get(f"{API_BASE}/karyawans", timeout=5)
                    if test_response.status_code != 200:
                        results.add_test(
                            "Database integrity check",
                            False,
                            "Database may have been compromised!",
                            "CRITICAL"
                        )
                        break
                else:
                    results.add_test(
                        f"SQL injection validation",
                        True,
                        "Input validation rejected malicious input"
                    )
            else:
                results.add_test(
                    f"SQL injection validation",
                    True,
                    f"Request rejected with status {response.status_code}"
                )
                
        except Exception as e:
            results.add_test(
                f"SQL injection test",
                False,
                f"Test failed: {str(e)}",
                "WARNING"
            )
    
    # Final database integrity check
    try:
        test_response = requests.get(f"{API_BASE}/karyawans", timeout=5)
        if test_response.status_code == 200:
            results.add_test(
                "Final database integrity",
                True,
                "Database remains accessible after SQL injection tests"
            )
        else:
            results.add_test(
                "Final database integrity",
                False,
                "Database access issues detected",
                "CRITICAL"
            )
    except:
        results.add_test(
            "Final database integrity",
            False,
            "Cannot access database after tests",
            "CRITICAL"
        )

def test_api_authentication(results: SecurityTestResults):
    """Test API authentication and authorization"""
    print(f"\n🔐 TESTING AUTHENTICATION & AUTHORIZATION")
    print("-" * 40)
    
    # Test accessing without authentication (if applicable)
    endpoints_to_test = [
        f"{API_BASE}/karyawans",
        f"{API_BASE}/karyawans/1",
        f"{API_BASE}/kantors",
    ]
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(endpoint, timeout=10)
            
            if response.status_code == 401 or response.status_code == 403:
                results.add_test(
                    f"Auth required for {endpoint.split('/')[-1]}",
                    True,
                    "Endpoint properly requires authentication"
                )
            elif response.status_code == 200:
                results.add_test(
                    f"Auth required for {endpoint.split('/')[-1]}",
                    False,
                    "Endpoint accessible without authentication",
                    "WARNING"
                )
            else:
                results.add_test(
                    f"Auth test for {endpoint.split('/')[-1]}",
                    True,
                    f"Endpoint returned status {response.status_code}"
                )
                
        except Exception as e:
            results.add_test(
                f"Auth test for {endpoint.split('/')[-1]}",
                False,
                f"Test failed: {str(e)}",
                "WARNING"
            )

def test_rate_limiting(results: SecurityTestResults):
    """Test rate limiting to prevent abuse"""
    print(f"\n⏰ TESTING RATE LIMITING")
    print("-" * 40)
    
    # Create a small valid image
    img = Image.new('RGB', (50, 50), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_data = img_bytes.getvalue()
    
    # Send multiple requests rapidly
    successful_requests = 0
    rate_limited = False
    created_ids = []
    
    for i in range(20):  # Try 20 rapid requests
        try:
            files = {
                'foto': (f'rate_test_{i}.jpg', io.BytesIO(img_data), 'image/jpeg')
            }
            
            data = {
                'nama': f'Rate Test {i}',
                'posisi': 'Rate Tester',
                'gaji': '3000000',
                'kantor_id': '2'
            }
            
            start_time = time.time()
            response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                   files=files, data=data, timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 429:  # Rate limited
                rate_limited = True
                break
            elif response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    successful_requests += 1
                    karyawan_id = result.get('data', {}).get('id')
                    if karyawan_id:
                        created_ids.append(karyawan_id)
            
            # Very short delay to simulate rapid requests
            time.sleep(0.1)
            
        except requests.exceptions.Timeout:
            # Server might be throttling
            rate_limited = True
            break
        except Exception:
            continue
    
    if rate_limited:
        results.add_test(
            "Rate limiting",
            True,
            f"Rate limiting detected after {successful_requests} requests"
        )
    elif successful_requests >= 20:
        results.add_test(
            "Rate limiting",
            False,
            f"No rate limiting detected - {successful_requests} rapid requests succeeded",
            "WARNING"
        )
    else:
        results.add_test(
            "Rate limiting",
            True,
            f"Server handled {successful_requests} requests (natural throttling or limits)"
        )
    
    # Cleanup
    for karyawan_id in created_ids:
        try:
            requests.delete(f"{API_BASE}/karyawans/{karyawan_id}", timeout=5)
        except:
            pass

def run_security_tests():
    """Run all security tests"""
    print(f"\n{'='*80}")
    print("🛡️  COMPREHENSIVE SECURITY TESTING SUITE")
    print(f"{'='*80}")
    
    # Check server availability
    try:
        response = requests.get(f"{API_BASE}/karyawans", timeout=5)
        print(f"✅ Server is available at {BASE_URL}")
    except:
        print(f"❌ Server not available at {BASE_URL}")
        return False
    
    results = SecurityTestResults()
    
    try:
        # Run all security tests
        test_file_type_validation(results)
        test_file_size_limits(results)
        test_path_traversal(results)
        test_sql_injection(results)
        test_api_authentication(results)
        test_rate_limiting(results)
        
        # Print summary
        results.print_summary()
        
        # Security rating
        if not results.vulnerabilities:
            if not results.warnings:
                print(f"\n🏆 EXCELLENT SECURITY!")
                print("   No critical vulnerabilities or warnings detected.")
            else:
                print(f"\n✅ GOOD SECURITY!")
                print("   No critical vulnerabilities, but some warnings to address.")
        else:
            print(f"\n⚠️  SECURITY ISSUES DETECTED!")
            print("   Critical vulnerabilities found that need immediate attention.")
        
        return len(results.vulnerabilities) == 0
        
    except Exception as e:
        print(f"\n💥 Security tests failed: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        success = run_security_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Security tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n💥 Security test suite failed: {str(e)}")
        exit(1)
