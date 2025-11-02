# Script untuk test CORS configuration

param(
    [string]$ServerUrl = "http://localhost:8080",
    [string]$Origin = "http://localhost:3000"
)

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "        CORS Configuration Testing" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔧 Test Configuration:" -ForegroundColor Yellow
Write-Host "   Server URL: $ServerUrl" -ForegroundColor White
Write-Host "   Test Origin: $Origin" -ForegroundColor White
Write-Host ""

# Check if server is running
Write-Host "🔍 Checking if server is running..." -ForegroundColor Yellow
try {
    $healthCheck = Invoke-WebRequest -Uri "$ServerUrl/health" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Server is running!" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "❌ Server is not responding!" -ForegroundColor Red
    Write-Host "💡 Please start the server first: cargo run" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Test CORS preflight request
Write-Host "🧪 Testing CORS Preflight Request..." -ForegroundColor Yellow
Write-Host "-----------------------------------" -ForegroundColor Gray

try {
    $response = Invoke-WebRequest `
        -Uri "$ServerUrl/api/auth/login" `
        -Method OPTIONS `
        -Headers @{
            "Origin" = $Origin
            "Access-Control-Request-Method" = "POST"
            "Access-Control-Request-Headers" = "content-type,authorization"
        } `
        -ErrorAction Stop

    Write-Host "✅ CORS Preflight Response:" -ForegroundColor Green
    Write-Host ""
    
    # Check important CORS headers
    $corsHeaders = @{
        "Access-Control-Allow-Origin" = $response.Headers["Access-Control-Allow-Origin"]
        "Access-Control-Allow-Methods" = $response.Headers["Access-Control-Allow-Methods"]
        "Access-Control-Allow-Headers" = $response.Headers["Access-Control-Allow-Headers"]
        "Access-Control-Allow-Credentials" = $response.Headers["Access-Control-Allow-Credentials"]
    }

    foreach ($header in $corsHeaders.GetEnumerator()) {
        if ($header.Value) {
            Write-Host "  ✅ $($header.Key): $($header.Value)" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $($header.Key): Not present" -ForegroundColor Red
        }
    }
    Write-Host ""

    # Validate CORS configuration
    Write-Host "🔍 CORS Configuration Validation:" -ForegroundColor Yellow
    Write-Host "-----------------------------------" -ForegroundColor Gray
    
    $allowedOrigin = $response.Headers["Access-Control-Allow-Origin"]
    if ($allowedOrigin -eq $Origin) {
        Write-Host "  ✅ Origin '$Origin' is allowed" -ForegroundColor Green
    } elseif ($allowedOrigin -eq "*") {
        Write-Host "  ⚠️  Warning: Wildcard (*) origin detected - Not secure for production!" -ForegroundColor Yellow
    } else {
        Write-Host "  ❌ Origin '$Origin' is NOT allowed" -ForegroundColor Red
        Write-Host "     Allowed: $allowedOrigin" -ForegroundColor Gray
    }

    $allowedMethods = $response.Headers["Access-Control-Allow-Methods"]
    if ($allowedMethods -match "POST") {
        Write-Host "  ✅ POST method is allowed" -ForegroundColor Green
    } else {
        Write-Host "  ❌ POST method is NOT allowed" -ForegroundColor Red
    }

    $allowsCredentials = $response.Headers["Access-Control-Allow-Credentials"]
    if ($allowsCredentials -eq "true") {
        Write-Host "  ✅ Credentials are allowed" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Credentials are NOT allowed" -ForegroundColor Yellow
        if ($allowedOrigin -eq "*") {
            Write-Host "     (Expected with wildcard origin)" -ForegroundColor DarkGray
        }
    }

} catch {
    Write-Host "❌ CORS Preflight Request Failed!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test different origins from .env
Write-Host "🧪 Testing Origins from .env Configuration..." -ForegroundColor Yellow
Write-Host "-----------------------------------" -ForegroundColor Gray

if (Test-Path ".env") {
    $corsOriginsLine = Get-Content .env | Where-Object { $_ -match "^CORS_ORIGINS=" }
    if ($corsOriginsLine) {
        $corsOrigins = ($corsOriginsLine -replace "^CORS_ORIGINS=", "")
        
        if ($corsOrigins.Trim() -eq "*") {
            Write-Host "⚠️  Wildcard (*) detected - Testing random origins:" -ForegroundColor Yellow
            Write-Host ""
            
            $testOrigins = @(
                "http://random-domain.com",
                "https://another-site.org",
                $Origin
            )
            
            foreach ($testOrigin in $testOrigins) {
                Write-Host "Testing: $testOrigin" -ForegroundColor Cyan
                
                try {
                    $testResponse = Invoke-WebRequest `
                        -Uri "$ServerUrl/api/auth/login" `
                        -Method OPTIONS `
                        -Headers @{
                            "Origin" = $testOrigin
                            "Access-Control-Request-Method" = "POST"
                        } `
                        -ErrorAction Stop

                    $allowedOrigin = $testResponse.Headers["Access-Control-Allow-Origin"]
                    if ($allowedOrigin -eq "*") {
                        Write-Host "  ✅ ALLOWED (Wildcard)" -ForegroundColor Green
                    } else {
                        Write-Host "  ❌ Response: $allowedOrigin" -ForegroundColor Red
                    }
                } catch {
                    Write-Host "  ❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
                }
                Write-Host ""
            }
        } else {
            $originList = $corsOrigins -split ","
            Write-Host "Found $($originList.Count) configured origins:" -ForegroundColor White
            Write-Host ""
            
            foreach ($testOrigin in $originList) {
                $testOrigin = $testOrigin.Trim()
                if ($testOrigin) {
                    Write-Host "Testing: $testOrigin" -ForegroundColor Cyan
                    
                    try {
                        $testResponse = Invoke-WebRequest `
                            -Uri "$ServerUrl/api/auth/login" `
                            -Method OPTIONS `
                            -Headers @{
                                "Origin" = $testOrigin
                                "Access-Control-Request-Method" = "POST"
                            } `
                            -ErrorAction Stop

                        $allowedOrigin = $testResponse.Headers["Access-Control-Allow-Origin"]
                        if ($allowedOrigin -eq $testOrigin -or $allowedOrigin -eq "*") {
                            Write-Host "  ✅ ALLOWED" -ForegroundColor Green
                        } else {
                            Write-Host "  ❌ BLOCKED (got: $allowedOrigin)" -ForegroundColor Red
                        }
                    } catch {
                        Write-Host "  ❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
                    }
                    Write-Host ""
                }
            }
        }
    }
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "💡 Tips:" -ForegroundColor Yellow
Write-Host "   - Update CORS_ORIGINS in .env file to add/remove origins" -ForegroundColor Gray
Write-Host "   - Restart server after changing .env file" -ForegroundColor Gray
Write-Host "   - Use specific origins in production (avoid wildcard *)" -ForegroundColor Gray
Write-Host "   - Test with: .\scripts\test_cors_config.ps1 -Origin 'http://your-url'" -ForegroundColor Gray
Write-Host "==================================================" -ForegroundColor Cyan
