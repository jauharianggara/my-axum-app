#!/usr/bin/env python3
"""
Debug script to test photo upload functionality
"""

import requests
import json
from PIL import Image
import io

BASE_URL = "http://localhost:8080"
API_BASE = f"{BASE_URL}/api"

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.getvalue()

def test_photo_upload():
    """Test photo upload"""
    print("🔍 Testing photo upload...")
    
    # Create test image
    image_data = create_test_image()
    print(f"📷 Created test image: {len(image_data)} bytes")
    
    # Test data
    files = {
        'foto': ('test.jpg', io.BytesIO(image_data), 'image/jpeg')
    }
    
    data = {
        'nama': 'Debug Test',
        'posisi': 'Debugger',
        'gaji': '3000000',
        'kantor_id': '2'  # Use existing kantor ID
    }
    
    try:
        print("📤 Sending request...")
        response = requests.post(f"{API_BASE}/karyawans/with-photo", 
                               files=files, data=data, timeout=10)
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📄 Response headers: {dict(response.headers)}")
        
        try:
            result = response.json()
            print(f"✅ Response JSON: {json.dumps(result, indent=2)}")
            
            if result.get('success'):
                print("🎉 Upload successful!")
                karyawan_id = result.get('data', {}).get('id')
                if karyawan_id:
                    print(f"🆔 Created karyawan ID: {karyawan_id}")
                    
                    # Clean up
                    delete_response = requests.delete(f"{API_BASE}/karyawans/{karyawan_id}")
                    print(f"🧹 Cleanup status: {delete_response.status_code}")
            else:
                print(f"❌ Upload failed: {result.get('message', 'Unknown error')}")
                
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response: {response.text}")
            
    except Exception as e:
        print(f"💥 Request failed: {str(e)}")

def test_basic_api():
    """Test basic API connectivity"""
    print("🌐 Testing basic API connectivity...")
    
    try:
        response = requests.get(f"{API_BASE}/karyawans", timeout=5)
        print(f"📊 GET /karyawans status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API is working. Found {len(result.get('data', []))} karyawans")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"💥 Basic API test failed: {str(e)}")

if __name__ == "__main__":
    print("🔧 DEBUG: Photo Upload API Testing")
    print("=" * 50)
    
    test_basic_api()
    print()
    test_photo_upload()