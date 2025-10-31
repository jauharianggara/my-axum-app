#!/usr/bin/env python3
"""
Test duplicate name handling specifically
"""

import requests

BASE_URL = "http://localhost:8080"

def test_duplicate():
    # Login as admin
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "username_or_email": "testuser",
            "password": "password123"
        }
    )
    
    admin_token = login_response.json()['data']['token']
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Get kantor
    kantor_response = requests.get(f"{BASE_URL}/api/kantors", headers=headers)
    kantor_id = kantor_response.json()['data'][0]['id']
    
    # Create first karyawan
    print("Creating first karyawan...")
    create1 = requests.post(
        f"{BASE_URL}/api/karyawans",
        headers=headers,
        json={
            "nama": "Duplicate Test User",
            "posisi": "Engineer",
            "gaji": "5000000",
            "kantor_id": str(kantor_id)
        }
    )
    
    print(f"Response 1: {create1.status_code}")
    print(f"Data 1: {create1.json()}")
    
    if create1.status_code in [200, 201]:
        karyawan1_id = create1.json()['data']['id']
        user1_id = create1.json()['data'].get('user_id')
        print(f"✅ First karyawan created - ID: {karyawan1_id}, User ID: {user1_id}")
        
        # Create second karyawan with same name
        print("\nCreating second karyawan with same name...")
        create2 = requests.post(
            f"{BASE_URL}/api/karyawans",
            headers=headers,
            json={
                "nama": "Duplicate Test User",  # SAME NAME!
                "posisi": "Senior Engineer",
                "gaji": "7000000",
                "kantor_id": str(kantor_id)
            }
        )
        
        print(f"Response 2: {create2.status_code}")
        print(f"Data 2: {create2.json()}")
        
        if create2.status_code in [200, 201]:
            response_json = create2.json()
            if response_json.get('data'):
                karyawan2_id = response_json['data']['id']
                user2_id = response_json['data'].get('user_id')
                print(f"✅ Second karyawan created - ID: {karyawan2_id}, User ID: {user2_id}")
                
                if user2_id == user1_id:
                    print(f"✅ CORRECT: Both karyawan share same user ID: {user1_id}")
                else:
                    print(f"❌ ERROR: Different user IDs! {user1_id} vs {user2_id}")
                
                # Cleanup
                requests.delete(f"{BASE_URL}/api/karyawans/{karyawan2_id}", headers=headers)
            else:
                print(f"❌ No data in response!")
        else:
            print(f"❌ Failed to create second karyawan")
        
        # Cleanup first
        requests.delete(f"{BASE_URL}/api/karyawans/{karyawan1_id}", headers=headers)

if __name__ == "__main__":
    test_duplicate()
