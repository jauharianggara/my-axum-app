# Simple Test Runner
# PowerShell script to run organized tests

param(
    [string]$Suite = "all",
    [switch]$Quick,
    [switch]$Help
)

if ($Help) {
    Write-Host "Test Suite Runner" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\simple_test.ps1 [options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Suite <api|photo|all>  Test suite to run (default: all)"
    Write-Host "  -Quick                  Run only essential tests"
    Write-Host "  -Help                   Show this help"
    exit 0
}

Write-Host "KARYAWAN API TEST RUNNER" -ForegroundColor Green
Write-Host "========================="

# Check if server is running
Write-Host "Checking server..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/health" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "Server is running" -ForegroundColor Green
} catch {
    Write-Host "Server not available" -ForegroundColor Red
    Write-Host "Please start the server first: cargo run" -ForegroundColor Yellow
    exit 1
}

$testsFailed = 0
$testsTotal = 0

if ($Suite -eq "api" -or $Suite -eq "all") {
    Write-Host "`nRunning API Tests..." -ForegroundColor Cyan
    
    python tests\api\basic_api_test.py
    if ($LASTEXITCODE -ne 0) { $testsFailed++ }
    $testsTotal++
    
    if (-not $Quick) {
        python tests\api\karyawan_crud_test.py
        if ($LASTEXITCODE -ne 0) { $testsFailed++ }
        $testsTotal++
        
        python tests\api\kantor_crud_test.py
        if ($LASTEXITCODE -ne 0) { $testsFailed++ }
        $testsTotal++
    }
}

if ($Suite -eq "photo" -or $Suite -eq "all") {
    Write-Host "`nRunning Photo Tests..." -ForegroundColor Cyan
    
    python tests\photo\photo_upload_test.py
    if ($LASTEXITCODE -ne 0) { $testsFailed++ }
    $testsTotal++
    
    python tests\photo\photo_validation_test.py
    if ($LASTEXITCODE -ne 0) { $testsFailed++ }
    $testsTotal++
    
    if (-not $Quick) {
        python tests\photo\photo_performance_test.py
        if ($LASTEXITCODE -ne 0) { $testsFailed++ }
        $testsTotal++
        
        python tests\photo\photo_security_test.py
        if ($LASTEXITCODE -ne 0) { $testsFailed++ }
        $testsTotal++
    }
}

# Summary
Write-Host "`nFINAL RESULTS" -ForegroundColor Cyan
Write-Host "============="
$testsPassed = $testsTotal - $testsFailed
Write-Host "Tests Passed: $testsPassed" -ForegroundColor Green
Write-Host "Tests Failed: $testsFailed" -ForegroundColor $(if ($testsFailed -eq 0) { "Green" } else { "Red" })
Write-Host "Success Rate: $([math]::Round(($testsPassed / $testsTotal) * 100, 1))%"

if ($testsFailed -eq 0) {
    Write-Host "`nALL TESTS PASSED!" -ForegroundColor Green
} else {
    Write-Host "`nSOME TESTS FAILED" -ForegroundColor Yellow
}

exit $testsFailed