#!/bin/bash

# Docker Build Validation Script with Schemathesis Integration
# This script validates the Dockerfile and runs Schemathesis API testing

echo "=== Docker Build Validation with Schemathesis Testing ==="
echo ""

# Check if Dockerfile exists
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile not found!"
    exit 1
fi

echo "✅ Dockerfile found"

# Check if required files exist
echo ""
echo "=== Checking required files ==="

required_files=(
    "Cargo.toml"
    "Cargo.lock"
    "migration/Cargo.toml"
    "src/main.rs"
    "migration/src/lib.rs"
    "schemathesis_test.py"
    "docker_with_schemathesis.sh"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        if [ "$file" = "schemathesis_test.py" ]; then
            echo "   ℹ️  Schemathesis testing will be skipped"
        fi
    fi
done

echo ""
echo "=== Dockerfile Syntax Check ==="

# Basic syntax validation
if grep -q "FROM.*as builder" Dockerfile; then
    echo "✅ Multi-stage build detected"
else
    echo "❌ Multi-stage build not found"
fi

if grep -q "WORKDIR" Dockerfile; then
    echo "✅ WORKDIR set"
else
    echo "❌ WORKDIR not set"
fi

if grep -q "USER appuser" Dockerfile; then
    echo "✅ Non-root user configured"
else
    echo "❌ Running as root (security risk)"
fi

if grep -q "EXPOSE" Dockerfile; then
    echo "✅ Port exposed"
else
    echo "❌ No port exposed"
fi

if grep -q "HEALTHCHECK" Dockerfile; then
    echo "✅ Health check configured"
else
    echo "⚠️  No health check (recommended)"
fi

echo ""
echo "=== Docker Compose Check ==="

if [ -f "docker-compose.yml" ]; then
    echo "✅ docker-compose.yml exists"
    
    if grep -q "depends_on" docker-compose.yml; then
        echo "✅ Service dependencies configured"
    fi
    
    if grep -q "healthcheck" docker-compose.yml; then
        echo "✅ Health checks in compose"
    fi
    
    if grep -q "volumes" docker-compose.yml; then
        echo "✅ Data persistence configured"
    fi
else
    echo "❌ docker-compose.yml not found"
fi

echo ""
echo "=== Security Checks ==="

if grep -q "USER.*root" Dockerfile; then
    echo "❌ Running as root user (security risk)"
elif grep -q "USER" Dockerfile; then
    echo "✅ Non-root user configured"
fi

if grep -q "apt-get.*clean\|rm.*apt" Dockerfile; then
    echo "✅ Package cache cleaned"
else
    echo "⚠️  Package cache not cleaned (larger image)"
fi

echo ""
echo "=== Build Optimization Checks ==="

if grep -q "\.dockerignore" . 2>/dev/null; then
    echo "✅ .dockerignore found"
else
    echo "⚠️  .dockerignore not found (larger build context)"
fi

if grep -q "strip.*target" Dockerfile; then
    echo "✅ Binary stripping enabled"
else
    echo "⚠️  Binary not stripped (larger image)"
fi

if grep -q "cargo build.*release.*cargo build" Dockerfile; then
    echo "✅ Dependency caching configured"
else
    echo "⚠️  No dependency caching (slower builds)"
fi

echo ""
echo "=== Schemathesis Testing Check ==="

# Check if Python is available for Schemathesis
if command -v python3 &> /dev/null || command -v python &> /dev/null; then
    echo "✅ Python found for Schemathesis testing"
    
    # Check if Schemathesis test files exist
    if [ -f "schemathesis_test.py" ]; then
        echo "✅ Schemathesis test script found"
        
        # Check if virtual environment can be created
        if python3 -m venv test_env_check 2>/dev/null || python -m venv test_env_check 2>/dev/null; then
            rm -rf test_env_check 2>/dev/null
            echo "✅ Python virtual environment support available"
        else
            echo "⚠️  Python virtual environment support not available"
        fi
        
        # Check if requirements file exists
        if [ -f "requirements-schemathesis.txt" ]; then
            echo "✅ Schemathesis requirements file found"
        else
            echo "⚠️  Schemathesis requirements file not found (will use basic install)"
        fi
        
        echo "ℹ️  Schemathesis testing is ready!"
        echo "   To run full Docker + Schemathesis test:"
        echo "   ./docker_with_schemathesis.sh"
        
    else
        echo "⚠️  Schemathesis test script not found"
        echo "   Testing will be limited to basic Docker validation"
    fi
else
    echo "⚠️  Python not found - Schemathesis testing not available"
    echo "   Install Python to enable comprehensive API testing"
fi

echo ""
echo "=== Validation Complete ==="

# Offer to run full integration test
if [ -f "schemathesis_test.py" ] && [ -f "docker_with_schemathesis.sh" ]; then
    echo ""
    echo "🚀 Ready for full Docker + Schemathesis integration test!"
    echo ""
    echo "To run the complete test suite:"
    echo "  chmod +x docker_with_schemathesis.sh"
    echo "  ./docker_with_schemathesis.sh"
    echo ""
    echo "Or use PowerShell on Windows:"
    echo "  .\\docker_with_schemathesis.ps1"
fi