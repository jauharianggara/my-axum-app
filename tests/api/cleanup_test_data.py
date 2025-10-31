#!/usr/bin/env python3
"""
Cleanup test data from database
"""

import requests

BASE_URL = "http://localhost:8080"

def cleanup():
    # Login as admin
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "username_or_email": "testuser",
            "password": "password123"
        }
    )
    
    if login_response.status_code != 200:
        print("❌ Failed to login as admin")
        return
    
    admin_token = login_response.json()['data']['token']
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Get all karyawan
    karyawan_response = requests.get(
        f"{BASE_URL}/api/karyawans",
        headers=headers
    )
    
    if karyawan_response.status_code != 200:
        print("❌ Failed to get karyawan list")
        return
    
    karyawans = karyawan_response.json()['data']
    
    # Delete test karyawan (contains "Test" in name or has user_id 9)
    deleted_count = 0
    for k in karyawans:
        if 'Test' in k.get('nama', '') or k.get('user_id') == 9:
            delete_response = requests.delete(
                f"{BASE_URL}/api/karyawans/{k['id']}",
                headers=headers
            )
            if delete_response.status_code in [200, 204]:
                print(f"✅ Deleted karyawan: {k['nama']} (ID: {k['id']}, User ID: {k.get('user_id')})")
                deleted_count += 1
            else:
                print(f"❌ Failed to delete karyawan {k['id']}: {delete_response.status_code}")
    
    print(f"\n🎉 Cleanup complete! Deleted {deleted_count} test karyawan")

if __name__ == "__main__":
    cleanup()
