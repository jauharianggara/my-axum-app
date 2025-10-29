# Docker with Schemathesis Testing Integration Script (PowerShell)
# This script builds Docker containers and runs comprehensive API testing

param(
    [string]$ProjectName = "my-axum-app-test",
    [string]$ApiBaseUrl = "http://localhost:8080",
    [int]$TestTimeout = 300,
    [switch]$SkipCleanup,
    [switch]$ShowLogs
)

$ErrorActionPreference = "Stop"

Write-Host "🐳 Docker Build & Schemathesis Testing Integration" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

# Helper functions
function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Check requirements
function Test-Requirements {
    Write-Info "Checking requirements..."
    
    # Check Docker
    try {
        $null = docker --version
        Write-Success "Docker found"
    } catch {
        Write-Error "Docker is not installed or not in PATH"
        exit 1
    }
    
    # Check Docker Compose
    try {
        $null = docker-compose --version
        Write-Success "Docker Compose found"
    } catch {
        Write-Error "Docker Compose is not installed or not in PATH"
        exit 1
    }
    
    # Check Python
    try {
        $null = python --version
        Write-Success "Python found"
    } catch {
        Write-Error "Python is not installed or not in PATH"
        exit 1
    }
    
    # Check required files
    $requiredFiles = @("docker-compose.yml", "Dockerfile", "schemathesis_test.py")
    foreach ($file in $requiredFiles) {
        if (!(Test-Path $file)) {
            Write-Error "Required file not found: $file"
            exit 1
        }
    }
    Write-Success "All required files found"
}

# Setup Python environment
function Initialize-PythonEnvironment {
    Write-Info "Setting up Python testing environment..."
    
    # Create virtual environment if not exists
    if (!(Test-Path "venv")) {
        python -m venv venv
        Write-Success "Python virtual environment created"
    }
    
    # Activate virtual environment
    & .\venv\Scripts\Activate.ps1
    
    # Install requirements
    if (Test-Path "requirements-schemathesis.txt") {
        pip install -r requirements-schemathesis.txt | Out-Null
    } else {
        pip install schemathesis requests hypothesis pytest | Out-Null
    }
    Write-Success "Python dependencies installed"
}

# Clean up previous containers
function Remove-PreviousContainers {
    if (!$SkipCleanup) {
        Write-Info "Cleaning up previous containers..."
        
        try {
            docker-compose -p $ProjectName down --volumes --remove-orphans 2>$null
            docker image prune -f 2>$null
            Write-Success "Cleanup completed"
        } catch {
            Write-Warning "Some cleanup operations failed (this is usually okay)"
        }
    }
}

# Build and start containers
function Start-DockerContainers {
    Write-Info "Building and starting containers..."
    
    # Set environment variable
    $env:COMPOSE_PROJECT_NAME = $ProjectName
    
    try {
        # Build containers
        Write-Info "Building Docker images..."
        docker-compose build --no-cache
        if ($LASTEXITCODE -ne 0) {
            throw "Docker build failed"
        }
        Write-Success "Docker build completed"
        
        # Start services
        Write-Info "Starting services..."
        docker-compose up -d
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to start containers"
        }
        Write-Success "Containers started"
        
    } catch {
        Write-Error "Container startup failed: $_"
        exit 1
    }
}

# Wait for API to be ready
function Wait-ForApi {
    param([string]$Url)
    
    Write-Info "Waiting for API to be ready at $Url..."
    
    $attempts = 0
    $maxAttempts = 30
    
    while ($attempts -lt $maxAttempts) {
        try {
            $response = Invoke-WebRequest -Uri "$Url/health" -TimeoutSec 5 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Success "API is ready!"
                return $true
            }
        } catch {
            Write-Host "." -NoNewline -ForegroundColor Yellow
        }
        
        $attempts++
        Start-Sleep -Seconds 2
    }
    
    Write-Host ""
    Write-Error "API failed to start within timeout"
    return $false
}

# Run Schemathesis tests
function Start-SchemathesisTests {
    Write-Info "Running Schemathesis API tests..."
    
    try {
        # Activate virtual environment
        & .\venv\Scripts\Activate.ps1
        
        # Set environment variables
        $env:API_BASE_URL = $ApiBaseUrl
        $env:MAX_EXAMPLES = "50"
        
        # Run tests
        python schemathesis_test.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Schemathesis tests passed!"
            return $true
        } else {
            Write-Error "Schemathesis tests failed!"
            return $false
        }
    } catch {
        Write-Error "Error running Schemathesis tests: $_"
        return $false
    }
}

# Run validation tests
function Start-ValidationTests {
    Write-Info "Running additional validation tests..."
    
    $testPassed = 0
    $testTotal = 0
    
    # Test 1: Root endpoint
    $testTotal++
    try {
        $response = Invoke-WebRequest -Uri $ApiBaseUrl -TimeoutSec 10 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Success "Root endpoint test passed"
            $testPassed++
        }
    } catch {
        Write-Error "Root endpoint test failed"
    }
    
    # Test 2: Health check
    $testTotal++
    try {
        $response = Invoke-WebRequest -Uri "$ApiBaseUrl/health" -TimeoutSec 10 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Success "Health check test passed"
            $testPassed++
        }
    } catch {
        Write-Error "Health check test failed"
    }
    
    # Test 3: API endpoints
    $testTotal++
    try {
        $response = Invoke-WebRequest -Uri "$ApiBaseUrl/api/karyawans" -TimeoutSec 10 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Success "Karyawans API test passed"
            $testPassed++
        }
    } catch {
        Write-Error "Karyawans API test failed"
    }
    
    $testTotal++
    try {
        $response = Invoke-WebRequest -Uri "$ApiBaseUrl/api/kantors" -TimeoutSec 10 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Success "Kantors API test passed"
            $testPassed++
        }
    } catch {
        Write-Error "Kantors API test failed"
    }
    
    # Test 5: Error handling
    $testTotal++
    try {
        $response = Invoke-WebRequest -Uri "$ApiBaseUrl/api/karyawans/invalid" -TimeoutSec 10 -UseBasicParsing
    } catch {
        if ($_.Exception.Response.StatusCode -eq 400) {
            Write-Success "Error handling test passed"
            $testPassed++
        } else {
            Write-Error "Error handling test failed (expected 400, got $($_.Exception.Response.StatusCode))"
        }
    }
    
    Write-Info "Validation tests: $testPassed/$testTotal passed"
    
    return ($testPassed -eq $testTotal)
}

# Show container logs
function Show-ContainerLogs {
    Write-Info "Container logs:"
    Write-Host "=" * 40 -ForegroundColor Gray
    try {
        docker-compose -p $ProjectName logs --tail=50
    } catch {
        Write-Warning "Could not retrieve container logs"
    }
    Write-Host "=" * 40 -ForegroundColor Gray
}

# Generate test report
function New-TestReport {
    param([bool]$TestSuccess)
    
    $reportFile = "docker_schemathesis_report.md"
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $status = if ($TestSuccess) { "✅ PASSED" } else { "❌ FAILED" }
    
    $report = @"
# Docker + Schemathesis Integration Test Report

**Generated**: $timestamp
**Project**: Karyawan & Kantor Management API
**Status**: $status

## Test Configuration
- Docker Compose Project: $ProjectName
- API Base URL: $ApiBaseUrl
- Test Timeout: ${TestTimeout}s
- Schemathesis Max Examples: 50

## Test Summary
1. ✅ Docker environment setup
2. ✅ Container build and deployment
3. $(if ($TestSuccess) { "✅" } else { "❌" }) API readiness check
4. $(if ($TestSuccess) { "✅" } else { "❌" }) Schemathesis property-based testing
5. $(if ($TestSuccess) { "✅" } else { "❌" }) Manual validation tests

## Files Generated
- OpenAPI Schema: api_schema.json
- Container Logs: Available via docker-compose logs
- Test Report: $reportFile

## Next Steps
$(if ($TestSuccess) {
    "- 🎉 All tests passed! API is ready for production`n- Consider running load tests with additional tools"
} else {
    "- 🔍 Review test failures in the logs above`n- Check container health: docker-compose ps`n- Review API logs: docker-compose logs app"
})

---
Generated by Docker + Schemathesis Integration Test Runner (PowerShell)
"@

    try {
        $report | Out-File -FilePath $reportFile -Encoding UTF8
        Write-Success "Test report saved to: $reportFile"
    } catch {
        Write-Warning "Could not save test report: $_"
    }
}

# Cleanup function
function Invoke-Cleanup {
    if (!$SkipCleanup) {
        Write-Info "Cleaning up..."
        try {
            docker-compose -p $ProjectName down --volumes --remove-orphans 2>$null
        } catch {
            Write-Warning "Cleanup failed (this is usually okay)"
        }
    }
    
    # Deactivate virtual environment if active
    if ($env:VIRTUAL_ENV) {
        deactivate 2>$null
    }
}

# Main execution
try {
    Write-Info "Starting Docker + Schemathesis integration test..."
    
    # Check all requirements
    Test-Requirements
    
    # Setup Python environment
    Initialize-PythonEnvironment
    
    # Clean up any previous containers
    Remove-PreviousContainers
    
    # Build and start containers
    Start-DockerContainers
    
    # Wait for API to be ready
    if (!(Wait-ForApi -Url $ApiBaseUrl)) {
        if ($ShowLogs) {
            Show-ContainerLogs
        }
        Write-Error "API failed to start - use -ShowLogs to see container logs"
        exit 1
    }
    
    # Run tests
    $testSuccess = $true
    
    # Run Schemathesis tests
    if (Start-SchemathesisTests) {
        Write-Success "Schemathesis tests completed successfully"
    } else {
        Write-Error "Schemathesis tests failed"
        $testSuccess = $false
    }
    
    # Run validation tests
    if (Start-ValidationTests) {
        Write-Success "Validation tests completed successfully"
    } else {
        Write-Error "Validation tests failed"
        $testSuccess = $false
    }
    
    # Generate report
    New-TestReport -TestSuccess $testSuccess
    
    # Show logs if requested or if tests failed
    if ($ShowLogs -or !$testSuccess) {
        Show-ContainerLogs
    }
    
    # Final result
    if ($testSuccess) {
        Write-Success "🎉 All tests passed! Docker + API integration successful!"
        Write-Host ""
        Write-Info "Your API is now running at: $ApiBaseUrl"
        Write-Info "To stop containers: docker-compose down"
        exit 0
    } else {
        Write-Error "❌ Some tests failed"
        exit 1
    }
    
} catch {
    Write-Error "Unexpected error: $_"
    exit 1
} finally {
    Invoke-Cleanup
}