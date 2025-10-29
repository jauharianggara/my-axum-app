#!/bin/bash

# Docker with Schemathesis Testing Integration Script
# This script builds Docker containers and runs comprehensive API testing

set -e

echo "🐳 Docker Build & Schemathesis Testing Integration"
echo "=" * 60

# Configuration
COMPOSE_PROJECT_NAME="my-axum-app-test"
TEST_TIMEOUT=300  # 5 minutes
API_BASE_URL="http://localhost:8080"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check requirements
check_requirements() {
    log_info "Checking requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    log_success "Docker found"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    log_success "Docker Compose found"
    
    # Check Python
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        log_error "Python is not installed"
        exit 1
    fi
    log_success "Python found"
    
    # Check required files
    required_files=("docker-compose.yml" "Dockerfile" "schemathesis_test.py")
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            log_error "Required file not found: $file"
            exit 1
        fi
    done
    log_success "All required files found"
}

# Setup Python environment for testing
setup_python_env() {
    log_info "Setting up Python testing environment..."
    
    # Create virtual environment if not exists
    if [ ! -d "venv" ]; then
        python3 -m venv venv 2>/dev/null || python -m venv venv
        log_success "Python virtual environment created"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install requirements
    if [ -f "requirements-schemathesis.txt" ]; then
        pip install -r requirements-schemathesis.txt > /dev/null 2>&1
    else
        pip install schemathesis requests hypothesis pytest > /dev/null 2>&1
    fi
    log_success "Python dependencies installed"
}

# Clean up previous containers
cleanup_containers() {
    log_info "Cleaning up previous containers..."
    
    docker-compose -p "$COMPOSE_PROJECT_NAME" down --volumes --remove-orphans 2>/dev/null || true
    
    # Remove dangling images
    docker image prune -f > /dev/null 2>&1 || true
    
    log_success "Cleanup completed"
}

# Build and start containers
start_containers() {
    log_info "Building and starting containers..."
    
    # Set project name
    export COMPOSE_PROJECT_NAME="$COMPOSE_PROJECT_NAME"
    
    # Build and start services
    if docker-compose build --no-cache; then
        log_success "Docker build completed"
    else
        log_error "Docker build failed"
        exit 1
    fi
    
    if docker-compose up -d; then
        log_success "Containers started"
    else
        log_error "Failed to start containers"
        exit 1
    fi
}

# Wait for API to be ready
wait_for_api() {
    log_info "Waiting for API to be ready..."
    
    local attempts=0
    local max_attempts=30
    
    while [ $attempts -lt $max_attempts ]; do
        if curl -s -f "$API_BASE_URL/health" > /dev/null 2>&1; then
            log_success "API is ready!"
            return 0
        fi
        
        attempts=$((attempts + 1))
        echo -n "."
        sleep 2
    done
    
    log_error "API failed to start within timeout"
    return 1
}

# Run Schemathesis tests
run_schemathesis_tests() {
    log_info "Running Schemathesis API tests..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Set environment variables
    export API_BASE_URL="$API_BASE_URL"
    export MAX_EXAMPLES=50
    
    # Run tests
    if python schemathesis_test.py; then
        log_success "Schemathesis tests passed!"
        return 0
    else
        log_error "Schemathesis tests failed!"
        return 1
    fi
}

# Run additional validation tests
run_validation_tests() {
    log_info "Running additional validation tests..."
    
    local test_passed=0
    local test_total=0
    
    # Test 1: Basic connectivity
    test_total=$((test_total + 1))
    if curl -s -f "$API_BASE_URL/" > /dev/null; then
        log_success "Root endpoint test passed"
        test_passed=$((test_passed + 1))
    else
        log_error "Root endpoint test failed"
    fi
    
    # Test 2: Health check
    test_total=$((test_total + 1))
    if curl -s -f "$API_BASE_URL/health" > /dev/null; then
        log_success "Health check test passed"
        test_passed=$((test_passed + 1))
    else
        log_error "Health check test failed"
    fi
    
    # Test 3: API endpoints
    test_total=$((test_total + 1))
    if curl -s -f "$API_BASE_URL/api/karyawans" > /dev/null; then
        log_success "Karyawans API test passed"
        test_passed=$((test_passed + 1))
    else
        log_error "Karyawans API test failed"
    fi
    
    test_total=$((test_total + 1))
    if curl -s -f "$API_BASE_URL/api/kantors" > /dev/null; then
        log_success "Kantors API test passed"
        test_passed=$((test_passed + 1))
    else
        log_error "Kantors API test failed"
    fi
    
    # Test 4: Error handling
    test_total=$((test_total + 1))
    response_code=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE_URL/api/karyawans/invalid")
    if [ "$response_code" = "400" ]; then
        log_success "Error handling test passed"
        test_passed=$((test_passed + 1))
    else
        log_error "Error handling test failed (expected 400, got $response_code)"
    fi
    
    log_info "Validation tests: $test_passed/$test_total passed"
    
    if [ $test_passed -eq $test_total ]; then
        return 0
    else
        return 1
    fi
}

# Show container logs
show_logs() {
    log_info "Container logs:"
    echo "===================="
    docker-compose -p "$COMPOSE_PROJECT_NAME" logs --tail=50
    echo "===================="
}

# Generate test report
generate_report() {
    local test_success=$1
    local report_file="docker_schemathesis_report.md"
    
    cat > "$report_file" << EOF
# Docker + Schemathesis Integration Test Report

**Generated**: $(date)
**Project**: Karyawan & Kantor Management API
**Status**: $([ $test_success -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")

## Test Configuration
- Docker Compose Project: $COMPOSE_PROJECT_NAME
- API Base URL: $API_BASE_URL
- Test Timeout: ${TEST_TIMEOUT}s
- Schemathesis Max Examples: 50

## Test Summary
1. ✅ Docker environment setup
2. ✅ Container build and deployment
3. $([ $test_success -eq 0 ] && echo "✅" || echo "❌") API readiness check
4. $([ $test_success -eq 0 ] && echo "✅" || echo "❌") Schemathesis property-based testing
5. $([ $test_success -eq 0 ] && echo "✅" || echo "❌") Manual validation tests

## Files Generated
- OpenAPI Schema: api_schema.json
- Container Logs: Available via docker-compose logs
- Test Report: $report_file

## Next Steps
$(if [ $test_success -eq 0 ]; then
    echo "- 🎉 All tests passed! API is ready for production"
    echo "- Consider running load tests with additional tools"
else
    echo "- 🔍 Review test failures in the logs above"
    echo "- Check container health: docker-compose ps"
    echo "- Review API logs: docker-compose logs app"
fi)

---
Generated by Docker + Schemathesis Integration Test Runner
EOF

    log_success "Test report saved to: $report_file"
}

# Cleanup function
cleanup() {
    log_info "Cleaning up..."
    docker-compose -p "$COMPOSE_PROJECT_NAME" down --volumes --remove-orphans 2>/dev/null || true
    
    # Deactivate virtual environment if active
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate 2>/dev/null || true
    fi
}

# Set trap for cleanup
trap cleanup EXIT

# Main execution
main() {
    log_info "Starting Docker + Schemathesis integration test..."
    
    # Check all requirements
    check_requirements
    
    # Setup Python environment
    setup_python_env
    
    # Clean up any previous containers
    cleanup_containers
    
    # Build and start containers
    start_containers
    
    # Wait for API to be ready
    if ! wait_for_api; then
        show_logs
        log_error "API failed to start - check logs above"
        exit 1
    fi
    
    # Run tests
    local test_success=0
    
    # Run Schemathesis tests
    if run_schemathesis_tests; then
        log_success "Schemathesis tests completed successfully"
    else
        log_error "Schemathesis tests failed"
        test_success=1
    fi
    
    # Run validation tests
    if run_validation_tests; then
        log_success "Validation tests completed successfully"
    else
        log_error "Validation tests failed"
        test_success=1
    fi
    
    # Generate report
    generate_report $test_success
    
    # Final result
    if [ $test_success -eq 0 ]; then
        log_success "🎉 All tests passed! Docker + API integration successful!"
        echo ""
        log_info "Your API is now running at: $API_BASE_URL"
        log_info "To stop containers: docker-compose down"
        exit 0
    else
        log_error "❌ Some tests failed"
        show_logs
        exit 1
    fi
}

# Run main function
main "$@"