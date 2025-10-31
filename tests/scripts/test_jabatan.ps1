# Test Jabatan CRUD Operations
# This script tests the new jabatan feature

$baseUrl = "http://localhost:8080"

Write-Host "=== Testing Jabatan Feature ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Login
Write-Host "1. Login as admin..." -ForegroundColor Yellow
$loginBody = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" -Method Post -Body $loginBody -ContentType "application/json"
    $token = $loginResponse.data.token
    Write-Host "✓ Login successful" -ForegroundColor Green
    Write-Host "Token: $($token.Substring(0, 20))..." -ForegroundColor Gray
} catch {
    Write-Host "✗ Login failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Create Jabatan
Write-Host "2. Creating new jabatan 'Manager'..." -ForegroundColor Yellow
$createJabatanBody = @{
    nama_jabatan = "Manager"
    deskripsi = "Manajer departemen"
} | ConvertTo-Json

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

try {
    $jabatan1 = Invoke-RestMethod -Uri "$baseUrl/api/jabatans" -Method Post -Body $createJabatanBody -Headers $headers
    Write-Host "✓ Jabatan 'Manager' created successfully with ID: $($jabatan1.data.id)" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to create jabatan: $_" -ForegroundColor Red
    $error[0] | Format-List -Force
    exit 1
}

Write-Host ""

# Step 3: Create another Jabatan
Write-Host "3. Creating new jabatan 'Staff'..." -ForegroundColor Yellow
$createJabatanBody2 = @{
    nama_jabatan = "Staff"
    deskripsi = "Staf operasional"
} | ConvertTo-Json

try {
    $jabatan2 = Invoke-RestMethod -Uri "$baseUrl/api/jabatans" -Method Post -Body $createJabatanBody2 -Headers $headers
    Write-Host "✓ Jabatan 'Staff' created successfully with ID: $($jabatan2.data.id)" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to create jabatan: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 4: Get All Jabatan
Write-Host "4. Getting all jabatan..." -ForegroundColor Yellow
try {
    $allJabatan = Invoke-RestMethod -Uri "$baseUrl/api/jabatans" -Method Get -Headers $headers
    Write-Host "✓ Retrieved $($allJabatan.data.Count) jabatan(s)" -ForegroundColor Green
    foreach ($jab in $allJabatan.data) {
        Write-Host "  - ID: $($jab.id), Nama: $($jab.nama_jabatan), Deskripsi: $($jab.deskripsi)" -ForegroundColor Gray
    }
} catch {
    Write-Host "✗ Failed to get jabatan: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 5: Get Jabatan by ID
Write-Host "5. Getting jabatan by ID $($jabatan1.data.id)..." -ForegroundColor Yellow
try {
    $jabatanById = Invoke-RestMethod -Uri "$baseUrl/api/jabatans/$($jabatan1.data.id)" -Method Get -Headers $headers
    Write-Host "✓ Retrieved: $($jabatanById.data.nama_jabatan)" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to get jabatan by ID: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 6: Update Jabatan
Write-Host "6. Updating jabatan ID $($jabatan1.data.id)..." -ForegroundColor Yellow
$updateJabatanBody = @{
    nama_jabatan = "Senior Manager"
    deskripsi = "Manajer senior departemen"
} | ConvertTo-Json

try {
    $updatedJabatan = Invoke-RestMethod -Uri "$baseUrl/api/jabatans/$($jabatan1.data.id)" -Method Put -Body $updateJabatanBody -Headers $headers
    Write-Host "✓ Jabatan updated successfully: $($updatedJabatan.data.nama_jabatan)" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to update jabatan: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 7: Create Karyawan with Jabatan
Write-Host "7. Creating karyawan with jabatan..." -ForegroundColor Yellow
$createKaryawanBody = @{
    nama = "Budi Santoso"
    posisi = "Manager IT"
    gaji = "15000000"
    kantor_id = "1"
    jabatan_id = "$($jabatan1.data.id)"
} | ConvertTo-Json

try {
    $karyawan = Invoke-RestMethod -Uri "$baseUrl/api/karyawans" -Method Post -Body $createKaryawanBody -Headers $headers
    Write-Host "✓ Karyawan created successfully with ID: $($karyawan.data.id)" -ForegroundColor Green
    Write-Host "  Nama: $($karyawan.data.nama), Jabatan ID: $($karyawan.data.jabatan_id)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Failed to create karyawan: $_" -ForegroundColor Red
    $error[0] | Format-List -Force
}

Write-Host ""

# Step 8: Delete Jabatan (should fail if used by karyawan)
$jabatanIdToDelete = $jabatan1.data.id
Write-Host "8. Trying to delete jabatan ID $jabatanIdToDelete (should fail - used by karyawan)..." -ForegroundColor Yellow
try {
    Invoke-RestMethod -Uri "$baseUrl/api/jabatans/$jabatanIdToDelete" -Method Delete -Headers $headers
    Write-Host "X Deletion should have failed but succeeded!" -ForegroundColor Red
} catch {
    Write-Host "OK Deletion correctly blocked (jabatan in use)" -ForegroundColor Green
}

Write-Host ""

# Step 9: Delete unused Jabatan
$jabatanIdToDelete2 = $jabatan2.data.id
Write-Host "9. Deleting unused jabatan ID $jabatanIdToDelete2..." -ForegroundColor Yellow
try {
    Invoke-RestMethod -Uri "$baseUrl/api/jabatans/$jabatanIdToDelete2" -Method Delete -Headers $headers
    Write-Host "OK Unused jabatan deleted successfully" -ForegroundColor Green
} catch {
    Write-Host "X Failed to delete jabatan: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Test Completed ===" -ForegroundColor Cyan
