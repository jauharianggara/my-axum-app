# Photo Upload API - Complete Testing Suite

This comprehensive testing framework validates all aspects of the photo upload functionality for the Karyawan (Employee) API.

## 🧪 Test Suite Overview

### 1. Functional Testing (`comprehensive_photo_tests.py`)
**Purpose**: Validates core API functionality and business logic
- ✅ Photo upload with karyawan creation
- ✅ Standalone photo upload to existing karyawan
- ✅ File format validation (JPEG, PNG, WebP)
- ✅ File size validation (5MB limit)
- ✅ Photo retrieval and serving
- ✅ Photo deletion and cleanup
- ✅ Error handling and edge cases
- ✅ API response validation

### 2. Performance Testing (`performance_photo_tests.py`)
**Purpose**: Evaluates API performance under load
- 🚀 Load testing (concurrent uploads)
- ⚡ Stress testing (sustained load)
- 📏 File size performance analysis
- 📊 Response time metrics
- 🎯 Throughput measurement
- 🧹 Automatic cleanup

### 3. Security Testing (`security_photo_tests.py`)
**Purpose**: Identifies security vulnerabilities
- 🛡️ File type validation bypass attempts
- 💉 SQL injection testing
- 📁 Path traversal attack prevention
- 🔒 Authentication/authorization checks
- ⏰ Rate limiting verification
- 🚨 Malicious file upload detection

### 4. Master Test Runner (`test_runner.py`)
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
```

### Run All Tests
```bash
# Run complete test suite (recommended)
python test_runner.py

# Run specific test suites
python test_runner.py --suites functional security

# Verbose output
python test_runner.py --verbose

# List available test suites
python test_runner.py --list
```

### Run Individual Test Suites
```bash
# Functional tests only
python comprehensive_photo_tests.py

# Performance tests only
python performance_photo_tests.py

# Security tests only
python security_photo_tests.py
```

## 📋 Test Execution Matrix

| Test Category | Tests | Duration | Automation Level |
|---------------|-------|----------|------------------|
| **Functional** | 20+ tests | 2-5 min | Fully Automated |
| **Performance** | Load/Stress | 5-10 min | Fully Automated |
| **Security** | 15+ tests | 3-7 min | Fully Automated |
| **Interactive** | Manual testing | Variable | HTML Form |

## 🔧 Configuration

### Server Settings
- **Base URL**: `http://localhost:8080`
- **API Endpoint**: `/api/karyawans`
- **Upload Endpoint**: `/api/karyawans/with-photo`
- **Static Files**: `/uploads/`

### Test Parameters
```python
# File size limits
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Supported formats
SUPPORTED_FORMATS = ['image/jpeg', 'image/png', 'image/webp']

# Performance test settings
LOAD_TEST_REQUESTS = 50
STRESS_TEST_DURATION = 60  # seconds
MAX_CONCURRENT_WORKERS = 20
```

## 📊 Understanding Test Results

### Success Indicators
- ✅ **All tests pass**: API is production-ready
- ✅ **Functional tests pass**: Core features work correctly
- ✅ **Security tests pass**: No critical vulnerabilities
- ✅ **Performance tests pass**: Handles expected load

### Warning Signs
- ⚠️ **Partial failures**: Review specific issues
- ⚠️ **Security warnings**: Address before production
- ⚠️ **Performance issues**: May need optimization

### Critical Issues
- ❌ **Functional failures**: Core features broken
- 🚨 **Security vulnerabilities**: Immediate attention required
- 💥 **System errors**: Infrastructure problems

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

## 🔐 Security Checklist

### Implemented Protections
- ✅ File type validation (MIME type + extension)
- ✅ File size limits
- ✅ Path traversal prevention
- ✅ SQL injection protection (parameterized queries)
- ✅ Unique file naming (UUID-based)
- ✅ Safe file storage location

### Additional Recommendations
- Implement authentication/authorization
- Add rate limiting
- Use HTTPS in production
- Regular security audits
- Input sanitization
- File content scanning

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