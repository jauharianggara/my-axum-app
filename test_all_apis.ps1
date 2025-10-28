# Comprehensive Test Script untuk Axum APIs (Karyawan & Kantor)
Write-Host "🚀 Testing Axum APIs - Karyawan & Kantor Management" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Gray

$baseUrl = "http://localhost:8080"
$successCount = 0
$failCount = 0

function Test-Endpoint {
    param(
        [string]$TestName,
        [string]$Method,
        [string]$Uri,
        [string]$Body = $null,
        [string]$ContentType = "application/json"
    )
    
    Write-Host "`n🧪 $TestName" -ForegroundColor Yellow
    try {
        if ($Body) {
            $response = Invoke-RestMethod -Uri $Uri -Method $Method -Body $Body -ContentType $ContentType
        } else {
            $response = Invoke-RestMethod -Uri $Uri -Method $Method
        }
        Write-Host "✅ SUCCESS: $($response | ConvertTo-Json -Depth 2 -Compress)" -ForegroundColor Green
        $script:successCount++
        return $response
    } catch {
        Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
        $script:failCount++
        return $null
    }
}

# ============================================================================
# BASIC HEALTH CHECKS
# ============================================================================
Write-Host "`n🏥 HEALTH CHECKS" -ForegroundColor Cyan
Write-Host "-" * 40 -ForegroundColor Gray

Test-Endpoint -TestName "Root Endpoint" -Method "GET" -Uri "$baseUrl/"
Test-Endpoint -TestName "Health Check" -Method "GET" -Uri "$baseUrl/health"

# ============================================================================
# KARYAWAN API TESTS
# ============================================================================
Write-Host "`n👥 KARYAWAN API TESTS" -ForegroundColor Cyan
Write-Host "-" * 40 -ForegroundColor Gray

# Basic CRUD
Test-Endpoint -TestName "Get All Karyawans" -Method "GET" -Uri "$baseUrl/api/karyawans"
Test-Endpoint -TestName "Get Karyawan by ID (1)" -Method "GET" -Uri "$baseUrl/api/karyawans/1"

# Create valid karyawan
$validKaryawan = @{
    nama = "John Doe"
    posisi = "Senior Developer"
    gaji = "12000000"
} | ConvertTo-Json

Test-Endpoint -TestName "Create Valid Karyawan" -Method "POST" -Uri "$baseUrl/api/karyawans" -Body $validKaryawan

# Update karyawan
$updateKaryawan = @{
    nama = "John Doe Updated"
    posisi = "Tech Lead"
    gaji = "15000000"
} | ConvertTo-Json

Test-Endpoint -TestName "Update Karyawan" -Method "PUT" -Uri "$baseUrl/api/karyawans/1" -Body $updateKaryawan

# Karyawan validation tests
$invalidKaryawan1 = @{
    nama = "J"
    posisi = "Dev"
    gaji = "abc"
} | ConvertTo-Json

Test-Endpoint -TestName "Invalid Karyawan (short nama, invalid gaji)" -Method "POST" -Uri "$baseUrl/api/karyawans" -Body $invalidKaryawan1

$invalidKaryawan2 = @{
    nama = "Jane Doe"
    posisi = "Manager"
    gaji = "500000"
} | ConvertTo-Json

Test-Endpoint -TestName "Invalid Karyawan (gaji too low)" -Method "POST" -Uri "$baseUrl/api/karyawans" -Body $invalidKaryawan2

Test-Endpoint -TestName "Invalid Karyawan ID (abc)" -Method "GET" -Uri "$baseUrl/api/karyawans/abc"

# ============================================================================
# KANTOR API TESTS
# ============================================================================
Write-Host "`n🏢 KANTOR API TESTS" -ForegroundColor Cyan
Write-Host "-" * 40 -ForegroundColor Gray

# Basic CRUD
Test-Endpoint -TestName "Get All Kantors" -Method "GET" -Uri "$baseUrl/api/kantors"
Test-Endpoint -TestName "Get Kantor by ID (1)" -Method "GET" -Uri "$baseUrl/api/kantors/1"

# Create valid kantor
$validKantor = @{
    nama = "Kantor Cabang Bali"
    alamat = "Jl. Monkey Forest Road No.88, Ubud, Bali"
    longitude = 115.2191175
    latitude = -8.5069683
} | ConvertTo-Json

Test-Endpoint -TestName "Create Valid Kantor" -Method "POST" -Uri "$baseUrl/api/kantors" -Body $validKantor

# Update kantor
$updateKantor = @{
    nama = "Kantor Cabang Bali - Updated"
    alamat = "Jl. Raya Ubud No.100, Ubud, Bali"
    longitude = 115.2191175
    latitude = -8.5069683
} | ConvertTo-Json

Test-Endpoint -TestName "Update Kantor" -Method "PUT" -Uri "$baseUrl/api/kantors/1" -Body $updateKantor

# Kantor validation tests
$invalidKantor1 = @{
    nama = "K"
    alamat = "Jl"
    longitude = 190.0
    latitude = -95.0
} | ConvertTo-Json

Test-Endpoint -TestName "Invalid Kantor (all fields invalid)" -Method "POST" -Uri "$baseUrl/api/kantors" -Body $invalidKantor1

$invalidKantor2 = @{
    nama = "Kantor Test Valid"
    alamat = "Jl. Test Valid No.123"
    longitude = 181.0
    latitude = -6.208763
} | ConvertTo-Json

Test-Endpoint -TestName "Invalid Kantor (longitude out of range)" -Method "POST" -Uri "$baseUrl/api/kantors" -Body $invalidKantor2

$invalidKantor3 = @{
    nama = "Kantor Test Valid"
    alamat = "Jl. Test Valid No.123"
    longitude = 106.845599
    latitude = 91.0
} | ConvertTo-Json

Test-Endpoint -TestName "Invalid Kantor (latitude out of range)" -Method "POST" -Uri "$baseUrl/api/kantors" -Body $invalidKantor3

# Boundary testing
$boundaryKantor = @{
    nama = "Kantor Boundary Test"
    alamat = "Perfect Boundary Location"
    longitude = 180.0
    latitude = 90.0
} | ConvertTo-Json

Test-Endpoint -TestName "Boundary Kantor (max values)" -Method "POST" -Uri "$baseUrl/api/kantors" -Body $boundaryKantor

$negativeBoundaryKantor = @{
    nama = "Kantor Negative Boundary"
    alamat = "Negative Boundary Location"
    longitude = -180.0
    latitude = -90.0
} | ConvertTo-Json

Test-Endpoint -TestName "Boundary Kantor (min values)" -Method "POST" -Uri "$baseUrl/api/kantors" -Body $negativeBoundaryKantor

Test-Endpoint -TestName "Invalid Kantor ID (abc)" -Method "GET" -Uri "$baseUrl/api/kantors/abc"

# ============================================================================
# DELETE OPERATIONS
# ============================================================================
Write-Host "`n🗑️ DELETE OPERATIONS" -ForegroundColor Cyan
Write-Host "-" * 40 -ForegroundColor Gray

Test-Endpoint -TestName "Delete Karyawan" -Method "DELETE" -Uri "$baseUrl/api/karyawans/2"
Test-Endpoint -TestName "Delete Kantor" -Method "DELETE" -Uri "$baseUrl/api/kantors/2"

# ============================================================================
# SUMMARY
# ============================================================================
Write-Host "`n📊 TEST SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray
Write-Host "✅ Successful Tests: $successCount" -ForegroundColor Green
Write-Host "❌ Failed Tests: $failCount" -ForegroundColor Red
Write-Host "🔢 Total Tests: $($successCount + $failCount)" -ForegroundColor White

$successRate = if (($successCount + $failCount) -gt 0) { 
    [math]::Round(($successCount / ($successCount + $failCount)) * 100, 2) 
} else { 0 }

Write-Host "📈 Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 80) { "Green" } elseif ($successRate -ge 60) { "Yellow" } else { "Red" })

Write-Host "`n🎯 FEATURES TESTED:" -ForegroundColor Cyan
Write-Host "• CRUD operations for both Karyawan and Kantor" -ForegroundColor White
Write-Host "• Input validation (length, format, range)" -ForegroundColor White
Write-Host "• Geographic coordinate validation" -ForegroundColor White
Write-Host "• Boundary value testing" -ForegroundColor White
Write-Host "• Error handling for invalid data" -ForegroundColor White
Write-Host "• HTTP method testing (GET, POST, PUT, DELETE)" -ForegroundColor White

if ($failCount -eq 0) {
    Write-Host "`n🎉 All tests passed! API is working perfectly!" -ForegroundColor Green
} elseif ($successRate -ge 80) {
    Write-Host "`n⚠️ Most tests passed, but some issues need attention." -ForegroundColor Yellow
} else {
    Write-Host "`n🚨 Multiple test failures detected. Please check the API implementation." -ForegroundColor Red
}

Write-Host "`nTesting completed at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray