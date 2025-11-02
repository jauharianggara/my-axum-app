# Real-time Log Monitor Script
# Watch Apache logs in real-time (similar to tail -f)

param(
    [string]$LogType = "access"
)

$LogDir = "/www/wwwlogs"
$Domain = "axum.synergyinfinity.id"

$LogFiles = @{
    "access" = "$LogDir/$Domain-access_log"
    "error" = "$LogDir/$Domain-error_log"
    "detailed" = "$LogDir/$Domain-detailed_log"
    "rejected" = "$LogDir/$Domain-rejected_log"
    "cors" = "$LogDir/$Domain-cors_log"
}

if (-not $LogFiles.ContainsKey($LogType.ToLower())) {
    Write-Host "❌ Invalid log type: $LogType" -ForegroundColor Red
    Write-Host ""
    Write-Host "Available log types:" -ForegroundColor Yellow
    Write-Host "  - access    : All incoming requests"
    Write-Host "  - error     : Error messages only"
    Write-Host "  - detailed  : Detailed request info"
    Write-Host "  - rejected  : Rejected requests (4xx/5xx)"
    Write-Host "  - cors      : CORS-related requests"
    exit 1
}

$LogFile = $LogFiles[$LogType.ToLower()]

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Real-time Log Monitor" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Monitoring: $LogFile" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop..." -ForegroundColor Gray
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $LogFile)) {
    Write-Host "⚠️  Log file not found: $LogFile" -ForegroundColor Red
    Write-Host "Creating file..." -ForegroundColor Yellow
    New-Item -ItemType File -Path $LogFile -Force | Out-Null
}

# Monitor file in real-time
Get-Content $LogFile -Wait -Tail 10 | ForEach-Object {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    if ($_ -match "error|fail|reject|403|404|500|502|503") {
        Write-Host "[$timestamp] " -NoNewline -ForegroundColor Gray
        Write-Host $_ -ForegroundColor Red
    } elseif ($_ -match "200|201|204") {
        Write-Host "[$timestamp] " -NoNewline -ForegroundColor Gray
        Write-Host $_ -ForegroundColor Green
    } elseif ($_ -match "OPTIONS|CORS|Origin") {
        Write-Host "[$timestamp] " -NoNewline -ForegroundColor Gray
        Write-Host $_ -ForegroundColor Cyan
    } elseif ($_ -match "POST|PUT|DELETE") {
        Write-Host "[$timestamp] " -NoNewline -ForegroundColor Gray
        Write-Host $_ -ForegroundColor Yellow
    } else {
        Write-Host "[$timestamp] " -NoNewline -ForegroundColor Gray
        Write-Host $_
    }
}
