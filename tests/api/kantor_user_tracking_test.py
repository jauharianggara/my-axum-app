"""
Test script untuk verifikasi user tracking di kantor
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_kantor_user_tracking():
    print("🧪 Testing User Tracking in Kantor...")
    print("=" * 60)
    
    # Step 1: Login
    print("\n1️⃣ Login...")
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "username_or_email": "testuser",
            "password": "password123"
        }
    )
    
    if login_response.status_code != 200:
        print("❌ Login failed!")
        print(f"Response: {login_response.text}")
        return
    
    login_data = login_response.json()
    token = login_data['data']['token']
    user_id = login_data['data']['user']['id']
    print(f"✅ Logged in as user ID: {user_id}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Create new kantor
    print("\n2️⃣ Creating new kantor...")
    create_response = requests.post(
        f"{BASE_URL}/api/kantors",
        headers=headers,
        json={
            "nama": "Kantor Test User Tracking",
            "alamat": "Jl. Test User Tracking No. 123",
            "longitude": 106.8456,
            "latitude": -6.2088
        }
    )
    
    if create_response.status_code not in [200, 201]:
        print("❌ Failed to create kantor")
        print(f"Status: {create_response.status_code}")
        print(f"Response: {create_response.text}")
        return
    
    kantor_data = create_response.json()['data']
    kantor_id = kantor_data['id']
    print(f"✅ Kantor created with ID: {kantor_id}")
    print(f"   Created by: {kantor_data.get('created_by')}")
    print(f"   Updated by: {kantor_data.get('updated_by')}")
    
    # Step 3: Verify created_by matches user_id
    if kantor_data.get('created_by') == user_id:
        print("✅ created_by correctly set to logged-in user!")
    else:
        print(f"❌ created_by mismatch! Expected {user_id}, got {kantor_data.get('created_by')}")
    
    if kantor_data.get('updated_by') == user_id:
        print("✅ updated_by correctly set to logged-in user!")
    else:
        print(f"❌ updated_by mismatch! Expected {user_id}, got {kantor_data.get('updated_by')}")
    
    # Step 4: Update kantor
    print("\n3️⃣ Updating kantor...")
    update_response = requests.put(
        f"{BASE_URL}/api/kantors/{kantor_id}",
        headers=headers,
        json={
            "nama": "Kantor Test Updated",
            "alamat": "Jl. Test Updated No. 456",
            "longitude": 106.8500,
            "latitude": -6.2100
        }
    )
    
    if update_response.status_code == 200:
        updated_data = update_response.json()['data']
        print(f"✅ Kantor updated")
        print(f"   Created by: {updated_data.get('created_by')}")
        print(f"   Updated by: {updated_data.get('updated_by')}")
        
        # Verify updated_by is updated
        if updated_data.get('updated_by') == user_id:
            print("✅ updated_by correctly updated!")
        else:
            print(f"❌ updated_by not updated correctly")
            
        # Verify created_by remains the same
        if updated_data.get('created_by') == user_id:
            print("✅ created_by remains unchanged!")
        else:
            print(f"❌ created_by changed unexpectedly!")
    else:
        print("❌ Failed to update kantor")
        print(f"Response: {update_response.text}")
    
    # Step 5: Get kantor details
    print("\n4️⃣ Getting kantor details...")
    get_response = requests.get(
        f"{BASE_URL}/api/kantors/{kantor_id}",
        headers=headers
    )
    
    if get_response.status_code == 200:
        full_data = get_response.json()['data']
        print("✅ Full kantor data:")
        print(f"   ID: {full_data['id']}")
        print(f"   Nama: {full_data['nama']}")
        print(f"   Alamat: {full_data['alamat']}")
        print(f"   Longitude: {full_data['longitude']}")
        print(f"   Latitude: {full_data['latitude']}")
        print(f"   Created by: {full_data.get('created_by')}")
        print(f"   Updated by: {full_data.get('updated_by')}")
        print(f"   Created at: {full_data['created_at']}")
        print(f"   Updated at: {full_data['updated_at']}")
    
    # Step 6: Test with different user (if available)
    print("\n5️⃣ Testing with different user...")
    login2_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "username_or_email": "admin",
            "password": "admin123"
        }
    )
    
    if login2_response.status_code == 200:
        login2_data = login2_response.json()
        token2 = login2_data['data']['token']
        user2_id = login2_data['data']['user']['id']
        print(f"✅ Logged in as second user ID: {user2_id}")
        
        headers2 = {
            "Authorization": f"Bearer {token2}",
            "Content-Type": "application/json"
        }
        
        # Update with second user
        update2_response = requests.put(
            f"{BASE_URL}/api/kantors/{kantor_id}",
            headers=headers2,
            json={
                "nama": "Kantor Test Updated by Admin",
                "alamat": "Jl. Test Admin No. 789",
                "longitude": 106.8600,
                "latitude": -6.2200
            }
        )
        
        if update2_response.status_code == 200:
            updated2_data = update2_response.json()['data']
            print(f"✅ Kantor updated by second user")
            print(f"   Created by: {updated2_data.get('created_by')} (should be {user_id})")
            print(f"   Updated by: {updated2_data.get('updated_by')} (should be {user2_id})")
            
            if updated2_data.get('created_by') == user_id and updated2_data.get('updated_by') == user2_id:
                print("✅ User tracking works correctly across different users!")
            else:
                print("❌ User tracking not working correctly across users")
        
        # Switch back to first user for cleanup
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    else:
        print("⚠️ Second user (admin) not available, skipping multi-user test")
    
    # Step 7: Cleanup - delete test kantor
    print("\n6️⃣ Cleaning up...")
    delete_response = requests.delete(
        f"{BASE_URL}/api/kantors/{kantor_id}",
        headers=headers
    )
    
    if delete_response.status_code == 200:
        print("✅ Test kantor deleted")
    else:
        print("⚠️ Could not delete test kantor")
        print(f"Response: {delete_response.text}")
    
    print("\n" + "=" * 60)
    print("🎉 Kantor user tracking test completed!")

if __name__ == "__main__":
    try:
        test_kantor_user_tracking()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
