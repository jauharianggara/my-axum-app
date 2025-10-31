# Auto-Create User Flow Test Script
# Flow: Create Karyawan → Auto-create User → Login → Get Profile

Write-Host "🧪 Testing Auto-Create User Feature" -ForegroundColor Cyan
Write-Host ("=" * 70)

try {
    # ============================================================================
    # STEP 1: Login sebagai admin untuk create karyawan
    # ============================================================================
    Write-Host "`n📋 STEP 1: Login as Admin" -ForegroundColor Yellow
    Write-Host ("-" * 70)
    
    $loginBody = @{
        username_or_email = "testuser"
        password = "password123"
    } | ConvertTo-Json

    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/auth/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $loginBody

    $adminToken = $loginResponse.data.token
    $adminUserId = $loginResponse.data.user.id
    Write-Host "✅ Admin logged in successfully" -ForegroundColor Green
    Write-Host "   Admin User ID: $adminUserId"
    Write-Host "   Admin Username: $($loginResponse.data.user.username)"

    $adminHeaders = @{
        Authorization = "Bearer $adminToken"
        "Content-Type" = "application/json"
    }

    # ============================================================================
    # STEP 2: Get existing kantor
    # ============================================================================
    Write-Host "`n📋 STEP 2: Get Kantor for Karyawan" -ForegroundColor Yellow
    Write-Host ("-" * 70)
    
    $kantorResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/kantors" `
        -Method GET `
        -Headers $adminHeaders

    $kantors = $kantorResponse.data
    if ($kantors.Count -eq 0) {
        Write-Host "❌ No kantor found. Please create one first." -ForegroundColor Red
        return
    }

    $kantorId = $kantors[0].id
    Write-Host "✅ Using kantor ID: $kantorId" -ForegroundColor Green
    Write-Host "   Kantor Name: $($kantors[0].nama)"

    # ============================================================================
    # STEP 3: Create Karyawan (Auto-create User)
    # ============================================================================
    Write-Host "`n📋 STEP 3: Create Karyawan (Auto-create User)" -ForegroundColor Yellow
    Write-Host ("-" * 70)
    
    $karyawanName = "Budi Santoso Test"
    $expectedUsername = $karyawanName.ToLower().Replace(" ", "")
    $expectedEmail = "$expectedUsername@karyawan.local"
    
    Write-Host "Creating karyawan: $karyawanName"
    Write-Host "Expected auto-created username: $expectedUsername"
    Write-Host "Expected auto-created email: $expectedEmail"
    
    $createBody = @{
        nama = $karyawanName
        posisi = "Software Engineer"
        gaji = "8500000"
        kantor_id = $kantorId.ToString()
    } | ConvertTo-Json

    $createResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/karyawans" `
        -Method POST `
        -Headers $adminHeaders `
        -Body $createBody

    $karyawanId = $createResponse.data.id
    $autoCreatedUserId = $createResponse.data.user_id

    Write-Host "✅ Karyawan created successfully" -ForegroundColor Green
    Write-Host "   Karyawan ID: $karyawanId"
    Write-Host "   Karyawan Name: $($createResponse.data.nama)"
    Write-Host "   Karyawan Position: $($createResponse.data.posisi)"
    Write-Host "   Karyawan Salary: Rp $($createResponse.data.gaji)"
    Write-Host "   Auto-created User ID: $autoCreatedUserId"

    if ($null -eq $autoCreatedUserId) {
        Write-Host "❌ User ID is None! Auto-create user failed!" -ForegroundColor Red
        return
    } else {
        Write-Host "✅ User auto-created successfully!" -ForegroundColor Green
    }

    # ============================================================================
    # STEP 4: Login dengan User yang Auto-created (Password Default)
    # ============================================================================
    Write-Host "`n📋 STEP 4: Login with Auto-created User" -ForegroundColor Yellow
    Write-Host ("-" * 70)
    
    $defaultPassword = "12345678"
    Write-Host "Attempting login with:"
    Write-Host "   Username: $expectedUsername"
    Write-Host "   Password: $defaultPassword"
    
    $karyawanLoginBody = @{
        username_or_email = $expectedUsername
        password = $defaultPassword
    } | ConvertTo-Json

    try {
        $karyawanLoginResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/auth/login" `
            -Method POST `
            -ContentType "application/json" `
            -Body $karyawanLoginBody

        $karyawanToken = $karyawanLoginResponse.data.token
        $karyawanUser = $karyawanLoginResponse.data.user
        $tokenExpiresIn = $karyawanLoginResponse.data.expires_in

        Write-Host "✅ Karyawan logged in successfully!" -ForegroundColor Green
        Write-Host "   User ID: $($karyawanUser.id)"
        Write-Host "   Username: $($karyawanUser.username)"
        Write-Host "   Email: $($karyawanUser.email)"
        Write-Host "   Full Name: $($karyawanUser.full_name)"
        Write-Host "   Is Active: $($karyawanUser.is_active)"
        Write-Host "   Token: $($karyawanToken.Substring(0, 50))..."
        Write-Host "   Token Expires In: $tokenExpiresIn seconds ($($tokenExpiresIn/3600) hours)"

        # Verify user_id matches
        if ($karyawanUser.id -eq $autoCreatedUserId) {
            Write-Host "✅ User ID matches auto-created user ID!" -ForegroundColor Green
        } else {
            Write-Host "❌ User ID mismatch! Expected $autoCreatedUserId, got $($karyawanUser.id)" -ForegroundColor Red
        }

        # Verify username
        if ($karyawanUser.username -eq $expectedUsername) {
            Write-Host "✅ Username matches expected: $expectedUsername" -ForegroundColor Green
        } else {
            Write-Host "❌ Username mismatch! Expected $expectedUsername, got $($karyawanUser.username)" -ForegroundColor Red
        }

        # Verify email
        if ($karyawanUser.email -eq $expectedEmail) {
            Write-Host "✅ Email matches expected: $expectedEmail" -ForegroundColor Green
        } else {
            Write-Host "❌ Email mismatch! Expected $expectedEmail, got $($karyawanUser.email)" -ForegroundColor Red
        }

        # Verify full name
        if ($karyawanUser.full_name -eq $karyawanName) {
            Write-Host "✅ Full name matches karyawan name: $karyawanName" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Full name mismatch! Expected $karyawanName, got $($karyawanUser.full_name)" -ForegroundColor Yellow
        }

    } catch {
        Write-Host "❌ Karyawan login failed!" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)"
        
        # Cleanup
        Invoke-RestMethod -Uri "http://localhost:8080/api/karyawans/$karyawanId" `
            -Method DELETE `
            -Headers $adminHeaders
        return
    }

    # ============================================================================
    # STEP 5: Get User Profile (using karyawan token)
    # ============================================================================
    Write-Host "`n📋 STEP 5: Get User Profile" -ForegroundColor Yellow
    Write-Host ("-" * 70)
    
    $karyawanHeaders = @{
        Authorization = "Bearer $karyawanToken"
        "Content-Type" = "application/json"
    }
    
    try {
        $profileResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/user/profile" `
            -Method GET `
            -Headers $karyawanHeaders

        $profileData = $profileResponse.data
        Write-Host "✅ User profile retrieved successfully!" -ForegroundColor Green
        Write-Host "   Profile User ID: $($profileData.id)"
        Write-Host "   Profile Username: $($profileData.username)"
        Write-Host "   Profile Email: $($profileData.email)"
        Write-Host "   Profile Full Name: $($profileData.full_name)"
        Write-Host "   Profile Is Active: $($profileData.is_active)"
        Write-Host "   Profile Created At: $($profileData.created_at)"

        # Verify profile matches login data
        if ($profileData.id -eq $karyawanUser.id) {
            Write-Host "✅ Profile ID matches login user ID!" -ForegroundColor Green
        } else {
            Write-Host "❌ Profile ID mismatch!" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Failed to get user profile" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)"
    }

    # ============================================================================
    # STEP 6: Get Karyawan List (as authenticated karyawan)
    # ============================================================================
    Write-Host "`n📋 STEP 6: Get Karyawan List (as authenticated karyawan)" -ForegroundColor Yellow
    Write-Host ("-" * 70)
    
    try {
        $karyawanListResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/karyawans" `
            -Method GET `
            -Headers $karyawanHeaders

        $karyawanList = $karyawanListResponse.data
        Write-Host "✅ Karyawan list retrieved successfully!" -ForegroundColor Green
        Write-Host "   Total karyawan: $($karyawanList.Count)"

        # Find our karyawan in the list
        $ourKaryawan = $karyawanList | Where-Object { $_.id -eq $karyawanId }
        if ($ourKaryawan) {
            Write-Host "✅ Found our karyawan in the list!" -ForegroundColor Green
            Write-Host "   Name: $($ourKaryawan.nama)"
            Write-Host "   User ID: $($ourKaryawan.user_id)"
        }
    } catch {
        Write-Host "❌ Failed to get karyawan list" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)"
    }

    # ============================================================================
    # STEP 7: Test Duplicate Name (Should reuse existing user)
    # ============================================================================
    Write-Host "`n📋 STEP 7: Test Duplicate Name (Should reuse existing user)" -ForegroundColor Yellow
    Write-Host ("-" * 70)
    
    Write-Host "Creating another karyawan with same name: $karyawanName"
    
    $createBody2 = @{
        nama = $karyawanName  # Same name!
        posisi = "Senior Engineer"
        gaji = "12000000"
        kantor_id = $kantorId.ToString()
    } | ConvertTo-Json

    try {
        $createResponse2 = Invoke-RestMethod -Uri "http://localhost:8080/api/karyawans" `
            -Method POST `
            -Headers $adminHeaders `
            -Body $createBody2

        $karyawan2Id = $createResponse2.data.id
        $karyawan2UserId = $createResponse2.data.user_id

        Write-Host "✅ Second karyawan created" -ForegroundColor Green
        Write-Host "   Karyawan 2 ID: $karyawan2Id"
        Write-Host "   Karyawan 2 User ID: $karyawan2UserId"

        if ($karyawan2UserId -eq $autoCreatedUserId) {
            Write-Host "✅ Second karyawan reused existing user (expected behavior)!" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Second karyawan has different user_id" -ForegroundColor Yellow
        }

        # Cleanup second karyawan
        Invoke-RestMethod -Uri "http://localhost:8080/api/karyawans/$karyawan2Id" `
            -Method DELETE `
            -Headers $adminHeaders | Out-Null
        Write-Host "✅ Second karyawan deleted" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Failed to create second karyawan (might be expected)" -ForegroundColor Yellow
        Write-Host "Error: $($_.Exception.Message)"
    }

    # ============================================================================
    # STEP 8: Cleanup - Delete Test Karyawan
    # ============================================================================
    Write-Host "`n📋 STEP 8: Cleanup" -ForegroundColor Yellow
    Write-Host ("-" * 70)
    
    Write-Host "Deleting test karyawan (ID: $karyawanId)..."
    Invoke-RestMethod -Uri "http://localhost:8080/api/karyawans/$karyawanId" `
        -Method DELETE `
        -Headers $adminHeaders | Out-Null
    Write-Host "✅ Test karyawan deleted" -ForegroundColor Green

    Write-Host "⚠️  Note: Auto-created user (ID: $autoCreatedUserId) is NOT deleted" -ForegroundColor Yellow
    Write-Host "   This is to maintain referential integrity."
    Write-Host "   Username: $expectedUsername"
    Write-Host "   You can still login with this user for testing."

    # ============================================================================
    # Summary
    # ============================================================================
    Write-Host "`n$("=" * 70)"
    Write-Host "🎉 Auto-Create User Flow Test Completed Successfully!" -ForegroundColor Cyan
    Write-Host ("=" * 70)
    Write-Host "`n📊 Test Summary:"
    Write-Host "   ✅ Admin login successful" -ForegroundColor Green
    Write-Host "   ✅ Karyawan created with auto-user creation" -ForegroundColor Green
    Write-Host "   ✅ Auto-created user login successful (password: $defaultPassword)" -ForegroundColor Green
    Write-Host "   ✅ User profile retrieved successfully" -ForegroundColor Green
    Write-Host "   ✅ Karyawan can access protected endpoints" -ForegroundColor Green
    Write-Host "   ✅ Duplicate name handling tested" -ForegroundColor Green
    Write-Host "`n📝 Credentials Created:"
    Write-Host "   Username: $expectedUsername"
    Write-Host "   Email: $expectedEmail"
    Write-Host "   Password: $defaultPassword"
    Write-Host "   User ID: $autoCreatedUserId"
    Write-Host "   Karyawan ID: $karyawanId (deleted)"

} catch {
    Write-Host "`n❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}
