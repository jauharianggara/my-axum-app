"""
Test script untuk verifikasi koneksi user-karyawan
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_user_tracking():
    print("🧪 Testing User Tracking in Karyawan...")
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
    
    # Step 2: Get existing kantor
    print("\n2️⃣ Getting kantor list...")
    kantor_response = requests.get(f"{BASE_URL}/api/kantors", headers=headers)
    if kantor_response.status_code == 200:
        kantors = kantor_response.json()['data']
        if kantors:
            kantor_id = kantors[0]['id']
            print(f"✅ Using kantor ID: {kantor_id}")
        else:
            print("❌ No kantor found. Please create one first.")
            return
    else:
        print("❌ Failed to get kantors")
        return
    
    # Step 3: Create new karyawan
    print("\n3️⃣ Creating new karyawan...")
    create_response = requests.post(
        f"{BASE_URL}/api/karyawans",
        headers=headers,
        json={
            "nama": "Test User Tracking",
            "posisi": "QA Engineer",
            "gaji": "7500000",
            "kantor_id": str(kantor_id)
        }
    )
    
    if create_response.status_code not in [200, 201]:
        print("❌ Failed to create karyawan")
        print(f"Status: {create_response.status_code}")
        print(f"Response: {create_response.text}")
        return
    
    karyawan_data = create_response.json()['data']
    karyawan_id = karyawan_data['id']
    print(f"✅ Karyawan created with ID: {karyawan_id}")
    print(f"   Created by: {karyawan_data.get('created_by')}")
    print(f"   Updated by: {karyawan_data.get('updated_by')}")
    
    # Step 4: Verify created_by matches user_id
    if karyawan_data.get('created_by') == user_id:
        print("✅ created_by correctly set to logged-in user!")
    else:
        print(f"❌ created_by mismatch! Expected {user_id}, got {karyawan_data.get('created_by')}")
    
    if karyawan_data.get('updated_by') == user_id:
        print("✅ updated_by correctly set to logged-in user!")
    else:
        print(f"❌ updated_by mismatch! Expected {user_id}, got {karyawan_data.get('updated_by')}")
    
    # Step 5: Update karyawan
    print("\n4️⃣ Updating karyawan...")
    update_response = requests.put(
        f"{BASE_URL}/api/karyawans/{karyawan_id}",
        headers=headers,
        json={
            "nama": "Test User Tracking Updated",
            "posisi": "Senior QA Engineer",
            "gaji": "8500000",
            "kantor_id": str(kantor_id)
        }
    )
    
    if update_response.status_code == 200:
        updated_data = update_response.json()['data']
        print(f"✅ Karyawan updated")
        print(f"   Created by: {updated_data.get('created_by')}")
        print(f"   Updated by: {updated_data.get('updated_by')}")
        
        # Verify updated_by is updated
        if updated_data.get('updated_by') == user_id:
            print("✅ updated_by correctly updated!")
        else:
            print(f"❌ updated_by not updated correctly")
    else:
        print("❌ Failed to update karyawan")
        print(f"Response: {update_response.text}")
    
    # Step 6: Get karyawan with kantor to see full info
    print("\n5️⃣ Getting karyawan with kantor info...")
    get_response = requests.get(
        f"{BASE_URL}/api/karyawans/{karyawan_id}/with-kantor",
        headers=headers
    )
    
    if get_response.status_code == 200:
        full_data = get_response.json()['data']
        print("✅ Full karyawan data:")
        print(f"   ID: {full_data['id']}")
        print(f"   Nama: {full_data['nama']}")
        print(f"   Posisi: {full_data['posisi']}")
        print(f"   Kantor: {full_data.get('kantor_nama')}")
        print(f"   Created by: {full_data.get('created_by')}")
        print(f"   Updated by: {full_data.get('updated_by')}")
        print(f"   Created at: {full_data['created_at']}")
        print(f"   Updated at: {full_data['updated_at']}")
    
    # Step 7: Cleanup - delete test karyawan
    print("\n6️⃣ Cleaning up...")
    delete_response = requests.delete(
        f"{BASE_URL}/api/karyawans/{karyawan_id}",
        headers=headers
    )
    
    if delete_response.status_code == 200:
        print("✅ Test karyawan deleted")
    else:
        print("⚠️ Could not delete test karyawan")
    
    print("\n" + "=" * 60)
    print("🎉 User tracking test completed!")

if __name__ == "__main__":
    try:
        test_user_tracking()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
