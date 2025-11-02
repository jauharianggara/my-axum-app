# Environment Configuration Check Script

Write-Host '=================================================='
Write-Host '  Environment Variables Configuration Check'
Write-Host '=================================================='
Write-Host ''

# Check if .env file exists
if (Test-Path '.env') {
    Write-Host 'OK: .env file found' -ForegroundColor Green
    Write-Host ''
    
    # Read and display .env contents
    Write-Host 'Current Configuration:' -ForegroundColor Yellow
    Write-Host '-----------------------------------'
    
    Get-Content .env | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            $key = $matches[1]
            $value = $matches[2]
            
            # Mask sensitive values
            if ($key -match '(SECRET|PASSWORD|URL)') {
                $maskedValue = '*****' + $value.Substring([Math]::Max(0, $value.Length - 4))
                Write-Host "$key=$maskedValue" -ForegroundColor Gray
            } else {
                Write-Host "$key=$value"
            }
        }
    }
    Write-Host ''
} else {
    Write-Host 'ERROR: .env file not found!' -ForegroundColor Red
    Write-Host 'TIP: Copy .env.example to .env' -ForegroundColor Yellow
    Write-Host ''
    exit 1
}

# Check required variables
Write-Host 'Checking Required Variables:' -ForegroundColor Yellow
Write-Host '-----------------------------------'

$requiredVars = @('DATABASE_URL', 'APP_HOST', 'APP_PORT', 'JWT_SECRET', 'ENVIRONMENT', 'CORS_ORIGINS')

$allPresent = $true
foreach ($var in $requiredVars) {
    $line = Get-Content .env | Where-Object { $_ -match "^$var=" }
    if ($line) {
        $value = $line -replace "^$var=", ''
        Write-Host "OK: $var" -ForegroundColor Green
        
        # Additional checks
        if ($var -eq 'CORS_ORIGINS' -and $value.Trim() -eq '*') {
            Write-Host '   WARNING: Wildcard - ALL origins allowed!' -ForegroundColor Yellow
        }
        if ($var -eq 'JWT_SECRET' -and $value.Length -lt 32) {
            Write-Host '   WARNING: Should be at least 32 characters' -ForegroundColor Yellow
        }
    } else {
        Write-Host "ERROR: $var (Missing)" -ForegroundColor Red
        $allPresent = $false
    }
}

Write-Host ''

if ($allPresent) {
    Write-Host 'RESULT: All required variables configured!' -ForegroundColor Green
} else {
    Write-Host 'RESULT: Some variables are missing!' -ForegroundColor Red
}

Write-Host ''
Write-Host '=================================================='
