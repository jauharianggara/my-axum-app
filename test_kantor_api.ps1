# Test script untuk Axum Kantor API
Write-Host "Testing Axum Kantor API..." -ForegroundColor Green

$baseUrl = "http://localhost:8080"

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

# Test 3: Get all kantors
Write-Host "`n3. Testing get all kantors..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors" -Method GET
    Write-Host "✓ Get all kantors: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Get all kantors failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Get kantor by ID
Write-Host "`n4. Testing get kantor by ID..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors/1" -Method GET
    Write-Host "✓ Get kantor by ID: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Get kantor by ID failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Create new kantor with valid data
Write-Host "`n5. Testing create kantor (valid data)..." -ForegroundColor Yellow
$newKantor = @{
    nama = "Kantor Cabang Surabaya"
    alamat = "Jl. Pemuda No.15, Surabaya"
    longitude = 112.768845
    latitude = -7.250445
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors" -Method POST -Body $newKantor -ContentType "application/json"
    Write-Host "✓ Create kantor: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Create kantor failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 6: Test validation with invalid nama (too short)
Write-Host "`n6. Testing validation (nama too short)..." -ForegroundColor Yellow
$invalidKantor1 = @{
    nama = "K"
    alamat = "Jl. Test No.1"
    longitude = 106.845599
    latitude = -6.208763
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors" -Method POST -Body $invalidKantor1 -ContentType "application/json"
    Write-Host "✓ Validation test (short nama): $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Validation test (short nama) failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 7: Test validation with invalid alamat (too short)
Write-Host "`n7. Testing validation (alamat too short)..." -ForegroundColor Yellow
$invalidKantor2 = @{
    nama = "Kantor Test"
    alamat = "Jl"
    longitude = 106.845599
    latitude = -6.208763
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors" -Method POST -Body $invalidKantor2 -ContentType "application/json"
    Write-Host "✓ Validation test (short alamat): $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Validation test (short alamat) failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 8: Test validation with invalid longitude (out of range)
Write-Host "`n8. Testing validation (invalid longitude)..." -ForegroundColor Yellow
$invalidKantor3 = @{
    nama = "Kantor Test"
    alamat = "Jl. Test No.123"
    longitude = 190.0
    latitude = -6.208763
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors" -Method POST -Body $invalidKantor3 -ContentType "application/json"
    Write-Host "✓ Validation test (invalid longitude): $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Validation test (invalid longitude) failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 9: Test validation with invalid latitude (out of range)
Write-Host "`n9. Testing validation (invalid latitude)..." -ForegroundColor Yellow
$invalidKantor4 = @{
    nama = "Kantor Test"
    alamat = "Jl. Test No.123"
    longitude = 106.845599
    latitude = -95.0
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors" -Method POST -Body $invalidKantor4 -ContentType "application/json"
    Write-Host "✓ Validation test (invalid latitude): $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Validation test (invalid latitude) failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 10: Update kantor with valid data
Write-Host "`n10. Testing update kantor..." -ForegroundColor Yellow
$updateKantor = @{
    nama = "Kantor Cabang Medan Updated"
    alamat = "Jl. Gatot Subroto No.25, Medan"
    longitude = 98.678333
    latitude = 3.595196
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors/1" -Method PUT -Body $updateKantor -ContentType "application/json"
    Write-Host "✓ Update kantor: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Update kantor failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 11: Test invalid ID format
Write-Host "`n11. Testing invalid ID format..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors/abc" -Method GET
    Write-Host "✓ Invalid ID test result: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Invalid ID test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 12: Delete kantor
Write-Host "`n12. Testing delete kantor..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors/2" -Method DELETE
    Write-Host "✓ Delete kantor: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Delete kantor failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 13: Test edge case coordinates (boundary values)
Write-Host "`n13. Testing boundary coordinates..." -ForegroundColor Yellow
$boundaryKantor = @{
    nama = "Kantor Boundary Test"
    alamat = "Boundary Location Test"
    longitude = 180.0
    latitude = 90.0
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors" -Method POST -Body $boundaryKantor -ContentType "application/json"
    Write-Host "✓ Boundary coordinates test: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Boundary coordinates test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 14: Test negative boundary coordinates
Write-Host "`n14. Testing negative boundary coordinates..." -ForegroundColor Yellow
$negativeBoundaryKantor = @{
    nama = "Kantor Negative Boundary"
    alamat = "Negative Boundary Location"
    longitude = -180.0
    latitude = -90.0
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/kantors" -Method POST -Body $negativeBoundaryKantor -ContentType "application/json"
    Write-Host "✓ Negative boundary coordinates test: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Green
} catch {
    Write-Host "✗ Negative boundary coordinates test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "Testing completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host "- Basic CRUD operations tested" -ForegroundColor White
Write-Host "- Validation rules tested (nama and alamat length)" -ForegroundColor White
Write-Host "- Coordinate validation tested (longitude: -180 to 180, latitude: -90 to 90)" -ForegroundColor White
Write-Host "- Boundary value testing included" -ForegroundColor White
Write-Host "- Error handling for invalid ID formats tested" -ForegroundColor White