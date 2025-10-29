# Schemathesis API Testing Guide

Panduan lengkap untuk menjalankan property-based testing menggunakan Schemathesis pada Karyawan & Kantor Management API.

## 📋 Overview

Schemathesis adalah tool untuk property-based testing yang menggunakan OpenAPI schema untuk generate test cases secara otomatis. Tool ini akan:

- Generate test data secara random berdasarkan API schema
- Test semua endpoints dengan berbagai kombinasi input
- Validate response format dan status codes
- Detect edge cases dan potential bugs
- Provide comprehensive coverage testing

## 🛠️ Setup Requirements

### Prerequisites
- **Python 3.7+** dengan pip
- **Docker & Docker Compose** (untuk integration testing)
- **Running API instance** (local atau containerized)

### Installation

1. **Clone repository dan masuk ke directory:**
   ```bash
   cd my-axum-app
   ```

2. **Install Python dependencies:**
   ```bash
   # Menggunakan requirements file
   pip install -r requirements-schemathesis.txt
   
   # Atau install manual
   pip install schemathesis requests hypothesis pytest
   ```

3. **Atau gunakan virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # atau
   .\venv\Scripts\activate   # Windows
   
   pip install -r requirements-schemathesis.txt
   ```

## 🚀 Running Tests

### Option 1: Standalone Schemathesis Testing

1. **Start API server:**
   ```bash
   # Local development
   cargo run
   
   # Atau dengan Docker
   docker-compose up -d
   ```

2. **Run Schemathesis tests:**
   ```bash
   # PowerShell (Windows)
   .\run_schemathesis_tests.ps1
   
   # Python script (Cross-platform)
   python schemathesis_test.py
   ```

### Option 2: Docker Integration Testing (Recommended)

```bash
# Linux/Mac
chmod +x docker_with_schemathesis.sh
./docker_with_schemathesis.sh

# Windows PowerShell
.\docker_with_schemathesis.ps1
```

## 📊 Test Configuration

### Environment Variables
```bash
export API_BASE_URL="http://localhost:8080"  # API base URL
export MAX_EXAMPLES=50                       # Max test examples per endpoint
```

### PowerShell Parameters
```powershell
# Run with custom configuration
.\run_schemathesis_tests.ps1 -BaseUrl "http://localhost:8080" -MaxExamples 100

# Skip dependency installation
.\run_schemathesis_tests.ps1 -SkipInstall

# Enable verbose output
.\run_schemathesis_tests.ps1 -Verbose
```

### Docker Integration Parameters
```powershell
# Custom project name
.\docker_with_schemathesis.ps1 -ProjectName "my-test-project"

# Custom API URL (if using different port)
.\docker_with_schemathesis.ps1 -ApiBaseUrl "http://localhost:8081"

# Show container logs
.\docker_with_schemathesis.ps1 -ShowLogs

# Skip cleanup after testing
.\docker_with_schemathesis.ps1 -SkipCleanup
```

## 🧪 Test Coverage

### Endpoints Tested

#### Health & Root Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check

#### Karyawan Management
- `GET /api/karyawans` - List all karyawans
- `GET /api/karyawans/with-kantor` - List karyawans with kantor info
- `GET /api/karyawans/:id` - Get karyawan by ID
- `GET /api/karyawans/:id/with-kantor` - Get karyawan with kantor by ID
- `POST /api/karyawans` - Create new karyawan
- `PUT /api/karyawans/:id` - Update karyawan
- `DELETE /api/karyawans/:id` - Delete karyawan

#### Kantor Management
- `GET /api/kantors` - List all kantors
- `GET /api/kantors/:id` - Get kantor by ID
- `POST /api/kantors` - Create new kantor
- `PUT /api/kantors/:id` - Update kantor
- `DELETE /api/kantors/:id` - Delete kantor

### Test Types

#### Property-Based Testing
- **Valid Input Generation**: Generate valid test data based on schema constraints
- **Edge Case Testing**: Test boundary values and edge cases
- **Random Data Testing**: Test with completely random (but valid) data
- **Invalid Input Testing**: Test with invalid data to verify error handling

#### Manual Validation Tests
- **Connectivity Tests**: Basic API connectivity and response
- **Response Format Tests**: JSON structure and required fields validation
- **Error Handling Tests**: Proper HTTP status codes for invalid requests
- **Relationship Tests**: Foreign key constraints and data integrity

## 📁 Generated Files

### Test Results
- `api_schema.json` - Generated OpenAPI schema
- `schemathesis_report.md` - PowerShell test report
- `docker_schemathesis_report.md` - Docker integration test report

### Virtual Environment
- `venv/` - Python virtual environment (auto-created)

## 🔧 Customization

### Modifying Test Data

Edit `schemathesis_test.py` untuk customize test data generation:

```python
@schemathesis.hook
def before_generate_body(context, strategy):
    """Custom hook untuk generate valid test data"""
    if context.operation.path == "/api/karyawans":
        # Custom logic untuk karyawan data
        return strategy.filter(lambda x: x.get('kantor_id') == "1")
    return strategy
```

### Adding Custom Validations

```python
def test_custom_validation(case):
    response = case.call()
    
    # Custom assertion
    if response.status_code == 200:
        data = response.json()
        assert data.get("success") is True
        assert "data" in data
```

### Modifying Schema

Edit the `generate_openapi_schema()` function dalam `schemathesis_test.py` untuk modify schema definitions.

## 🐛 Troubleshooting

### Common Issues

#### 1. Python Not Found
```bash
# Install Python dan add to PATH
# Windows: Download dari https://python.org
# Linux: sudo apt install python3 python3-pip
# Mac: brew install python3
```

#### 2. API Not Available
```bash
# Check if API is running
curl http://localhost:8080/health

# Start API if needed
cargo run
# atau
docker-compose up -d
```

#### 3. Port Already in Use
```bash
# Check what's using port 8080
netstat -ano | findstr :8080  # Windows
lsof -i :8080                 # Linux/Mac

# Use different port
API_BASE_URL="http://localhost:8081" python schemathesis_test.py
```

#### 4. Permission Issues (Linux/Mac)
```bash
# Make scripts executable
chmod +x docker_with_schemathesis.sh
chmod +x validate-docker.sh
```

#### 5. Virtual Environment Issues
```bash
# Remove and recreate venv
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements-schemathesis.txt
```

### Debug Mode

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Considerations

### Test Duration
- Default: 50 examples per endpoint (~5-10 minutes total)
- Fast testing: 10 examples per endpoint (~1-2 minutes)
- Comprehensive: 200+ examples per endpoint (~20-30 minutes)

### Memory Usage
- Virtual environment: ~100MB
- Test execution: ~50-100MB
- Docker containers: ~200-500MB

### Optimization Tips
1. **Use smaller MAX_EXAMPLES** untuk testing cepat
2. **Run specific endpoints** dengan filtered schema
3. **Use parallel testing** untuk multiple environments
4. **Cache dependencies** dalam CI/CD pipelines

## 🔗 Integration with CI/CD

### GitHub Actions Example
```yaml
name: Schemathesis API Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements-schemathesis.txt
      - name: Start API with Docker
        run: docker-compose up -d
      - name: Wait for API
        run: sleep 30
      - name: Run Schemathesis tests
        run: python schemathesis_test.py
      - name: Upload test artifacts
        uses: actions/upload-artifact@v2
        with:
          name: test-reports
          path: |
            api_schema.json
            schemathesis_report.md
```

## 📚 Additional Resources

- [Schemathesis Documentation](https://schemathesis.readthedocs.io/)
- [Hypothesis Property-Based Testing](https://hypothesis.readthedocs.io/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 🤝 Contributing

Untuk contribute ke Schemathesis testing setup:

1. Fork repository
2. Tambah test cases atau improve existing tests
3. Update dokumentasi jika needed
4. Submit pull request dengan test results

---

**Last Updated**: October 29, 2025  
**Version**: 1.0.0