# Comprehensive API Testing Guide

This complete testing framework validates all aspects of the Karyawan (Employee) API including security, functionality, and performance.

## 🧪 Test Suite Overview

### 1. Security Testing (`security_tests.py`) 🛡️
**Purpose**: Validates all security implementations
- ✅ Rate limiting protection
- ✅ CORS policy enforcement
- ✅ SQL injection prevention
- ✅ NoSQL injection prevention  
- ✅ CSRF protection validation
- ✅ XSS protection testing
- ✅ Security headers verification
- ✅ Input sanitization testing
- ✅ Authentication bypass attempts

### 2. Functional Testing (`comprehensive_photo_tests.py`) 📷
**Purpose**: Validates core API functionality and business logic
- ✅ Photo upload with karyawan creation
- ✅ Standalone photo upload to existing karyawan
- ✅ File format validation (JPEG, PNG, WebP)
- ✅ File size validation (5MB limit)
- ✅ Photo retrieval and serving
- ✅ Photo deletion and cleanup
- ✅ Error handling and edge cases
- ✅ API response validation

### 3. Authentication & Authorization Testing (`auth_tests.py`) 🔐
**Purpose**: Validates authentication and authorization mechanisms
- ✅ User registration with security validation
- ✅ Login functionality
- ✅ JWT token validation
- ✅ Protected endpoint access
- ✅ Role-based access control
- ✅ Session management
- ✅ Password security

### 4. Performance Testing (`performance_photo_tests.py`) ⚡
**Purpose**: Evaluates API performance under load
- 🚀 Load testing (concurrent uploads)
- ⚡ Stress testing (sustained load)
- 📏 File size performance analysis
- 📊 Response time metrics
- 🎯 Throughput measurement
- 🧹 Automatic cleanup

### 5. Master Test Runner (`test_runner.py`) 🎯
**Purpose**: Orchestrates all test suites
- 🎯 Automated test execution
- 🔍 Dependency checking
- 🚀 Server management
- 📊 Comprehensive reporting
- 🧹 Resource cleanup

## 🚀 Quick Start

### Prerequisites
```bash
# Install Python dependencies
pip install requests pillow

# Ensure Rust server is buildable
cargo check

# Ensure database is running
docker-compose up -d
```

### Run All Tests (Recommended)
```bash
# Run complete test suite with auto-server start
python tests/master_test_runner.py --start-server

# Run all tests (manual server start)
cargo run &  # Start server in background
python tests/master_test_runner.py

# Run specific test suites
python tests/master_test_runner.py --suites security auth

# Verbose output for debugging
python tests/master_test_runner.py --verbose

# List available test suites
python tests/master_test_runner.py --list
```

### Run Individual Test Suites
```bash
# Security tests (RECOMMENDED FIRST)
python tests/security_tests.py

# Authentication tests
python tests/auth_tests.py

# Functional tests (photo uploads, etc.)
python tests/comprehensive_photo_tests.py

# Performance tests
python tests/performance_photo_tests.py
```

### PowerShell Testing (Windows)
```powershell
# Quick security validation
$response = Invoke-WebRequest -Uri "http://localhost:8080/health"
$response.Headers  # Check security headers

# Test CSRF protection
Invoke-WebRequest -Uri "http://localhost:8080/api/auth/register" -Method POST -ContentType "application/json" -Body '{"username": "test"}'

# Test with valid origin
Invoke-WebRequest -Uri "http://localhost:8080/api/auth/register" -Method POST -ContentType "application/json" -Headers @{"Origin"="http://localhost:3000"} -Body '{"username": "validtest", "email": "test@test.com", "password": "TestPass123"}'
```

## 📋 Test Execution Matrix

| Test Category | Tests | Duration | Automation Level | Priority |
|---------------|-------|----------|------------------|----------|
| **Security** | 25+ tests | 3-5 min | Fully Automated | 🔴 Critical |
| **Authentication** | 15+ tests | 2-3 min | Fully Automated | 🟠 High |
| **Functional** | 20+ tests | 2-5 min | Fully Automated | 🟡 Medium |
| **Performance** | Load/Stress | 5-10 min | Fully Automated | 🟢 Low |
| **Interactive** | Manual testing | Variable | HTML Form | 🔵 Optional |

### Security Test Coverage
- ✅ Rate limiting protection
- ✅ CORS policy enforcement  
- ✅ SQL injection prevention
- ✅ NoSQL injection prevention
- ✅ CSRF protection validation
- ✅ XSS protection testing
- ✅ Security headers verification
- ✅ Input sanitization testing
- ✅ Authentication bypass attempts

### Authentication Test Coverage
- ✅ User registration with validation
- ✅ Login with username/email
- ✅ JWT token validation
- ✅ Protected endpoint access
- ✅ Invalid credential handling
- ✅ Session management
- ✅ Authorization checks

## 🔧 Configuration

### Server Settings
- **Base URL**: `http://localhost:8080`
- **API Endpoints**: 
  - Authentication: `/api/auth/register`, `/api/auth/login`
  - Protected: `/api/karyawans`, `/api/kantors`, `/api/jabatans`
  - User: `/api/user/profile`
  - Static Files: `/uploads/`

### Security Test Parameters
```python
# Security testing configuration
CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'http://localhost:5173']
RATE_LIMIT_REQUESTS = 100  # per minute
MAX_REQUEST_SIZE = 5 * 1024 * 1024  # 5MB

# SQL/NoSQL injection patterns tested
SQL_INJECTION_PATTERNS = [
    "'; DROP TABLE users; --",
    "' OR 1=1 --", 
    "UNION SELECT password FROM users"
]

NOSQL_INJECTION_PATTERNS = [
    "$where: function() { return true; }",
    "{\"$gt\": \"\"}",
    "this.password != null"
]
```

### Authentication Test Parameters
```python
# Authentication testing configuration
TEST_USER_PREFIX = "testuser_"
TEST_EMAIL_DOMAIN = "@test.com"
DEFAULT_PASSWORD = "SecurePass123"
JWT_TOKEN_VALIDATION = True
```

## 📊 Understanding Test Results

### Success Indicators
- ✅ **All tests pass**: API is production-ready
- ✅ **Security tests pass**: No critical vulnerabilities detected
- ✅ **Authentication tests pass**: User management works correctly
- ✅ **Functional tests pass**: Core features work correctly
- ✅ **Performance tests pass**: Handles expected load

### Security Assessment Levels
- 🟢 **EXCELLENT**: All security tests passed (0 failures)
- 🟡 **GOOD**: Minor security issues detected (1-2 failures)  
- 🟠 **WARNING**: Several security issues need attention (3-5 failures)
- 🔴 **CRITICAL**: Major security vulnerabilities detected (6+ failures)

### Authentication Assessment Levels
- 🟢 **EXCELLENT**: All authentication tests passed
- 🟡 **GOOD**: Minor authentication issues detected
- 🟠 **WARNING**: Authentication issues need attention
- 🔴 **CRITICAL**: Major authentication vulnerabilities detected

### Critical Security Failures
- ❌ **CSRF Protection Disabled**: Immediate security risk
- ❌ **SQL Injection Possible**: Database compromise risk
- ❌ **XSS Vulnerabilities**: Client-side attack risk
- ❌ **Missing Security Headers**: Browser protection disabled
- ❌ **Authentication Bypass**: Unauthorized access possible

### Warning Signs
- ⚠️ **Partial failures**: Review specific issues
- ⚠️ **Security warnings**: Address before production
- ⚠️ **Performance issues**: May need optimization
- ⚠️ **Authentication edge cases**: Review security implications

## 🧹 Cleanup and Maintenance

### Automatic Cleanup
All test suites include automatic cleanup:
- Test karyawans are deleted after creation
- Uploaded photos are removed
- Database remains clean

### Manual Cleanup (if needed)
```bash
# Check for test records
curl http://localhost:8080/api/karyawans | grep -i "test\|demo\|security"

# Clean uploads directory
rm -rf uploads/test_*
rm -rf uploads/demo_*
```

## 🔍 Troubleshooting

### Common Issues

**Server not starting:**
```bash
# Check if port is in use
netstat -an | grep :8080

# Build server first
cargo build

# Run server manually
cargo run
```

**Dependencies missing:**
```bash
# Install Python packages
pip install requests pillow

# On Windows, might need:
pip install --upgrade certifi
```

**Database connection issues:**
```bash
# Check database status
# Ensure PostgreSQL is running
# Verify connection settings in .env
```

**Permission errors:**
```bash
# Ensure uploads directory is writable
chmod 755 uploads/

# On Windows, check folder permissions
```

### Debug Mode
```bash
# Run tests with verbose output
python test_runner.py --verbose

# Run server with debug logs
RUST_LOG=debug cargo run

# Check individual test script
python comprehensive_photo_tests.py
```

## 📈 Performance Benchmarks

### Expected Performance
- **Single upload**: < 1 second
- **Concurrent uploads**: 10+ requests/second
- **File processing**: < 500ms per image
- **Database operations**: < 100ms per query

### Scaling Considerations
- File storage: Consider cloud storage for production
- Database: Index optimization for large datasets
- Caching: Implement image caching for frequently accessed photos
- Load balancing: Multiple server instances for high traffic

## 🔐 Security Testing Checklist

### Pre-Production Security Validation
Run this checklist before deploying to production:

```bash
# 1. Run comprehensive security tests
python tests/security_tests.py

# 2. Verify all security headers are present
curl -I http://localhost:8080/health | grep -E "(X-|Content-Security|Referrer)"

# 3. Test CSRF protection
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"Test123"}'
# Should return 403 Forbidden

# 4. Test with valid origin
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3000" \
  -d '{"username":"validtest","email":"valid@test.com","password":"Test123"}'
# Should return 200 OK

# 5. Test SQL injection prevention
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3000" \
  -d '{"username":"admin'\'''; DROP TABLE users; --","email":"hack@test.com","password":"Test123"}'
# Should return 400 Bad Request with security error

# 6. Test authentication bypass
curl http://localhost:8080/api/jabatans
# Should return 401 Unauthorized

# 7. Test with valid authentication
# First login and get token, then:
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8080/api/jabatans
# Should return 200 OK with data
```

### Security Headers Validation
Expected headers on all responses:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- `Content-Security-Policy: default-src 'self'...`

### CORS Validation
- ✅ `localhost:3000` should be allowed
- ✅ `localhost:5173` should be allowed  
- ❌ `malicious-site.com` should be blocked
- ✅ Credentials should be supported
- ✅ Preflight requests should work

## 📝 Test Reports

### Generating Reports
Tests automatically generate console output with:
- Pass/fail status for each test
- Performance metrics
- Security assessment
- Overall health score

### CI/CD Integration
```yaml
# Example GitHub Actions workflow
- name: Run API Tests
  run: python test_runner.py --suites functional security
  
- name: Performance Baseline
  run: python performance_photo_tests.py
```

## 🆘 Support

### Getting Help
1. **Check test output**: Look for specific error messages
2. **Review logs**: Server logs provide detailed error information
3. **Verify setup**: Ensure database and server are properly configured
4. **Test isolation**: Run individual test suites to isolate issues

### Extending Tests
```python
# Add new test case to comprehensive_photo_tests.py
def test_new_feature(self):
    """Test description"""
    # Test implementation
    response = self.upload_photo_with_karyawan(...)
    self.assertTrue(response['success'])
```

## 🎯 Next Steps

After successful testing:
1. **Deploy to staging**: Run tests against staging environment
2. **Performance tuning**: Optimize based on test results
3. **Monitoring setup**: Implement production monitoring
4. **Documentation**: Update API documentation
5. **User acceptance**: Conduct user testing with real scenarios

---

**Happy Testing!** 🧪✨