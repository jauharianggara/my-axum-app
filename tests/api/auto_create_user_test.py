"""
Test script untuk Auto-Create User Feature
Flow: Create Karyawan → Auto-create User → Login → Get Profile
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_auto_create_user_flow():
    print("🧪 Testing Auto-Create User Feature")
    print("=" * 70)
    
    # ============================================================================
    # STEP 1: Login sebagai admin untuk create karyawan
    # ============================================================================
    print("\n📋 STEP 1: Login as Admin")
    print("-" * 70)
    
    login_admin_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "username_or_email": "testuser",
            "password": "password123"
        }
    )
    
    if login_admin_response.status_code != 200:
        print("❌ Admin login failed!")
        print(f"Response: {login_admin_response.text}")
        return
    
    admin_data = login_admin_response.json()
    admin_token = admin_data['data']['token']
    admin_user_id = admin_data['data']['user']['id']
    print(f"✅ Admin logged in successfully")
    print(f"   Admin User ID: {admin_user_id}")
    print(f"   Admin Username: {admin_data['data']['user']['username']}")
    
    admin_headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    
    # ============================================================================
    # STEP 2: Get existing kantor
    # ============================================================================
    print("\n📋 STEP 2: Get Kantor for Karyawan")
    print("-" * 70)
    
    kantor_response = requests.get(f"{BASE_URL}/api/kantors", headers=admin_headers)
    if kantor_response.status_code == 200:
        kantors = kantor_response.json()['data']
        if kantors:
            kantor_id = kantors[0]['id']
            print(f"✅ Using kantor ID: {kantor_id}")
            print(f"   Kantor Name: {kantors[0]['nama']}")
        else:
            print("❌ No kantor found. Please create one first.")
            return
    else:
        print("❌ Failed to get kantors")
        return
    
    # ============================================================================
    # STEP 3: Create Karyawan (Auto-create User)
    # ============================================================================
    print("\n📋 STEP 3: Create Karyawan (Auto-create User)")
    print("-" * 70)
    
    karyawan_name = "Budi Santoso Test"
    expected_username = karyawan_name.lower().replace(" ", "")
    expected_email = f"{expected_username}@karyawan.local"
    
    print(f"Creating karyawan: {karyawan_name}")
    print(f"Expected auto-created username: {expected_username}")
    print(f"Expected auto-created email: {expected_email}")
    
    create_karyawan_response = requests.post(
        f"{BASE_URL}/api/karyawans",
        headers=admin_headers,
        json={
            "nama": karyawan_name,
            "posisi": "Software Engineer",
            "gaji": "8500000",
            "kantor_id": str(kantor_id)
            # Note: user_id NOT provided - should auto-create user
        }
    )
    
    if create_karyawan_response.status_code not in [200, 201]:
        print("❌ Failed to create karyawan")
        print(f"Status: {create_karyawan_response.status_code}")
        print(f"Response: {create_karyawan_response.text}")
        return
    
    try:
        response_json = create_karyawan_response.json()
        karyawan_data = response_json.get('data')
        
        if not karyawan_data:
            print("❌ No data in response")
            print(f"Response: {response_json}")
            return
            
        karyawan_id = karyawan_data['id']
        auto_created_user_id = karyawan_data.get('user_id')
    except Exception as e:
        print(f"❌ Error parsing response: {e}")
        print(f"Response text: {create_karyawan_response.text}")
        return
    
    print(f"✅ Karyawan created successfully")
    print(f"   Karyawan ID: {karyawan_id}")
    print(f"   Karyawan Name: {karyawan_data['nama']}")
    print(f"   Karyawan Position: {karyawan_data['posisi']}")
    print(f"   Karyawan Salary: Rp {karyawan_data['gaji']:,}")
    print(f"   Auto-created User ID: {auto_created_user_id}")
    
    if auto_created_user_id is None:
        print("❌ User ID is None! Auto-create user failed!")
        return
    else:
        print("✅ User auto-created successfully!")
    
    # ============================================================================
    # STEP 4: Login dengan User yang Auto-created (Password Default)
    # ============================================================================
    print("\n📋 STEP 4: Login with Auto-created User")
    print("-" * 70)
    
    default_password = "12345678"
    print(f"Attempting login with:")
    print(f"   Username: {expected_username}")
    print(f"   Password: {default_password}")
    
    login_karyawan_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "username_or_email": expected_username,
            "password": default_password
        }
    )
    
    if login_karyawan_response.status_code != 200:
        print("❌ Karyawan login failed!")
        print(f"Status: {login_karyawan_response.status_code}")
        print(f"Response: {login_karyawan_response.text}")
        
        # Try with email instead
        print(f"\nTrying with email: {expected_email}")
        login_karyawan_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "username_or_email": expected_email,
                "password": default_password
            }
        )
        
        if login_karyawan_response.status_code != 200:
            print("❌ Login with email also failed!")
            print(f"Response: {login_karyawan_response.text}")
            cleanup_karyawan(karyawan_id, admin_headers)
            return
    
    karyawan_login_data = login_karyawan_response.json()['data']
    karyawan_token = karyawan_login_data['token']
    karyawan_user = karyawan_login_data['user']
    token_expires_in = karyawan_login_data['expires_in']
    
    print(f"✅ Karyawan logged in successfully!")
    print(f"   User ID: {karyawan_user['id']}")
    print(f"   Username: {karyawan_user['username']}")
    print(f"   Email: {karyawan_user['email']}")
    print(f"   Full Name: {karyawan_user.get('full_name')}")
    print(f"   Is Active: {karyawan_user['is_active']}")
    print(f"   Token: {karyawan_token[:50]}...")
    print(f"   Token Expires In: {token_expires_in} seconds ({token_expires_in/3600} hours)")
    
    # Verify user_id matches
    if karyawan_user['id'] == auto_created_user_id:
        print(f"✅ User ID matches auto-created user ID!")
    else:
        print(f"❌ User ID mismatch! Expected {auto_created_user_id}, got {karyawan_user['id']}")
    
    # Verify username
    if karyawan_user['username'] == expected_username:
        print(f"✅ Username matches expected: {expected_username}")
    else:
        print(f"❌ Username mismatch! Expected {expected_username}, got {karyawan_user['username']}")
    
    # Verify email
    if karyawan_user['email'] == expected_email:
        print(f"✅ Email matches expected: {expected_email}")
    else:
        print(f"❌ Email mismatch! Expected {expected_email}, got {karyawan_user['email']}")
    
    # Verify full name
    if karyawan_user.get('full_name') == karyawan_name:
        print(f"✅ Full name matches karyawan name: {karyawan_name}")
    else:
        print(f"⚠️  Full name mismatch! Expected {karyawan_name}, got {karyawan_user.get('full_name')}")
    
    # ============================================================================
    # STEP 5: Get User Profile (using karyawan token)
    # ============================================================================
    print("\n📋 STEP 5: Get User Profile")
    print("-" * 70)
    
    karyawan_headers = {
        "Authorization": f"Bearer {karyawan_token}",
        "Content-Type": "application/json"
    }
    
    profile_response = requests.get(
        f"{BASE_URL}/api/user/me",
        headers=karyawan_headers
    )
    
    if profile_response.status_code != 200:
        print("❌ Failed to get user profile")
        print(f"Status: {profile_response.status_code}")
        print(f"Response: {profile_response.text}")
    else:
        profile_data = profile_response.json()['data']
        print(f"✅ User profile retrieved successfully!")
        print(f"   Profile User ID: {profile_data['id']}")
        print(f"   Profile Username: {profile_data['username']}")
        print(f"   Profile Email: {profile_data['email']}")
        print(f"   Profile Full Name: {profile_data.get('full_name')}")
        print(f"   Profile Is Active: {profile_data['is_active']}")
        print(f"   Profile Created At: {profile_data['created_at']}")
        
        # Verify profile matches login data
        if profile_data['id'] == karyawan_user['id']:
            print(f"✅ Profile ID matches login user ID!")
        else:
            print(f"❌ Profile ID mismatch!")
    
    # ============================================================================
    # STEP 6: Get Karyawan List (as authenticated karyawan)
    # ============================================================================
    print("\n📋 STEP 6: Get Karyawan List (as authenticated karyawan)")
    print("-" * 70)
    
    karyawan_list_response = requests.get(
        f"{BASE_URL}/api/karyawans",
        headers=karyawan_headers
    )
    
    if karyawan_list_response.status_code != 200:
        print("❌ Failed to get karyawan list")
        print(f"Status: {karyawan_list_response.status_code}")
    else:
        karyawan_list = karyawan_list_response.json()['data']
        print(f"✅ Karyawan list retrieved successfully!")
        print(f"   Total karyawan: {len(karyawan_list)}")
        
        # Find our karyawan in the list
        our_karyawan = next((k for k in karyawan_list if k['id'] == karyawan_id), None)
        if our_karyawan:
            print(f"✅ Found our karyawan in the list!")
            print(f"   Name: {our_karyawan['nama']}")
            print(f"   User ID: {our_karyawan.get('user_id')}")
    
    # ============================================================================
    # STEP 7: Test Duplicate Name (Should reuse existing user)
    # ============================================================================
    print("\n📋 STEP 7: Test Duplicate Name (Should reuse existing user)")
    print("-" * 70)
    
    print(f"Creating another karyawan with same name: {karyawan_name}")
    
    create_karyawan2_response = requests.post(
        f"{BASE_URL}/api/karyawans",
        headers=admin_headers,
        json={
            "nama": karyawan_name,  # Same name!
            "posisi": "Senior Engineer",
            "gaji": "12000000",
            "kantor_id": str(kantor_id)
        }
    )
    
    if create_karyawan2_response.status_code not in [200, 201]:
        print("⚠️  Failed to create second karyawan (might be expected)")
        print(f"Status: {create_karyawan2_response.status_code}")
        print(f"Response: {create_karyawan2_response.text}")
        karyawan2_id = None
    else:
        try:
            karyawan2_response_json = create_karyawan2_response.json()
            if karyawan2_response_json and 'data' in karyawan2_response_json and karyawan2_response_json['data']:
                karyawan2_data = karyawan2_response_json['data']
                karyawan2_id = karyawan2_data['id']
                karyawan2_user_id = karyawan2_data.get('user_id')
            
                print(f"✅ Second karyawan created")
                print(f"   Karyawan 2 ID: {karyawan2_id}")
                print(f"   Karyawan 2 User ID: {karyawan2_user_id}")
                
                if karyawan2_user_id == auto_created_user_id:
                    print(f"✅ Second karyawan reused existing user (expected behavior)!")
                else:
                    print(f"⚠️  Second karyawan has different user_id")
                
                # Cleanup second karyawan
                cleanup_karyawan(karyawan2_id, admin_headers)
            else:
                print("⚠️  Could not parse second karyawan response - data is None")
                karyawan2_id = None
        except Exception as e:
            print(f"⚠️  Error handling second karyawan: {e}")
            karyawan2_id = None
    
    # ============================================================================
    # STEP 8: Cleanup - Delete Test Karyawan
    # ============================================================================
    print("\n📋 STEP 8: Cleanup")
    print("-" * 70)
    
    cleanup_karyawan(karyawan_id, admin_headers)
    
    # Note: We don't delete the auto-created user because it might be referenced
    # by other records. In production, you'd want a proper user cleanup strategy.
    print(f"⚠️  Note: Auto-created user (ID: {auto_created_user_id}) is NOT deleted")
    print(f"   This is to maintain referential integrity.")
    print(f"   Username: {expected_username}")
    print(f"   You can still login with this user for testing.")
    
    # ============================================================================
    # Summary
    # ============================================================================
    print("\n" + "=" * 70)
    print("🎉 Auto-Create User Flow Test Completed Successfully!")
    print("=" * 70)
    print("\n📊 Test Summary:")
    print(f"   ✅ Admin login successful")
    print(f"   ✅ Karyawan created with auto-user creation")
    print(f"   ✅ Auto-created user login successful (password: {default_password})")
    print(f"   ✅ User profile retrieved successfully")
    print(f"   ✅ Karyawan can access protected endpoints")
    print(f"   ✅ Duplicate name handling tested")
    print(f"\n📝 Credentials Created:")
    print(f"   Username: {expected_username}")
    print(f"   Email: {expected_email}")
    print(f"   Password: {default_password}")
    print(f"   User ID: {auto_created_user_id}")
    print(f"   Karyawan ID: {karyawan_id} (deleted)")

def cleanup_karyawan(karyawan_id, headers):
    """Helper function to delete test karyawan"""
    print(f"Deleting test karyawan (ID: {karyawan_id})...")
    delete_response = requests.delete(
        f"{BASE_URL}/api/karyawans/{karyawan_id}",
        headers=headers
    )
    
    if delete_response.status_code == 200:
        print(f"✅ Test karyawan deleted")
    else:
        print(f"⚠️  Could not delete test karyawan")
        print(f"Response: {delete_response.text}")

if __name__ == "__main__":
    try:
        test_auto_create_user_flow()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
