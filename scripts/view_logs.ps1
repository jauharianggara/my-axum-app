# View Apache Logs Script
# Monitor different types of logs for Axum API

param(
    [string]$LogType = "all",
    [int]$Lines = 50
)

$LogDir = "/www/wwwlogs"
$Domain = "axum.synergyinfinity.id"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Axum API Apache Logs Viewer" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

function Show-Log {
    param(
        [string]$LogFile,
        [string]$Title,
        [string]$Color = "Yellow"
    )
    
    Write-Host "📋 $Title" -ForegroundColor $Color
    Write-Host "File: $LogFile" -ForegroundColor Gray
    Write-Host "---" -ForegroundColor Gray
    
    if (Test-Path $LogFile) {
        Get-Content $LogFile -Tail $Lines | ForEach-Object {
            if ($_ -match "error|fail|reject|403|404|500|502|503") {
                Write-Host $_ -ForegroundColor Red
            } elseif ($_ -match "200|201|204") {
                Write-Host $_ -ForegroundColor Green
            } elseif ($_ -match "OPTIONS|CORS") {
                Write-Host $_ -ForegroundColor Cyan
            } else {
                Write-Host $_
            }
        }
    } else {
        Write-Host "⚠️  Log file not found: $LogFile" -ForegroundColor Red
    }
    Write-Host ""
}

switch ($LogType.ToLower()) {
    "access" {
        Show-Log "$LogDir/$Domain-access_log" "Access Log (All Requests)" "Green"
    }
    "error" {
        Show-Log "$LogDir/$Domain-error_log" "Error Log (Errors Only)" "Red"
    }
    "detailed" {
        Show-Log "$LogDir/$Domain-detailed_log" "Detailed Log (With Timing)" "Yellow"
    }
    "rejected" {
        Show-Log "$LogDir/$Domain-rejected_log" "Rejected Requests (4xx/5xx)" "Red"
    }
    "cors" {
        Show-Log "$LogDir/$Domain-cors_log" "CORS Requests" "Cyan"
    }
    "all" {
        Show-Log "$LogDir/$Domain-access_log" "1️⃣ Access Log (All Requests)" "Green"
        Show-Log "$LogDir/$Domain-error_log" "2️⃣ Error Log (Errors Only)" "Red"
        Show-Log "$LogDir/$Domain-detailed_log" "3️⃣ Detailed Log (With Timing)" "Yellow"
        Show-Log "$LogDir/$Domain-rejected_log" "4️⃣ Rejected Requests (4xx/5xx)" "Magenta"
        Show-Log "$LogDir/$Domain-cors_log" "5️⃣ CORS Requests" "Cyan"
    }
    default {
        Write-Host "❌ Invalid log type: $LogType" -ForegroundColor Red
        Write-Host ""
        Write-Host "Available log types:" -ForegroundColor Yellow
        Write-Host "  - access    : All incoming requests"
        Write-Host "  - error     : Error messages only"
        Write-Host "  - detailed  : Detailed request info with timing"
        Write-Host "  - rejected  : Rejected requests (4xx/5xx)"
        Write-Host "  - cors      : CORS-related requests"
        Write-Host "  - all       : Show all logs (default)"
        Write-Host ""
        Write-Host "Usage examples:" -ForegroundColor Cyan
        Write-Host "  .\scripts\view_logs.ps1 -LogType access -Lines 100"
        Write-Host "  .\scripts\view_logs.ps1 -LogType error"
        Write-Host "  .\scripts\view_logs.ps1 -Lines 200"
        exit 1
    }
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "✅ Log viewing complete" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
