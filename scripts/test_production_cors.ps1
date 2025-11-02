# Test CORS untuk production server

param(
    [string]$ServerUrl = "http://103.167.113.116:8080",
    [string]$FrontendUrl = "http://103.167.113.116:3000"
)

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   Production CORS Configuration Test" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔧 Configuration:" -ForegroundColor Yellow
Write-Host "   API Server: $ServerUrl" -ForegroundColor White
Write-Host "   Frontend:   $FrontendUrl" -ForegroundColor White
Write-Host ""

# Test 1: Health Check
Write-Host "🔍 Test 1: Server Health Check" -ForegroundColor Yellow
Write-Host "-----------------------------------" -ForegroundColor Gray
try {
    $health = Invoke-WebRequest -Uri "$ServerUrl/health" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "  ✅ Server is running" -ForegroundColor Green
    Write-Host "     Status: $($health.StatusCode)" -ForegroundColor DarkGray
} catch {
    Write-Host "  ❌ Server is not responding!" -ForegroundColor Red
    Write-Host "     Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    exit 1
}
Write-Host ""

# Test 2: CORS Preflight (OPTIONS)
Write-Host "🔍 Test 2: CORS Preflight Request (OPTIONS)" -ForegroundColor Yellow
Write-Host "-----------------------------------" -ForegroundColor Gray
try {
    $preflight = Invoke-WebRequest `
        -Uri "$ServerUrl/api/auth/login" `
        -Method OPTIONS `
        -Headers @{
            "Origin" = $FrontendUrl
            "Access-Control-Request-Method" = "POST"
            "Access-Control-Request-Headers" = "content-type"
        } `
        -ErrorAction Stop

    Write-Host "  ✅ Preflight request successful" -ForegroundColor Green
    Write-Host "     Status: $($preflight.StatusCode)" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  📋 CORS Headers:" -ForegroundColor Cyan
    
    $corsHeaders = @(
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Credentials",
        "Access-Control-Max-Age"
    )
    
    $hasErrors = $false
    foreach ($header in $corsHeaders) {
        $value = $preflight.Headers[$header]
        if ($value) {
            if ($header -eq "Access-Control-Allow-Origin") {
                if ($value -eq $FrontendUrl -or $value -eq "*") {
                    Write-Host "     ✅ $header`: $value" -ForegroundColor Green
                } else {
                    Write-Host "     ❌ $header`: $value (Expected: $FrontendUrl)" -ForegroundColor Red
                    $hasErrors = $true
                }
            } else {
                Write-Host "     ✅ $header`: $value" -ForegroundColor Green
            }
        } else {
            Write-Host "     ⚠️  $header`: Not present" -ForegroundColor Yellow
        }
    }
    
    if ($hasErrors) {
        Write-Host ""
        Write-Host "  ❌ CORS not configured correctly!" -ForegroundColor Red
        Write-Host "     Please check CORS_ORIGINS in .env file" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "  ❌ Preflight request failed!" -ForegroundColor Red
    Write-Host "     Error: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "     Status Code: $statusCode" -ForegroundColor Red
    }
}
Write-Host ""

# Test 3: Actual POST Request
Write-Host "🔍 Test 3: POST Request with CORS" -ForegroundColor Yellow
Write-Host "-----------------------------------" -ForegroundColor Gray
try {
    $body = @{
        username_or_email = "testuser"
        password = "password123"
    } | ConvertTo-Json

    $response = Invoke-WebRequest `
        -Uri "$ServerUrl/api/auth/login" `
        -Method POST `
        -Headers @{
            "Origin" = $FrontendUrl
            "Content-Type" = "application/json"
        } `
        -Body $body `
        -ErrorAction Stop

    Write-Host "  ✅ POST request successful" -ForegroundColor Green
    Write-Host "     Status: $($response.StatusCode)" -ForegroundColor DarkGray
    
    $allowOrigin = $response.Headers["Access-Control-Allow-Origin"]
    if ($allowOrigin -eq $FrontendUrl -or $allowOrigin -eq "*") {
        Write-Host "     ✅ CORS Allow-Origin: $allowOrigin" -ForegroundColor Green
    } else {
        Write-Host "     ⚠️  CORS Allow-Origin: $allowOrigin" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "  ⚠️  POST request failed (expected if no test user)" -ForegroundColor Yellow
    Write-Host "     This is normal - checking CORS headers..." -ForegroundColor DarkGray
    
    # Still check CORS headers even on error
    if ($_.Exception.Response) {
        $errorResponse = $_.Exception.Response
        $allowOrigin = $errorResponse.Headers["Access-Control-Allow-Origin"]
        if ($allowOrigin) {
            Write-Host "     ✅ CORS headers present in error response" -ForegroundColor Green
            Write-Host "     Allow-Origin: $allowOrigin" -ForegroundColor DarkGray
        }
    }
}
Write-Host ""

# Summary
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "              Summary & Recommendations" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "💡 Quick Fixes:" -ForegroundColor Yellow
Write-Host "   # Allow all origins (testing only):" -ForegroundColor Gray
Write-Host "   CORS_ORIGINS=*" -ForegroundColor White
Write-Host ""
Write-Host "   # Production (your IP):" -ForegroundColor Gray
Write-Host "   CORS_ORIGINS=http://103.167.113.116:3000,http://103.167.113.116:5173" -ForegroundColor White
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
