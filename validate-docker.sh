#!/bin/bash

# Docker Build Validation Script
# This script validates the Dockerfile without actually building

echo "=== Docker Build Validation ==="
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
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
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
echo "=== Validation Complete ==="