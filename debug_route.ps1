# Debug routing test
Write-Host "Testing API endpoints..." -ForegroundColor Yellow

# Test root endpoint
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/" -Method GET
    Write-Host "✅ Root endpoint: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Root endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test health endpoint
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/health" -Method GET
    Write-Host "✅ Health endpoint: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test karyawan list endpoint
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/api/karyawans" -Method GET
    Write-Host "✅ Karyawan list endpoint: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Karyawan list endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test karyawan by ID endpoint
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/api/karyawans/2" -Method GET
    Write-Host "✅ Karyawan by ID endpoint: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response: $($response.Content)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Karyawan by ID endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "Testing completed!" -ForegroundColor Yellow