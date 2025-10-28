# Test script untuk Axum Karyawan API
Write-Host "Testing Axum Karyawan API..." -ForegroundColor Green

$baseUrl = "http://localhost:3000"

# Test 1: Root endpoint
Write-Host "`n1. Testing root endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/" -Method GET
    Write-Host "✓ Root: $response" -ForegroundColor Green
} catch {
    Write-Host "✗ Root failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Health check
Write-Host "`n2. Testing health check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/health" -Method GET
    Write-Host "✓ Health: $($response | ConvertTo-Json)" -ForegroundColor Green
} catch {
    Write-Host "✗ Health failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Get all karyawans
Write-Host "`n3. Testing get all karyawans..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/karyawans" -Method GET
    Write-Host "✓ Get all karyawans: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Get all karyawans failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Get karyawan by ID
Write-Host "`n4. Testing get karyawan by ID..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/karyawans/1" -Method GET
    Write-Host "✓ Get karyawan by ID: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Get karyawan by ID failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Create new karyawan
Write-Host "`n5. Testing create karyawan..." -ForegroundColor Yellow
$newKaryawan = @{
    nama = "Joko Widodo"
    posisi = "President"
    gaji = "15000000"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/karyawans" -Method POST -Body $newKaryawan -ContentType "application/json"
    Write-Host "✓ Create karyawan: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Create karyawan failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 6: Test validation with invalid gaji
Write-Host "`n6. Testing validation (invalid gaji)..." -ForegroundColor Yellow
$invalidKaryawan = @{
    nama = "Test User"
    posisi = "Tester"
    gaji = "abc"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/karyawans" -Method POST -Body $invalidKaryawan -ContentType "application/json"
    Write-Host "✓ Validation test result: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Validation test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 7: Test invalid ID format
Write-Host "`n7. Testing invalid ID format..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/karyawans/abc" -Method GET
    Write-Host "✓ Invalid ID test result: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Invalid ID test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "Testing completed!" -ForegroundColor Green