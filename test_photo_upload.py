#!/usr/bin/env python3
"""
Comprehensive API Testing for Karyawan Photo Upload Feature
Test file upload functionality with validation
"""

import requests
import json
import os
import tempfile
from PIL import Image
import io

BASE_URL = "http://localhost:8080"

def create_test_image(filename, size=(200, 200), format='JPEG', quality=85):
    """Create a test image file"""
    # Create a simple colored image
    img = Image.new('RGB', size, color='red')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=format, quality=quality)
    img_bytes.seek(0)
    
    # Write to file
    with open(filename, 'wb') as f:
        f.write(img_bytes.getvalue())
    
    return os.path.getsize(filename)

def test_create_karyawan_with_photo():
    """Test creating karyawan with photo upload"""
    print("\n=== Testing Create Karyawan with Photo ===")
    
    # Create test image
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        image_size = create_test_image(temp_file.name)
        print(f"✅ Created test image: {temp_file.name} ({image_size} bytes)")
        
        # Prepare multipart data
        files = {
            'foto': ('test_photo.jpg', open(temp_file.name, 'rb'), 'image/jpeg')
        }
        
        data = {
            'nama': 'Test Karyawan Photo',
            'posisi': 'Developer',
            'gaji': '5000000',
            'kantor_id': '1'
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/karyawans/with-photo", 
                files=files,
                data=data,
                timeout=30
            )
            
            files['foto'][1].close()  # Close file handle
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response: {json.dumps(result, indent=2, default=str)}")
                
                if result.get('success'):
                    karyawan_data = result.get('data')
                    if karyawan_data and karyawan_data.get('foto_path'):
                        print(f"✅ Photo uploaded successfully!")
                        print(f"   📁 File path: {karyawan_data['foto_path']}")
                        print(f"   📄 Original name: {karyawan_data['foto_original_name']}")
                        print(f"   📊 File size: {karyawan_data['foto_size']} bytes")
                        print(f"   🎭 MIME type: {karyawan_data['foto_mime_type']}")
                        return karyawan_data['id']  # Return ID for further tests
                    else:
                        print("❌ Photo data missing in response")
                else:
                    print(f"❌ API Error: {result.get('message')}")
                    if result.get('errors'):
                        for error in result['errors']:
                            print(f"   - {error}")
            else:
                print(f"❌ HTTP Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file.name)
            except:
                pass
    
    return None

def test_upload_photo_to_existing_karyawan(karyawan_id):
    """Test uploading photo to existing karyawan"""
    if not karyawan_id:
        print("❌ No karyawan ID provided for photo upload test")
        return
        
    print(f"\n=== Testing Upload Photo to Karyawan ID {karyawan_id} ===")
    
    # Create a different test image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        image_size = create_test_image(temp_file.name, size=(300, 300), format='PNG')
        print(f"✅ Created test image: {temp_file.name} ({image_size} bytes)")
        
        files = {
            'foto': ('updated_photo.png', open(temp_file.name, 'rb'), 'image/png')
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/karyawans/{karyawan_id}/photo", 
                files=files,
                timeout=30
            )
            
            files['foto'][1].close()
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response: {json.dumps(result, indent=2, default=str)}")
                
                if result.get('success'):
                    karyawan_data = result.get('data')
                    print(f"✅ Photo updated successfully!")
                    print(f"   📁 New file path: {karyawan_data['foto_path']}")
                    print(f"   📄 New original name: {karyawan_data['foto_original_name']}")
                else:
                    print(f"❌ API Error: {result.get('message')}")
            else:
                print(f"❌ HTTP Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        finally:
            try:
                os.unlink(temp_file.name)
            except:
                pass

def test_delete_photo(karyawan_id):
    """Test deleting karyawan photo"""
    if not karyawan_id:
        print("❌ No karyawan ID provided for photo deletion test")
        return
        
    print(f"\n=== Testing Delete Photo from Karyawan ID {karyawan_id} ===")
    
    try:
        response = requests.delete(
            f"{BASE_URL}/api/karyawans/{karyawan_id}/photo",
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {json.dumps(result, indent=2, default=str)}")
            
            if result.get('success'):
                karyawan_data = result.get('data')
                print(f"✅ Photo deleted successfully!")
                print(f"   📁 Photo path: {karyawan_data.get('foto_path', 'None')}")
            else:
                print(f"❌ API Error: {result.get('message')}")
        else:
            print(f"❌ HTTP Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_invalid_file_types():
    """Test uploading invalid file types"""
    print("\n=== Testing Invalid File Types ===")
    
    # Test text file
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
        temp_file.write(b"This is not an image")
        temp_file.flush()
        
        files = {
            'foto': ('test.txt', open(temp_file.name, 'rb'), 'text/plain')
        }
        
        data = {
            'nama': 'Test Invalid File',
            'posisi': 'Tester',
            'gaji': '3000000',
            'kantor_id': '1'
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/karyawans/with-photo", 
                files=files,
                data=data,
                timeout=30
            )
            
            files['foto'][1].close()
            
            print(f"Status: {response.status_code}")
            result = response.json()
            
            if not result.get('success'):
                print(f"✅ Correctly rejected invalid file type")
                print(f"   Error: {result.get('message')}")
                if result.get('errors'):
                    for error in result['errors']:
                        print(f"   - {error}")
            else:
                print(f"❌ Should have rejected invalid file type")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        finally:
            try:
                os.unlink(temp_file.name)
            except:
                pass

def test_large_file():
    """Test uploading large file (over 5MB limit)"""
    print("\n=== Testing Large File Upload (>5MB) ===")
    
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        # Create large image
        image_size = create_test_image(temp_file.name, size=(3000, 3000), quality=100)
        print(f"✅ Created large test image: {temp_file.name} ({image_size} bytes)")
        
        if image_size > 5 * 1024 * 1024:  # > 5MB
            files = {
                'foto': ('large_photo.jpg', open(temp_file.name, 'rb'), 'image/jpeg')
            }
            
            data = {
                'nama': 'Test Large File',
                'posisi': 'Tester',
                'gaji': '3000000',
                'kantor_id': '1'
            }
            
            try:
                response = requests.post(
                    f"{BASE_URL}/api/karyawans/with-photo", 
                    files=files,
                    data=data,
                    timeout=30
                )
                
                files['foto'][1].close()
                
                print(f"Status: {response.status_code}")
                result = response.json()
                
                if not result.get('success'):
                    print(f"✅ Correctly rejected large file")
                    print(f"   Error: {result.get('message')}")
                else:
                    print(f"❌ Should have rejected large file")
                    
            except Exception as e:
                print(f"❌ Exception: {str(e)}")
            finally:
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
        else:
            print(f"⚠️  Image not large enough for test ({image_size} bytes)")

def test_get_karyawan_with_photo():
    """Test retrieving karyawan data including photo info"""
    print("\n=== Testing Get Karyawan with Photo Info ===")
    
    try:
        response = requests.get(f"{BASE_URL}/api/karyawans/with-kantor", timeout=30)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                karyawans = result.get('data', [])
                print(f"✅ Retrieved {len(karyawans)} karyawans")
                
                # Show karyawans with photos
                photo_count = 0
                for karyawan in karyawans:
                    if karyawan.get('foto_path'):
                        photo_count += 1
                        print(f"   📷 {karyawan['nama']} has photo: {karyawan['foto_path']}")
                
                print(f"✅ Found {photo_count} karyawans with photos")
            else:
                print(f"❌ API Error: {result.get('message')}")
        else:
            print(f"❌ HTTP Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def main():
    """Run all photo-related tests"""
    print("🔍 Starting Karyawan Photo Upload API Tests")
    print("=" * 50)
    
    # Test 1: Create karyawan with photo
    karyawan_id = test_create_karyawan_with_photo()
    
    # Test 2: Upload photo to existing karyawan
    if karyawan_id:
        test_upload_photo_to_existing_karyawan(karyawan_id)
    
    # Test 3: Get karyawan with photo info
    test_get_karyawan_with_photo()
    
    # Test 4: Delete photo
    if karyawan_id:
        test_delete_photo(karyawan_id)
    
    # Test 5: Invalid file types
    test_invalid_file_types()
    
    # Test 6: Large file upload
    test_large_file()
    
    print("\n" + "=" * 50)
    print("🏁 Photo Upload API Tests Completed!")

if __name__ == "__main__":
    main()