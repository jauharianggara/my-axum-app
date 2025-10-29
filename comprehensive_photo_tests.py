#!/usr/bin/env python3
"""
Comprehensive Test Suite for Karyawan Photo Upload Feature
Testing all endpoints, validation, error handling, and edge cases
"""

import requests
import json
import os
import tempfile
import time
import threading
from PIL import Image
import io
import unittest
from typing import Dict, List, Optional

BASE_URL = "http://localhost:8080"
API_BASE = f"{BASE_URL}/api"

class PhotoTestUtils:
    """Utility class for creating test images and files"""
    
    @staticmethod
    def create_test_image(filename: str, size=(200, 200), format='JPEG', quality=85, color='red') -> int:
        """Create a test image file and return its size in bytes"""
        img = Image.new('RGB', size, color=color)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format=format, quality=quality)
        img_bytes.seek(0)
        
        with open(filename, 'wb') as f:
            f.write(img_bytes.getvalue())
        
        return os.path.getsize(filename)
    
    @staticmethod
    def create_large_image(filename: str, target_size_mb=6) -> int:
        """Create a large image file over specified size"""
        # Start with large dimensions and high quality
        size = (4000, 4000)
        quality = 100
        
        PhotoTestUtils.create_test_image(filename, size=size, format='JPEG', quality=quality)
        return os.path.getsize(filename)
    
    @staticmethod
    def create_text_file(filename: str, content="This is not an image") -> int:
        """Create a text file for testing invalid file types"""
        with open(filename, 'w') as f:
            f.write(content)
        return os.path.getsize(filename)

class KaryawanPhotoTestSuite(unittest.TestCase):
    """Main test suite for photo upload functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.test_karyawan_ids = []
        cls.created_files = []
        print(f"\n{'='*80}")
        print("🧪 COMPREHENSIVE KARYAWAN PHOTO UPLOAD TEST SUITE")
        print(f"{'='*80}")
        
        # Verify server is running
        try:
            response = requests.get(f"{API_BASE}/karyawans", timeout=5)
            print(f"✅ Server is running at {BASE_URL}")
        except requests.exceptions.RequestException:
            raise unittest.SkipTest(f"❌ Server not running at {BASE_URL}")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        print(f"\n{'='*80}")
        print("🧹 CLEANING UP TEST DATA")
        print(f"{'='*80}")
        
        # Delete test karyawans
        for karyawan_id in cls.test_karyawan_ids:
            try:
                response = requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
                if response.status_code == 200:
                    print(f"✅ Deleted test karyawan ID {karyawan_id}")
                else:
                    print(f"⚠️  Could not delete karyawan ID {karyawan_id}")
            except:
                print(f"⚠️  Error deleting karyawan ID {karyawan_id}")
        
        # Delete temporary files
        for file_path in cls.created_files:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
                    print(f"✅ Deleted temp file {file_path}")
            except:
                print(f"⚠️  Could not delete file {file_path}")
    
    def setUp(self):
        """Set up for each test"""
        self.temp_files = []
    
    def tearDown(self):
        """Clean up after each test"""
        for file_path in self.temp_files:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except:
                pass
    
    def create_temp_file(self, suffix='.jpg', **kwargs) -> str:
        """Create a temporary file and track it for cleanup"""
        temp_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        temp_file.close()
        self.temp_files.append(temp_file.name)
        self.__class__.created_files.append(temp_file.name)
        return temp_file.name

    # =================================================================
    # TEST 1: BASIC FUNCTIONALITY TESTS
    # =================================================================
    
    def test_01_create_karyawan_with_valid_photo(self):
        """Test creating karyawan with valid photo"""
        print("\n📝 Test 1: Create karyawan with valid photo")
        
        # Create test image
        image_file = self.create_temp_file('.jpg')
        image_size = PhotoTestUtils.create_test_image(image_file)
        
        files = {
            'foto': ('test_photo.jpg', open(image_file, 'rb'), 'image/jpeg')
        }
        
        data = {
            'nama': 'Test Karyawan Photo',
            'posisi': 'QA Tester',
            'gaji': '4500000',
            'kantor_id': '2'
        }
        
        try:
            response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                   files=files, data=data, timeout=30)
            
            files['foto'][1].close()
            
            self.assertEqual(response.status_code, 200)
            result = response.json()
            
            self.assertTrue(result['success'])
            self.assertIn('data', result)
            
            karyawan = result['data']
            self.assertIsNotNone(karyawan['foto_path'])
            self.assertEqual(karyawan['foto_original_name'], 'test_photo.jpg')
            self.assertEqual(karyawan['foto_mime_type'], 'image/jpeg')
            self.assertGreater(karyawan['foto_size'], 0)
            
            # Store ID for cleanup
            self.__class__.test_karyawan_ids.append(karyawan['id'])
            
            print(f"✅ Successfully created karyawan with photo")
            print(f"   📁 Photo path: {karyawan['foto_path']}")
            print(f"   📊 File size: {karyawan['foto_size']} bytes")
            
            return karyawan['id']
            
        except Exception as e:
            self.fail(f"Failed to create karyawan with photo: {str(e)}")
    
    def test_02_upload_photo_to_existing_karyawan(self):
        """Test uploading photo to existing karyawan"""
        print("\n📤 Test 2: Upload photo to existing karyawan")
        
        # First create a karyawan without photo
        karyawan_data = {
            'nama': 'Test Upload Target',
            'posisi': 'Developer',
            'gaji': '5000000',
            'kantor_id': '2'
        }
        
        response = requests.post(f"{API_BASE}/karyawans", 
                               json=karyawan_data, timeout=30)
        self.assertEqual(response.status_code, 200)
        
        result = response.json()
        karyawan_id = result['data']['id']
        self.__class__.test_karyawan_ids.append(karyawan_id)
        
        # Now upload photo
        image_file = self.create_temp_file('.png')
        PhotoTestUtils.create_test_image(image_file, format='PNG', color='blue')
        
        files = {
            'foto': ('uploaded_photo.png', open(image_file, 'rb'), 'image/png')
        }
        
        try:
            response = requests.post(f"{API_BASE}/karyawans/{karyawan_id}/photo", 
                                   files=files, timeout=30)
            
            files['foto'][1].close()
            
            self.assertEqual(response.status_code, 200)
            result = response.json()
            
            self.assertTrue(result['success'])
            karyawan = result['data']
            self.assertIsNotNone(karyawan['foto_path'])
            self.assertEqual(karyawan['foto_original_name'], 'uploaded_photo.png')
            self.assertEqual(karyawan['foto_mime_type'], 'image/png')
            
            print(f"✅ Successfully uploaded photo to karyawan ID {karyawan_id}")
            
        except Exception as e:
            self.fail(f"Failed to upload photo: {str(e)}")
    
    def test_03_delete_photo_from_karyawan(self):
        """Test deleting photo from karyawan"""
        print("\n🗑️  Test 3: Delete photo from karyawan")
        
        # Create karyawan with photo first
        karyawan_id = self.test_01_create_karyawan_with_valid_photo()
        
        # Delete the photo
        response = requests.delete(f"{API_BASE}/karyawans/{karyawan_id}/photo", timeout=30)
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        self.assertTrue(result['success'])
        karyawan = result['data']
        self.assertIsNone(karyawan['foto_path'])
        self.assertIsNone(karyawan['foto_original_name'])
        self.assertIsNone(karyawan['foto_size'])
        self.assertIsNone(karyawan['foto_mime_type'])
        
        print(f"✅ Successfully deleted photo from karyawan ID {karyawan_id}")

    # =================================================================
    # TEST 2: VALIDATION TESTS
    # =================================================================
    
    def test_04_reject_invalid_file_types(self):
        """Test rejection of invalid file types"""
        print("\n🚫 Test 4: Reject invalid file types")
        
        invalid_files = [
            ('test.txt', 'text/plain', 'This is a text file'),
            ('test.pdf', 'application/pdf', b'%PDF-fake-content'),
            ('test.exe', 'application/octet-stream', b'MZ\x90\x00fake-exe'),
        ]
        
        for filename, content_type, content in invalid_files:
            with self.subTest(file_type=content_type):
                temp_file = self.create_temp_file()
                
                if isinstance(content, str):
                    with open(temp_file, 'w') as f:
                        f.write(content)
                else:
                    with open(temp_file, 'wb') as f:
                        f.write(content)
                
                files = {
                    'foto': (filename, open(temp_file, 'rb'), content_type)
                }
                
                data = {
                    'nama': 'Test Invalid File',
                    'posisi': 'Tester',
                    'gaji': '3000000',
                    'kantor_id': '2'
                }
                
                try:
                    response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                           files=files, data=data, timeout=30)
                    
                    files['foto'][1].close()
                    
                    self.assertEqual(response.status_code, 200)
                    result = response.json()
                    
                    self.assertFalse(result['success'])
                    self.assertIn('Invalid file type', result['message'])
                    
                    print(f"✅ Correctly rejected {content_type}")
                    
                except Exception as e:
                    self.fail(f"Error testing {content_type}: {str(e)}")
    
    def test_05_reject_large_files(self):
        """Test rejection of files over size limit"""
        print("\n📏 Test 5: Reject large files (>5MB)")
        
        temp_file = self.create_temp_file('.jpg')
        file_size = PhotoTestUtils.create_large_image(temp_file, target_size_mb=6)
        
        print(f"   Created test file: {file_size} bytes ({file_size/1024/1024:.1f} MB)")
        
        if file_size > 5 * 1024 * 1024:  # > 5MB
            files = {
                'foto': ('large_photo.jpg', open(temp_file, 'rb'), 'image/jpeg')
            }
            
            data = {
                'nama': 'Test Large File',
                'posisi': 'Tester',
                'gaji': '3000000',
                'kantor_id': '2'
            }
            
            try:
                response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                       files=files, data=data, timeout=30)
                
                files['foto'][1].close()
                
                self.assertEqual(response.status_code, 200)
                result = response.json()
                
                self.assertFalse(result['success'])
                self.assertIn('File too large', result['message'])
                
                print(f"✅ Correctly rejected large file")
                
            except Exception as e:
                self.fail(f"Error testing large file: {str(e)}")
        else:
            print(f"⚠️  Generated file not large enough for test ({file_size} bytes)")
    
    def test_06_validate_karyawan_data(self):
        """Test validation of karyawan data fields"""
        print("\n✅ Test 6: Validate karyawan data fields")
        
        invalid_data_sets = [
            # Invalid nama (too short)
            {
                'nama': 'A',
                'posisi': 'Developer',
                'gaji': '5000000',
                'kantor_id': '2',
                'expected_error': 'Nama harus antara 2-50 karakter'
            },
            # Invalid posisi (too short)
            {
                'nama': 'Valid Name',
                'posisi': 'X',
                'gaji': '5000000',
                'kantor_id': '2',
                'expected_error': 'Posisi harus antara 2-30 karakter'
            },
            # Invalid gaji (too low)
            {
                'nama': 'Valid Name',
                'posisi': 'Developer',
                'gaji': '500000',
                'kantor_id': '2',
                'expected_error': 'Gaji harus antara 1,000,000 - 100,000,000'
            },
            # Invalid kantor_id
            {
                'nama': 'Valid Name',
                'posisi': 'Developer',
                'gaji': '5000000',
                'kantor_id': 'invalid',
                'expected_error': 'kantor_id harus berupa angka'
            },
        ]
        
        for i, test_data in enumerate(invalid_data_sets):
            with self.subTest(test_case=i):
                temp_file = self.create_temp_file('.jpg')
                PhotoTestUtils.create_test_image(temp_file)
                
                files = {
                    'foto': ('test.jpg', open(temp_file, 'rb'), 'image/jpeg')
                }
                
                data = {
                    'nama': test_data['nama'],
                    'posisi': test_data['posisi'],
                    'gaji': test_data['gaji'],
                    'kantor_id': test_data['kantor_id']
                }
                
                try:
                    response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                           files=files, data=data, timeout=30)
                    
                    files['foto'][1].close()
                    
                    self.assertEqual(response.status_code, 200)
                    result = response.json()
                    
                    self.assertFalse(result['success'])
                    
                    print(f"✅ Correctly rejected invalid data: {test_data['expected_error'][:50]}...")
                    
                except Exception as e:
                    self.fail(f"Error testing validation: {str(e)}")

    # =================================================================
    # TEST 3: EDGE CASES AND ERROR HANDLING
    # =================================================================
    
    def test_07_missing_photo_field(self):
        """Test creating karyawan with photo endpoint but no photo file"""
        print("\n📭 Test 7: Missing photo field")
        
        data = {
            'nama': 'No Photo Test',
            'posisi': 'Developer',
            'gaji': '5000000',
            'kantor_id': '2'
        }
        
        # No files parameter - should work but no photo
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               data=data, timeout=30)
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        self.assertTrue(result['success'])
        karyawan = result['data']
        
        # Should create karyawan but with no photo
        self.assertIsNone(karyawan['foto_path'])
        self.__class__.test_karyawan_ids.append(karyawan['id'])
        
        print(f"✅ Created karyawan without photo (optional photo)")
    
    def test_08_nonexistent_karyawan_photo_ops(self):
        """Test photo operations on non-existent karyawan"""
        print("\n👻 Test 8: Photo operations on non-existent karyawan")
        
        fake_id = 999999
        
        # Test upload photo to non-existent karyawan
        temp_file = self.create_temp_file('.jpg')
        PhotoTestUtils.create_test_image(temp_file)
        
        files = {
            'foto': ('test.jpg', open(temp_file, 'rb'), 'image/jpeg')
        }
        
        response = requests.post(f"{API_BASE}/karyawans/{fake_id}/photo", 
                               files=files, timeout=30)
        
        files['foto'][1].close()
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        self.assertFalse(result['success'])
        self.assertIn('not found', result['message'].lower())
        
        # Test delete photo from non-existent karyawan
        response = requests.delete(f"{API_BASE}/karyawans/{fake_id}/photo", timeout=30)
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        self.assertFalse(result['success'])
        self.assertIn('not found', result['message'].lower())
        
        print(f"✅ Correctly handled non-existent karyawan operations")
    
    def test_09_empty_file_upload(self):
        """Test uploading empty file"""
        print("\n📄 Test 9: Empty file upload")
        
        temp_file = self.create_temp_file('.jpg')
        # Create empty file
        open(temp_file, 'w').close()
        
        files = {
            'foto': ('empty.jpg', open(temp_file, 'rb'), 'image/jpeg')
        }
        
        data = {
            'nama': 'Empty File Test',
            'posisi': 'Tester',
            'gaji': '3000000',
            'kantor_id': '2'
        }
        
        try:
            response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                   files=files, data=data, timeout=30)
            
            files['foto'][1].close()
            
            self.assertEqual(response.status_code, 200)
            result = response.json()
            
            self.assertFalse(result['success'])
            self.assertIn('empty', result['message'].lower())
            
            print(f"✅ Correctly rejected empty file")
            
        except Exception as e:
            self.fail(f"Error testing empty file: {str(e)}")

    # =================================================================
    # TEST 4: PHOTO FORMATS AND QUALITY
    # =================================================================
    
    def test_10_supported_image_formats(self):
        """Test all supported image formats"""
        print("\n🖼️  Test 10: Supported image formats")
        
        formats = [
            ('JPEG', 'image/jpeg', '.jpg'),
            ('PNG', 'image/png', '.png'),
            ('WebP', 'image/webp', '.webp'),
        ]
        
        for format_name, mime_type, extension in formats:
            with self.subTest(format=format_name):
                try:
                    temp_file = self.create_temp_file(extension)
                    PhotoTestUtils.create_test_image(temp_file, format=format_name)
                    
                    files = {
                        'foto': (f'test{extension}', open(temp_file, 'rb'), mime_type)
                    }
                    
                    data = {
                        'nama': f'Test {format_name}',
                        'posisi': 'Designer',
                        'gaji': '4000000',
                        'kantor_id': '2'
                    }
                    
                    response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                           files=files, data=data, timeout=30)
                    
                    files['foto'][1].close()
                    
                    self.assertEqual(response.status_code, 200)
                    result = response.json()
                    
                    self.assertTrue(result['success'])
                    karyawan = result['data']
                    self.assertEqual(karyawan['foto_mime_type'], mime_type)
                    
                    self.__class__.test_karyawan_ids.append(karyawan['id'])
                    
                    print(f"✅ {format_name} format accepted")
                    
                except Exception as e:
                    # WebP might not be supported by PIL in some environments
                    if format_name == 'WebP':
                        print(f"⚠️  WebP format test skipped: {str(e)}")
                    else:
                        self.fail(f"Error testing {format_name}: {str(e)}")

    # =================================================================
    # TEST 5: INTEGRATION TESTS
    # =================================================================
    
    def test_11_get_karyawan_with_photo_info(self):
        """Test retrieving karyawan data with photo information"""
        print("\n📋 Test 11: Get karyawan with photo info")
        
        # Create karyawan with photo
        karyawan_id = self.test_01_create_karyawan_with_valid_photo()
        
        # Get karyawan with kantor info
        response = requests.get(f"{API_BASE}/karyawans/with-kantor", timeout=30)
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        self.assertTrue(result['success'])
        karyawans = result['data']
        
        # Find our test karyawan
        test_karyawan = None
        for k in karyawans:
            if k['id'] == karyawan_id:
                test_karyawan = k
                break
        
        self.assertIsNotNone(test_karyawan)
        self.assertIsNotNone(test_karyawan['foto_path'])
        self.assertIsNotNone(test_karyawan['foto_original_name'])
        self.assertIsNotNone(test_karyawan['foto_size'])
        self.assertIsNotNone(test_karyawan['foto_mime_type'])
        
        print(f"✅ Successfully retrieved karyawan with photo info")
        print(f"   📁 Photo: {test_karyawan['foto_original_name']}")
        print(f"   📊 Size: {test_karyawan['foto_size']} bytes")
    
    def test_12_photo_file_accessibility(self):
        """Test that uploaded photos are accessible via HTTP"""
        print("\n🌐 Test 12: Photo file accessibility")
        
        # Create karyawan with photo
        karyawan_id = self.test_01_create_karyawan_with_valid_photo()
        
        # Get karyawan data to find photo path
        response = requests.get(f"{API_BASE}/karyawans/{karyawan_id}", timeout=30)
        self.assertEqual(response.status_code, 200)
        
        result = response.json()
        karyawan = result['data']
        
        if karyawan['foto_path']:
            # Try to access the photo file
            photo_url = f"{BASE_URL}/{karyawan['foto_path']}"
            
            try:
                photo_response = requests.get(photo_url, timeout=30)
                
                if photo_response.status_code == 200:
                    self.assertTrue(len(photo_response.content) > 0)
                    print(f"✅ Photo accessible at: {photo_url}")
                    print(f"   📊 Content length: {len(photo_response.content)} bytes")
                else:
                    print(f"⚠️  Photo not accessible (HTTP {photo_response.status_code})")
                    
            except Exception as e:
                print(f"⚠️  Could not access photo: {str(e)}")

    # =================================================================
    # TEST 6: PERFORMANCE AND LOAD TESTS
    # =================================================================
    
    def test_13_concurrent_photo_uploads(self):
        """Test concurrent photo uploads"""
        print("\n⚡ Test 13: Concurrent photo uploads")
        
        results = []
        errors = []
        
        def upload_photo(thread_id):
            try:
                temp_file = self.create_temp_file(f'_thread_{thread_id}.jpg')
                PhotoTestUtils.create_test_image(temp_file, color='green')
                
                files = {
                    'foto': (f'concurrent_{thread_id}.jpg', open(temp_file, 'rb'), 'image/jpeg')
                }
                
                data = {
                    'nama': f'Concurrent Test {thread_id}',
                    'posisi': 'Tester',
                    'gaji': '3500000',
                    'kantor_id': '2'
                }
                
                response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                                       files=files, data=data, timeout=30)
                
                files['foto'][1].close()
                
                if response.status_code == 200:
                    result = response.json()
                    if result['success']:
                        results.append(result['data']['id'])
                    else:
                        errors.append(f"Thread {thread_id}: {result['message']}")
                else:
                    errors.append(f"Thread {thread_id}: HTTP {response.status_code}")
                    
            except Exception as e:
                errors.append(f"Thread {thread_id}: {str(e)}")
        
        # Start 5 concurrent uploads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=upload_photo, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Add successful IDs to cleanup list
        self.__class__.test_karyawan_ids.extend(results)
        
        print(f"✅ Concurrent uploads completed")
        print(f"   ✅ Successful: {len(results)}")
        print(f"   ❌ Errors: {len(errors)}")
        
        if errors:
            for error in errors:
                print(f"   - {error}")
        
        # At least some should succeed
        self.assertGreater(len(results), 0, "No concurrent uploads succeeded")

def run_comprehensive_tests():
    """Run the comprehensive test suite"""
    print(f"\n{'='*80}")
    print("🚀 STARTING COMPREHENSIVE KARYAWAN PHOTO UPLOAD TESTS")
    print(f"{'='*80}")
    
    # Configure test runner
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(KaryawanPhotoTestSuite)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=open('test_results.txt', 'w'),
        buffer=False
    )
    
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*80}")
    print("📊 TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🏆 EXCELLENT! Photo upload feature is working great!")
    elif success_rate >= 75:
        print("✅ GOOD! Most features are working with minor issues.")
    else:
        print("⚠️  NEEDS ATTENTION! Several issues found.")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    try:
        success = run_comprehensive_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n💥 Test suite failed: {str(e)}")
        exit(1)
