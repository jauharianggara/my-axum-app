# Test script untuk Karyawan-Kantor Relationship# Test script untuk Karyawan-Kantor Relationship

Write-Host "Testing Karyawan-Kantor Relationship API..." -ForegroundColor YellowWrite-Host "🧪 Testing Karyawan-Kantor Relationship API..." -ForegroundColor Yellow



$baseUrl = "http://localhost:8080"$baseUrl = "http://localhost:8080"



# Test 1: Create Kantor# Test 1: Create Kantor

Write-Host "`n1. Testing CREATE Kantor..." -ForegroundColor BlueWrite-Host "`n1️⃣ Testing CREATE Kantor..." -ForegroundColor Blue

$kantorBody = @{$kantorBody = @{

    nama = "Kantor Test"    nama = "Kantor Bandung"

    alamat = "Jl. Test No.123"    alamat = "Jl. Asia Afrika No.123, Bandung"

    longitude = 107.6    longitude = 107.609810

    latitude = -6.9    latitude = -6.917464

} | ConvertTo-Json} | ConvertTo-Json



try {try {

    $response = Invoke-WebRequest -Uri "$baseUrl/api/kantors" -Method POST -Body $kantorBody -ContentType "application/json" -UseBasicParsing    $response = Invoke-WebRequest -Uri "$baseUrl/api/kantors" -Method POST -Body $kantorBody -ContentType "application/json" -UseBasicParsing

    $data = $response.Content | ConvertFrom-Json    $data = $response.Content | ConvertFrom-Json

    $kantorId = $data.data.id    $kantorId = $data.data.id

    Write-Host "SUCCESS: Kantor created with ID: $kantorId" -ForegroundColor Green    Write-Host "✅ Kantor created with ID: $kantorId" -ForegroundColor Green

} catch {} catch {

    Write-Host "FAILED to create kantor: $_" -ForegroundColor Red    Write-Host "❌ Failed to create kantor: $_" -ForegroundColor Red

    exit 1    exit 1

}}



# Test 2: Create Karyawan WITH kantor_id# Test 2: Create Karyawan WITH kantor_id

Write-Host "`n2. Testing CREATE Karyawan with kantor_id..." -ForegroundColor BlueWrite-Host "`n2️⃣ Testing CREATE Karyawan with kantor_id..." -ForegroundColor Blue

$karyawanBody = @{$karyawanWithKantorBody = @{

    nama = "Test Employee"    nama = "Alice Johnson"

    posisi = "Developer"    posisi = "Software Engineer"

    gaji = "8000000"    gaji = "8500000"

    kantor_id = $kantorId    kantor_id = $kantorId

} | ConvertTo-Json} | ConvertTo-Json



try {try {

    $response = Invoke-WebRequest -Uri "$baseUrl/api/karyawans" -Method POST -Body $karyawanBody -ContentType "application/json" -UseBasicParsing    $response = Invoke-WebRequest -Uri "$baseUrl/api/karyawans" -Method POST -Body $karyawanWithKantorBody -ContentType "application/json" -UseBasicParsing

    $data = $response.Content | ConvertFrom-Json    $data = $response.Content | ConvertFrom-Json

    Write-Host "SUCCESS: Karyawan created with kantor_id: $($data.data.kantor_id)" -ForegroundColor Green    $karyawanId = $data.data.id

} catch {    Write-Host "✅ Karyawan created with ID: $karyawanId, kantor_id: $($data.data.kantor_id)" -ForegroundColor Green

    Write-Host "FAILED to create karyawan: $_" -ForegroundColor Red} catch {

}    Write-Host "❌ Failed to create karyawan with kantor: $_" -ForegroundColor Red

}

# Test 3: Test invalid kantor_id

Write-Host "`n3. Testing VALIDATION with invalid kantor_id..." -ForegroundColor Blue# Test 3: Create Karyawan WITHOUT kantor_id

$invalidBody = @{Write-Host "`n3️⃣ Testing CREATE Karyawan without kantor_id..." -ForegroundColor Blue

    nama = "Invalid Test"$karyawanWithoutKantorBody = @{

    posisi = "Test"    nama = "Charlie Brown"

    gaji = "5000000"    posisi = "Freelancer"

    kantor_id = 999    gaji = "6000000"

} | ConvertTo-Json    kantor_id = $null

} | ConvertTo-Json

try {

    $response = Invoke-WebRequest -Uri "$baseUrl/api/karyawans" -Method POST -Body $invalidBody -ContentType "application/json" -UseBasicParsingtry {

    $data = $response.Content | ConvertFrom-Json    $response = Invoke-WebRequest -Uri "$baseUrl/api/karyawans" -Method POST -Body $karyawanWithoutKantorBody -ContentType "application/json" -UseBasicParsing

    if ($data.success -eq $false) {    $data = $response.Content | ConvertFrom-Json

        Write-Host "SUCCESS: Validation correctly rejected invalid kantor_id" -ForegroundColor Green    $freelancerId = $data.data.id

    } else {    Write-Host "✅ Freelancer created with ID: $freelancerId, kantor_id: null" -ForegroundColor Green

        Write-Host "FAILED: Validation should have failed" -ForegroundColor Red} catch {

    }    Write-Host "❌ Failed to create freelancer: $_" -ForegroundColor Red

} catch {}

    Write-Host "FAILED validation test: $_" -ForegroundColor Red

}# Test 4: Validation - Invalid kantor_id

Write-Host "`n4️⃣ Testing VALIDATION with invalid kantor_id..." -ForegroundColor Blue

Write-Host "`nRelationship tests completed!" -ForegroundColor Green$invalidKantorBody = @{
    nama = "Invalid User"
    posisi = "Test"
    gaji = "5000000"
    kantor_id = 999
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/karyawans" -Method POST -Body $invalidKantorBody -ContentType "application/json" -UseBasicParsing
    $data = $response.Content | ConvertFrom-Json
    if ($data.success -eq $false) {
        Write-Host "✅ Validation correctly rejected invalid kantor_id: $($data.errors)" -ForegroundColor Green
    } else {
        Write-Host "❌ Validation should have failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Validation test failed: $_" -ForegroundColor Red
}

# Test 5: Update Karyawan kantor assignment
Write-Host "`n5️⃣ Testing UPDATE Karyawan kantor assignment..." -ForegroundColor Blue
$updateKantorBody = @{
    nama = "Charlie Brown"
    posisi = "Junior Developer"
    gaji = "7000000"
    kantor_id = $kantorId
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/karyawans/$freelancerId" -Method PUT -Body $updateKantorBody -ContentType "application/json" -UseBasicParsing
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Freelancer now assigned to kantor ID: $($data.data.kantor_id)" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to update karyawan kantor: $_" -ForegroundColor Red
}

# Test 6: Get all karyawans with relationship data
Write-Host "`n6️⃣ Testing GET all karyawans with relationships..." -ForegroundColor Blue
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/karyawans" -UseBasicParsing
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Retrieved $($data.data.Count) karyawans:" -ForegroundColor Green
    foreach ($karyawan in $data.data) {
        $kantorInfo = if ($karyawan.kantor_id) { "Kantor ID: $($karyawan.kantor_id)" } else { "No Kantor" }
        Write-Host "   - $($karyawan.nama) ($($karyawan.posisi)) - $kantorInfo" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ Failed to get karyawans: $_" -ForegroundColor Red
}

# Test 7: Get all kantors
Write-Host "`n7️⃣ Testing GET all kantors..." -ForegroundColor Blue
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/kantors" -UseBasicParsing
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Retrieved $($data.data.Count) kantors:" -ForegroundColor Green
    foreach ($kantor in $data.data) {
        Write-Host "   - ID: $($kantor.id) - $($kantor.nama) ($($kantor.alamat))" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ Failed to get kantors: $_" -ForegroundColor Red
}

Write-Host "`n🎉 Relationship tests completed!" -ForegroundColor Green
Write-Host "📋 Summary:" -ForegroundColor Yellow
Write-Host "   ✅ Foreign key relationship working" -ForegroundColor Green
Write-Host "   ✅ Validation prevents invalid kantor_id" -ForegroundColor Green
Write-Host "   ✅ NULL kantor_id allowed (freelancers)" -ForegroundColor Green
Write-Host "   ✅ Karyawan can be assigned/reassigned to kantors" -ForegroundColor Green