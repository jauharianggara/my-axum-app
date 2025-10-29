# 🧪 Test Suite Documentation

Organized testing framework for Karyawan API with clean structure and comprehensive coverage.

## 📁 Test Structure

```
tests/
├── api/                    # API functionality tests
│   ├── auth_test.py               # JWT authentication testing
│   ├── basic_api_test.py          # Basic endpoint testing
│   ├── karyawan_crud_test.py      # Karyawan CRUD operations
│   └── kantor_crud_test.py        # Kantor CRUD operations
├── photo/                  # Photo upload tests
│   ├── photo_upload_test.py       # Core photo functionality
│   ├── photo_validation_test.py   # Photo validation & security
│   ├── photo_performance_test.py  # Performance testing
│   └── photo_security_test.py     # Security testing
├── html/                   # Interactive tests
│   └── test_photo_form.html       # Web-based photo upload testing
├── scripts/                # Automation scripts
│   └── quick_test.ps1             # PowerShell quick test runner
└── utils/                  # Test utilities
    └── test_utils.py              # Common test utilities
```

## 🚀 Quick Start

### 1. Run All Tests (Recommended)
```bash
# Using Python master runner
python run_tests.py

# Using PowerShell script
tests\scripts\quick_test.ps1
```

### 2. Run Specific Test Suites
```bash
# API tests only
python run_tests.py --suite api

# Photo tests only  
python run_tests.py --suite photo

# Quick tests (essential only)
python run_tests.py --quick
```

### 3. Run Individual Test Files
```bash
# JWT Authentication testing
python tests\api\auth_test.py

# Basic API functionality
python tests\api\basic_api_test.py

# Photo upload functionality
python tests\photo\photo_upload_test.py

# Security testing
python tests\photo\photo_security_test.py
```

## 📋 Test Categories

### � Authentication & Security Tests

#### JWT Authentication Protection Test (`../test_protected_endpoints.py`)
- ✅ Public endpoints accessible without auth
- ✅ Protected endpoints require JWT token
- ✅ Valid token grants access to protected resources
- ✅ Invalid tokens properly rejected with 401
- ✅ Missing authorization header handling
- ✅ Endpoint security boundary testing

```bash
# Run comprehensive authentication protection test
python test_protected_endpoints.py
```

### �🔧 API Tests (`tests/api/`)

#### JWT Authentication Test (`auth_test.py`)
- ✅ User registration
- ✅ User login with JWT token generation
- ✅ Protected endpoint access with valid token
- ✅ Protected endpoint rejection without token
- ✅ Invalid token handling
- ✅ Token expiration validation
- ✅ User profile retrieval

#### Basic API Test (`basic_api_test.py`)
- ✅ Health endpoint
- ✅ Root endpoint
- ✅ Karyawan list
- ✅ Kantor list
- ✅ Get by ID
- ✅ Invalid ID handling
- ✅ Non-existent ID handling

#### Karyawan CRUD Test (`karyawan_crud_test.py`)
- ✅ Create karyawan
- ✅ Read karyawan
- ✅ Update karyawan
- ✅ Delete karyawan
- ✅ Invalid data validation
- ✅ Non-existent operations

#### Kantor CRUD Test (`kantor_crud_test.py`)
- ✅ Create kantor
- ✅ Read kantor
- ✅ Update kantor
- ✅ Delete kantor
- ✅ Coordinate validation
- ✅ Relationship testing

### 📷 Photo Tests (`tests/photo/`)

#### Photo Upload Test (`photo_upload_test.py`)
- ✅ Create karyawan with photo
- ✅ Photo file accessibility
- ✅ Upload to existing karyawan
- ✅ Delete photo
- ✅ Invalid file type rejection
- ✅ Multiple format support
- ✅ Performance testing

#### Photo Validation Test (`photo_validation_test.py`)
- ✅ File type validation
- ✅ File size validation
- ✅ Empty file validation
- ✅ Filename security
- ✅ MIME type spoofing
- ✅ Valid format acceptance

#### Photo Performance Test (`photo_performance_test.py`)
- ✅ Single upload performance
- ✅ Multiple uploads performance
- ✅ Concurrent uploads
- ✅ File size performance
- ✅ Upload throughput

#### Photo Security Test (`photo_security_test.py`)
- ✅ Malicious file prevention
- ✅ File size limits
- ✅ Path traversal prevention
- ✅ SQL injection prevention
- ✅ MIME validation
- ✅ Secure storage

## 🛠️ Test Utilities (`tests/utils/`)

### Common Functions
- `wait_for_server()` - Wait for server availability
- `check_server_health()` - Quick health check
- `get_valid_kantor_id()` - Get test kantor ID
- `create_test_image()` - Generate test images
- `cleanup_test_*()` - Resource cleanup
- `TestRunner` class - Base test runner

## 🌐 Interactive Testing (`tests/html/`)

### Web-based Testing
- **`test_photo_form.html`** - Interactive photo upload testing
- Direct browser testing interface
- Manual validation capabilities

## ⚡ Automation Scripts (`tests/scripts/`)

### PowerShell Quick Test (`quick_test.ps1`)
```powershell
# Run all tests
.\tests\scripts\quick_test.ps1

# Run specific suite
.\tests\scripts\quick_test.ps1 -Suite photo

# Quick tests only
.\tests\scripts\quick_test.ps1 -Quick

# Help
.\tests\scripts\quick_test.ps1 -Help
```

## 📊 Test Results

### Success Indicators
- ✅ **All tests pass**: API is production-ready with full authentication
- ✅ **Authentication tests pass**: JWT security properly implemented
- ✅ **API tests pass**: Core functionality working
- ✅ **Photo tests pass**: Photo upload working
- ✅ **Security tests pass**: No vulnerabilities

### Output Format
```
🧪 TEST SUITE NAME
=====================================
✅ Test Name 1
✅ Test Name 2
❌ Test Name 3
      Error details here

📊 TEST SUMMARY
=====================================
Passed: 8
Failed: 1
Total:  9
Success Rate: 88.9%
```

## � JWT Authentication Testing

### Authentication Test Workflow

#### 1. Complete Authentication Flow Test
```bash
# Test the full JWT authentication system
python tests\api\auth_test.py
```
**Tests:**
- User registration with validation
- Login with credential verification  
- JWT token generation and format
- Protected endpoint access with valid token
- Unauthorized access rejection

#### 2. Protected Endpoints Security Test
```bash
# Test endpoint protection implementation
python test_protected_endpoints.py
```
**Tests:**
- Public endpoints remain accessible
- Protected endpoints require authentication
- Valid JWT tokens grant access
- Invalid/missing tokens return 401 Unauthorized

#### 3. Manual Authentication Testing
```bash
# Login and get token
$body = '{"username_or_email":"testuser","password":"password123"}'
$response = Invoke-WebRequest -Uri http://localhost:8080/api/auth/login -Method POST -Body $body -ContentType "application/json"
$token = ($response.Content | ConvertFrom-Json).data.token

# Test protected endpoint
$headers = @{ "Authorization" = "Bearer $token" }
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans -Headers $headers
```

### Authentication Security Validation

#### Protected Endpoints:
- **`/api/karyawans/*`** - All karyawan operations
- **`/api/kantors/*`** - All kantor operations

#### Public Endpoints:
- **`/`** - Root endpoint
- **`/health`** - Health check
- **`/api/auth/*`** - Authentication operations
- **`/uploads/*`** - Static file serving

#### Expected Responses:
```bash
# Without token
GET /api/karyawans → 401 {"errors":["Missing authorization header"]}

# With valid token  
GET /api/karyawans → 200 {"data":[...karyawan records...]}

# With invalid token
GET /api/karyawans → 401 {"errors":["Invalid or expired token"]}
```

## �🔧 Configuration

### Server Settings
- **Base URL**: `http://localhost:8080`
- **Health Endpoint**: `/health`
- **API Base**: `/api`

### Test Dependencies
```bash
pip install requests pillow

# For JWT testing
# No additional dependencies needed - uses standard requests library
```

### Environment Setup
1. Start server: `cargo run`
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python run_tests.py`

## 🐛 Troubleshooting

### Common Issues

**Authentication failures:**
```bash
# Check if you're logged in
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8080/api/user/me

# Get new token
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username_or_email":"testuser","password":"password123"}'
```

**Server not running:**
```bash
# Check if server is running
curl http://localhost:8080/health

# Start server
cargo run
```

**Python dependencies missing:**
```bash
pip install requests pillow
```

**Permission errors:**
```bash
# Windows: Run PowerShell as Administrator
# Linux/Mac: Check file permissions
chmod +x tests/scripts/quick_test.ps1
```

### Debug Mode
```bash
# Verbose test output
python run_tests.py --verbose

# Individual test debugging
python tests/api/auth_test.py
python tests/api/basic_api_test.py

# Authentication-specific debugging
python test_protected_endpoints.py
```

## 📈 Performance Expectations

### Benchmark Results
- **Authentication**: < 2 seconds per login
- **JWT Token Validation**: < 100ms per request
- **Basic API**: < 1 second per test
- **CRUD Operations**: < 2 seconds per operation
- **Photo Upload**: < 5 seconds per upload
- **Concurrent Tests**: 80%+ success rate
- **Overall Suite**: < 90 seconds total

### Performance Thresholds
- Single upload: < 5 seconds
- Multiple uploads: < 30 seconds
- Concurrent uploads: 60%+ success
- Throughput: > 10 KB/s

## 🔐 Security Validation

### Security Checks
- ✅ JWT authentication implementation
- ✅ Protected endpoint access control
- ✅ Token validation and expiry
- ✅ Authorization header enforcement
- ✅ File type validation
- ✅ Size limit enforcement
- ✅ Path traversal prevention
- ✅ SQL injection protection
- ✅ MIME type validation
- ✅ Secure file storage

### Security Issues Reporting
Security tests will report:
- 🚨 **CRITICAL**: Immediate attention required
- ⚠️ **WARNING**: Should be addressed
- ✅ **PASS**: No issues detected

## 📝 Adding New Tests

### Creating New Test Files
```python
#!/usr/bin/env python3
"""
New Test Suite
Description of what this test suite covers
"""

import sys
sys.path.insert(0, '../utils')
from test_utils import TestRunner, print_test_header

class NewTestSuite(TestRunner):
    def __init__(self):
        super().__init__("NEW TEST SUITE")
    
    def test_something(self):
        """Test something specific"""
        # Test implementation
        return True

def run_tests():
    """Run all tests"""
    print_test_header("NEW TEST SUITE")
    
    tester = NewTestSuite()
    
    try:
        tester.test("Test something", tester.test_something)
        return tester.summary()
    finally:
        tester.cleanup()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
```

### Integration with Master Runner
Add new test files to `run_tests.py`:
```python
test_suites.append(('tests/new/new_test.py', 'New Test Description'))
```

## 🎯 Best Practices

### Test Writing Guidelines
1. **Always cleanup**: Use `created_ids` and cleanup methods
2. **Clear naming**: Descriptive test names
3. **Error handling**: Try/catch in test methods
4. **Assertions**: Clear pass/fail conditions
5. **Documentation**: Comment test purposes

### Test Execution Guidelines
1. **Start server first**: Ensure server is running
2. **Check dependencies**: Verify Python packages
3. **Run systematically**: Use organized test runners
4. **Review results**: Check all test outputs
5. **Address failures**: Fix issues before deployment

---

## 🏆 Summary

This organized test suite provides:
- **JWT Authentication** with comprehensive security testing
- **Protected endpoint validation** ensuring proper access control
- **Clean structure** with logical organization
- **Comprehensive coverage** of all functionality including authentication
- **Easy execution** with multiple entry points
- **Clear reporting** with detailed results
- **Security validation** with vulnerability and authentication testing
- **Performance measurement** with benchmarks
- **Maintainable code** with reusable utilities

**Your API testing is now professional-grade with enterprise-level security!** 🛡️🚀✨