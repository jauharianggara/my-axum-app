# Test script untuk validasi API

Write-Host "Testing API Validation..." -ForegroundColor Green

# Test 1: Valid data
Write-Host "`n1. Testing with valid data..." -ForegroundColor Yellow
$validData = @{
    nama = "John Doe"
    posisi = "Software Engineer"
    gaji = 8000000
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:3000/karyawans" -Method POST -Body $validData -ContentType "application/json"
    Write-Host "✓ Valid data response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "✗ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Invalid nama (too short)
Write-Host "`n2. Testing with invalid nama (too short)..." -ForegroundColor Yellow
$invalidData1 = @{
    nama = "A"
    posisi = "Developer"
    gaji = 5000000
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:3000/karyawans" -Method POST -Body $invalidData1 -ContentType "application/json"
    Write-Host "✓ Invalid nama response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "✗ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Invalid gaji (too low)
Write-Host "`n3. Testing with invalid gaji (too low)..." -ForegroundColor Yellow
$invalidData2 = @{
    nama = "Jane Doe"
    posisi = "Manager"
    gaji = 500000
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:3000/karyawans" -Method POST -Body $invalidData2 -ContentType "application/json"
    Write-Host "✓ Invalid gaji response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "✗ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Multiple validation errors
Write-Host "`n4. Testing with multiple validation errors..." -ForegroundColor Yellow
$invalidData3 = @{
    nama = "X"
    posisi = "A"
    gaji = 100
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:3000/karyawans" -Method POST -Body $invalidData3 -ContentType "application/json"
    Write-Host "✓ Multiple errors response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "✗ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nValidation tests completed!" -ForegroundColor Green