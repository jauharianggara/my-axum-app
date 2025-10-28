# Simple Kantor API Test
Write-Host "Testing Kantor API..." -ForegroundColor Green

$baseUrl = "http://localhost:8080"

# Test 1: Get all kantors
Write-Host "1. Testing get all kantors..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors" -Method GET
    Write-Host "SUCCESS: Get all kantors" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 2)
} catch {
    Write-Host "FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Get kantor by ID
Write-Host "`n2. Testing get kantor by ID..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors/1" -Method GET
    Write-Host "SUCCESS: Get kantor by ID" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 2)
} catch {
    Write-Host "FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Create new kantor
Write-Host "`n3. Testing create kantor..." -ForegroundColor Yellow
$newKantor = @{
    nama = "Kantor Test API"
    alamat = "Jl. API Test No.99"
    longitude = 110.123456
    latitude = -7.654321
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors" -Method POST -Body $newKantor -ContentType "application/json"
    Write-Host "SUCCESS: Create kantor" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 2)
} catch {
    Write-Host "FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Test validation (invalid longitude)
Write-Host "`n4. Testing validation (invalid longitude)..." -ForegroundColor Yellow
$invalidKantor = @{
    nama = "Kantor Invalid"
    alamat = "Jl. Invalid No.1"
    longitude = 200.0
    latitude = -7.654321
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors" -Method POST -Body $invalidKantor -ContentType "application/json"
    Write-Host "SUCCESS: Validation test" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 2)
} catch {
    Write-Host "FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Test validation (invalid latitude)
Write-Host "`n5. Testing validation (invalid latitude)..." -ForegroundColor Yellow
$invalidKantor2 = @{
    nama = "Kantor Invalid 2"
    alamat = "Jl. Invalid No.2"
    longitude = 110.123456
    latitude = -95.0
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors" -Method POST -Body $invalidKantor2 -ContentType "application/json"
    Write-Host "SUCCESS: Validation test 2" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 2)
} catch {
    Write-Host "FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 6: Update kantor
Write-Host "`n6. Testing update kantor..." -ForegroundColor Yellow
$updateKantor = @{
    nama = "Kantor Updated"
    alamat = "Jl. Updated No.123"
    longitude = 115.555555
    latitude = -8.111111
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors/1" -Method PUT -Body $updateKantor -ContentType "application/json"
    Write-Host "SUCCESS: Update kantor" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 2)
} catch {
    Write-Host "FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 7: Delete kantor
Write-Host "`n7. Testing delete kantor..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors/2" -Method DELETE
    Write-Host "SUCCESS: Delete kantor" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 2)
} catch {
    Write-Host "FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nKantor API testing completed!" -ForegroundColor Green