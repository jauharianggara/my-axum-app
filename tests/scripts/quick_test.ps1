# Quick Test Script
# Simple PowerShell script to run tests quickly

param(
    [string]$Suite = "all",
    [switch]$Quick,
    [switch]$Help
)

if ($Help) {
    Write-Host "🧪 Karyawan API Test Suite" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\quick_test.ps1 [options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Suite <api|photo|all>  Test suite to run (default: all)"
    Write-Host "  -Quick                  Run only essential tests"
    Write-Host "  -Help                   Show this help"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\quick_test.ps1                    # Run all tests"
    Write-Host "  .\quick_test.ps1 -Suite photo       # Run only photo tests"
    Write-Host "  .\quick_test.ps1 -Quick             # Run quick tests only"
    exit 0
}

Write-Host "🚀 KARYAWAN API QUICK TEST" -ForegroundColor Green
Write-Host "=" * 40

# Check if server is running
Write-Host "🌐 Checking server status..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/health" -Method GET -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Server is running" -ForegroundColor Green
    } else {
        Write-Host "❌ Server returned status $($response.StatusCode)" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Server not available at http://localhost:8080" -ForegroundColor Red
    Write-Host "   Please start the server first: cargo run" -ForegroundColor Yellow
    exit 1
}

# Check Python and dependencies
Write-Host "🐍 Checking Python dependencies..." -ForegroundColor Yellow
try {
    python -c "import requests, PIL" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python dependencies available" -ForegroundColor Green
    } else {
        Write-Host "❌ Missing dependencies. Installing..." -ForegroundColor Red
        pip install requests pillow
    }
} catch {
    Write-Host "❌ Python not available" -ForegroundColor Red
    exit 1
}

# Run tests based on suite
$testsFailed = 0
$testsTotal = 0

if ($Suite -eq "api" -or $Suite -eq "all") {
    Write-Host "`n🔧 Running API Tests..." -ForegroundColor Cyan
    
    # Basic API test
    python tests\api\basic_api_test.py
    if ($LASTEXITCODE -ne 0) { $testsFailed++ }
    $testsTotal++
    
    if (-not $Quick) {
        # CRUD tests
        python tests\api\karyawan_crud_test.py
        if ($LASTEXITCODE -ne 0) { $testsFailed++ }
        $testsTotal++
        
        python tests\api\kantor_crud_test.py
        if ($LASTEXITCODE -ne 0) { $testsFailed++ }
        $testsTotal++
    }
}

if ($Suite -eq "photo" -or $Suite -eq "all") {
    Write-Host "`n📷 Running Photo Tests..." -ForegroundColor Cyan
    
    # Photo functionality test
    python tests\photo\photo_upload_test.py
    if ($LASTEXITCODE -ne 0) { $testsFailed++ }
    $testsTotal++
    
    # Photo validation test
    python tests\photo\photo_validation_test.py
    if ($LASTEXITCODE -ne 0) { $testsFailed++ }
    $testsTotal++
    
    if (-not $Quick) {
        # Performance and security tests
        python tests\photo\photo_performance_test.py
        if ($LASTEXITCODE -ne 0) { $testsFailed++ }
        $testsTotal++
        
        python tests\photo\photo_security_test.py
        if ($LASTEXITCODE -ne 0) { $testsFailed++ }
        $testsTotal++
    }
}

# Final summary
Write-Host "`n📊 FINAL RESULTS" -ForegroundColor Cyan
Write-Host "=" * 40
$testsPassed = $testsTotal - $testsFailed
Write-Host "Tests Passed: $testsPassed" -ForegroundColor Green
Write-Host "Tests Failed: $testsFailed" -ForegroundColor $(if ($testsFailed -eq 0) { "Green" } else { "Red" })
Write-Host "Total Tests:  $testsTotal"
Write-Host "Success Rate: $([math]::Round(($testsPassed / $testsTotal) * 100, 1))%"

if ($testsFailed -eq 0) {
    Write-Host "`n🏆 ALL TESTS PASSED!" -ForegroundColor Green
    Write-Host "Your API is working correctly!" -ForegroundColor Green
} elseif ($testsFailed -le ($testsTotal / 2)) {
    Write-Host "`n⚠️  SOME TESTS FAILED" -ForegroundColor Yellow
    Write-Host "Please review the failed tests above." -ForegroundColor Yellow
} else {
    Write-Host "`n❌ MULTIPLE TEST FAILURES" -ForegroundColor Red
    Write-Host "Significant issues detected. Please investigate." -ForegroundColor Red
}

exit $testsFailed