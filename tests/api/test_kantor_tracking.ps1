# Kantor User Tracking Test Script
Write-Host "🧪 Testing Kantor User Tracking..." -ForegroundColor Cyan
Write-Host ("=" * 60)

try {
    # Step 1: Login
    Write-Host "`n1️⃣ Login..." -ForegroundColor Yellow
    $loginBody = @{
        username_or_email = "testuser"
        password = "password123"
    } | ConvertTo-Json

    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/auth/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $loginBody

    $token = $loginResponse.data.token
    $userId = $loginResponse.data.user.id
    Write-Host "✅ Logged in as user ID: $userId" -ForegroundColor Green

    $headers = @{
        Authorization = "Bearer $token"
        "Content-Type" = "application/json"
    }

    # Step 2: Create Kantor
    Write-Host "`n2️⃣ Creating new kantor..." -ForegroundColor Yellow
    $createBody = @{
        nama = "Kantor Test User Tracking"
        alamat = "Jl. Test User Tracking No. 123"
        longitude = 106.8456
        latitude = -6.2088
    } | ConvertTo-Json

    $createResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/kantors" `
        -Method POST `
        -Headers $headers `
        -Body $createBody

    $kantorId = $createResponse.data.id
    $createdBy = $createResponse.data.created_by
    $updatedBy = $createResponse.data.updated_by

    Write-Host "✅ Kantor created with ID: $kantorId" -ForegroundColor Green
    Write-Host "   Created by: $createdBy"
    Write-Host "   Updated by: $updatedBy"

    # Step 3: Verify created_by
    if ($createdBy -eq $userId) {
        Write-Host "✅ created_by correctly set to logged-in user!" -ForegroundColor Green
    } else {
        Write-Host "❌ created_by mismatch! Expected $userId, got $createdBy" -ForegroundColor Red
    }

    if ($updatedBy -eq $userId) {
        Write-Host "✅ updated_by correctly set to logged-in user!" -ForegroundColor Green
    } else {
        Write-Host "❌ updated_by mismatch! Expected $userId, got $updatedBy" -ForegroundColor Red
    }

    # Step 4: Update Kantor
    Write-Host "`n3️⃣ Updating kantor..." -ForegroundColor Yellow
    $updateBody = @{
        nama = "Kantor Test Updated"
        alamat = "Jl. Test Updated No. 456"
        longitude = 106.8500
        latitude = -6.2100
    } | ConvertTo-Json

    $updateResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/kantors/$kantorId" `
        -Method PUT `
        -Headers $headers `
        -Body $updateBody

    $updatedCreatedBy = $updateResponse.data.created_by
    $updatedUpdatedBy = $updateResponse.data.updated_by

    Write-Host "✅ Kantor updated" -ForegroundColor Green
    Write-Host "   Created by: $updatedCreatedBy"
    Write-Host "   Updated by: $updatedUpdatedBy"

    # Step 5: Verify updated_by changed but created_by didn't
    if ($updatedUpdatedBy -eq $userId) {
        Write-Host "✅ updated_by correctly updated!" -ForegroundColor Green
    } else {
        Write-Host "❌ updated_by not updated correctly" -ForegroundColor Red
    }

    if ($updatedCreatedBy -eq $userId) {
        Write-Host "✅ created_by remains unchanged!" -ForegroundColor Green
    } else {
        Write-Host "❌ created_by changed unexpectedly!" -ForegroundColor Red
    }

    # Step 6: Get full kantor details
    Write-Host "`n4️⃣ Getting kantor details..." -ForegroundColor Yellow
    $getResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/kantors/$kantorId" `
        -Method GET `
        -Headers $headers

    Write-Host "✅ Full kantor data:" -ForegroundColor Green
    Write-Host "   ID: $($getResponse.data.id)"
    Write-Host "   Nama: $($getResponse.data.nama)"
    Write-Host "   Alamat: $($getResponse.data.alamat)"
    Write-Host "   Created by: $($getResponse.data.created_by)"
    Write-Host "   Updated by: $($getResponse.data.updated_by)"
    Write-Host "   Created at: $($getResponse.data.created_at)"
    Write-Host "   Updated at: $($getResponse.data.updated_at)"

    # Step 7: Cleanup
    Write-Host "`n5️⃣ Cleaning up..." -ForegroundColor Yellow
    $deleteResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/kantors/$kantorId" `
        -Method DELETE `
        -Headers $headers

    Write-Host "✅ Test kantor deleted" -ForegroundColor Green

    Write-Host "`n$("=" * 60)"
    Write-Host "🎉 Kantor user tracking test completed!" -ForegroundColor Cyan

} catch {
    Write-Host "`n❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}
