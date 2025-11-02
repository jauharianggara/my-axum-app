# Log Analysis Script
# Analyze Apache logs for patterns, errors, and statistics

param(
    [int]$Lines = 1000
)

$LogDir = "/www/wwwlogs"
$Domain = "axum.synergyinfinity.id"
$AccessLog = "$LogDir/$Domain-access_log"
$ErrorLog = "$LogDir/$Domain-error_log"
$RejectedLog = "$LogDir/$Domain-rejected_log"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Apache Log Analysis for Axum API" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if file exists
function Test-LogFile {
    param([string]$FilePath)
    if (-not (Test-Path $FilePath)) {
        Write-Host "⚠️  Log file not found: $FilePath" -ForegroundColor Yellow
        return $false
    }
    return $true
}

# Analyze Access Log
if (Test-LogFile $AccessLog) {
    Write-Host "📊 Access Log Statistics (Last $Lines lines)" -ForegroundColor Green
    Write-Host "---" -ForegroundColor Gray
    
    $accessLines = Get-Content $AccessLog -Tail $Lines
    $totalRequests = $accessLines.Count
    
    # Count by HTTP method
    $getMethods = ($accessLines | Select-String -Pattern '"GET ').Count
    $postMethods = ($accessLines | Select-String -Pattern '"POST ').Count
    $putMethods = ($accessLines | Select-String -Pattern '"PUT ').Count
    $deleteMethods = ($accessLines | Select-String -Pattern '"DELETE ').Count
    $optionsMethods = ($accessLines | Select-String -Pattern '"OPTIONS ').Count
    
    # Count by status code
    $status200 = ($accessLines | Select-String -Pattern ' 200 ').Count
    $status201 = ($accessLines | Select-String -Pattern ' 201 ').Count
    $status400 = ($accessLines | Select-String -Pattern ' 400 ').Count
    $status401 = ($accessLines | Select-String -Pattern ' 401 ').Count
    $status403 = ($accessLines | Select-String -Pattern ' 403 ').Count
    $status404 = ($accessLines | Select-String -Pattern ' 404 ').Count
    $status500 = ($accessLines | Select-String -Pattern ' 500 ').Count
    
    Write-Host "  Total Requests: $totalRequests" -ForegroundColor White
    Write-Host ""
    
    Write-Host "  HTTP Methods:" -ForegroundColor Yellow
    Write-Host "    GET:     $getMethods" -ForegroundColor White
    Write-Host "    POST:    $postMethods" -ForegroundColor White
    Write-Host "    PUT:     $putMethods" -ForegroundColor White
    Write-Host "    DELETE:  $deleteMethods" -ForegroundColor White
    Write-Host "    OPTIONS: $optionsMethods" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "  Status Codes:" -ForegroundColor Yellow
    Write-Host "    200 OK:                $status200" -ForegroundColor Green
    Write-Host "    201 Created:           $status201" -ForegroundColor Green
    Write-Host "    400 Bad Request:       $status400" -ForegroundColor Red
    Write-Host "    401 Unauthorized:      $status401" -ForegroundColor Red
    Write-Host "    403 Forbidden:         $status403" -ForegroundColor Red
    Write-Host "    404 Not Found:         $status404" -ForegroundColor Red
    Write-Host "    500 Internal Error:    $status500" -ForegroundColor Red
    Write-Host ""
    
    # Top endpoints
    Write-Host "  Top 10 Endpoints:" -ForegroundColor Yellow
    $accessLines | ForEach-Object {
        if ($_ -match '"[A-Z]+ ([^ ]+) HTTP') {
            $matches[1]
        }
    } | Group-Object | Sort-Object Count -Descending | Select-Object -First 10 | ForEach-Object {
        $endpoint = $_.Name
        $count = $_.Count
        Write-Host "    $count requests: $endpoint" -ForegroundColor White
    }
    Write-Host ""
}

# Analyze Error Log
if (Test-LogFile $ErrorLog) {
    Write-Host "🔴 Error Log Summary (Last $Lines lines)" -ForegroundColor Red
    Write-Host "---" -ForegroundColor Gray
    
    $errorLines = Get-Content $ErrorLog -Tail $Lines
    $totalErrors = $errorLines.Count
    
    if ($totalErrors -eq 0) {
        Write-Host "  ✅ No errors found!" -ForegroundColor Green
    } else {
        Write-Host "  Total Errors: $totalErrors" -ForegroundColor Red
        Write-Host ""
        Write-Host "  Recent Errors:" -ForegroundColor Yellow
        $errorLines | Select-Object -Last 5 | ForEach-Object {
            Write-Host "    $_" -ForegroundColor Red
        }
    }
    Write-Host ""
}

# Analyze Rejected Requests
if (Test-LogFile $RejectedLog) {
    Write-Host "⛔ Rejected Requests (Last $Lines lines)" -ForegroundColor Magenta
    Write-Host "---" -ForegroundColor Gray
    
    $rejectedLines = Get-Content $RejectedLog -Tail $Lines
    $totalRejected = $rejectedLines.Count
    
    if ($totalRejected -eq 0) {
        Write-Host "  ✅ No rejected requests!" -ForegroundColor Green
    } else {
        Write-Host "  Total Rejected: $totalRejected" -ForegroundColor Magenta
        Write-Host ""
        
        # Count by IP address
        Write-Host "  Top IPs with rejected requests:" -ForegroundColor Yellow
        $rejectedLines | ForEach-Object {
            if ($_ -match '^([0-9\.]+)') {
                $matches[1]
            }
        } | Group-Object | Sort-Object Count -Descending | Select-Object -First 5 | ForEach-Object {
            $ip = $_.Name
            $count = $_.Count
            Write-Host "    $ip : $count requests" -ForegroundColor White
        }
    }
    Write-Host ""
}

# Summary
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "✅ Analysis Complete" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Yellow
Write-Host "  - Use .\scripts\view_logs.ps1 to view raw logs"
Write-Host "  - Use .\scripts\monitor_logs.ps1 for real-time monitoring"
Write-Host "  - Increase -Lines parameter for deeper analysis"
Write-Host ""
