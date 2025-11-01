# 📚 API Documentation Guide

Panduan lengkap untuk menggunakan dokumentasi API Karyawan & Kantor Management dengan comprehensive security features.

## 📖 Format Dokumentasi

### 1. OpenAPI/Swagger Documentation
File: `docs/openapi.yaml`

**Format**: OpenAPI 3.0.3 specification yang lengkap dengan:
- ✅ Semua endpoint yang tersedia
- ✅ Request/response schema yang detail
- ✅ Authentication flow dengan JWT
- ✅ Error handling dan status codes
- ✅ Photo upload specifications
- ✅ Validation rules dan constraints
- ✅ Interactive examples
- ✅ **Security features documentation**
- ✅ **Rate limiting specifications**
- ✅ **Security headers documentation**

**Fitur Utama**:
- **Comprehensive**: Mencakup semua endpoint dari health check hingga file upload
- **Interactive**: Dapat digunakan untuk testing langsung (jika ada Swagger UI)
- **Detailed**: Schema lengkap dengan validation rules dan security features
- **Standard Compliant**: Mengikuti OpenAPI 3.0.3 standards
- **Security Focused**: Comprehensive security feature documentation

### 2. Postman Collection
File: `docs/postman_collection.json`

**Features**:
- 🚀 **Ready-to-use**: Import dan langsung bisa digunakan
- 🔧 **Automated Scripts**: Test scripts dan environment variable automation
- 🧪 **Testing Suites**: Complete workflow testing dan security validation
- 📋 **Examples**: Real request/response examples
- 🔐 **Authentication Flow**: Automated JWT token management
- 🛡️ **Security Testing**: Comprehensive security test cases
- ⚡ **Rate Limiting Tests**: Rate limiting validation
- 🔒 **Injection Testing**: SQL/NoSQL/XSS protection validation

## 🚀 Setup Postman

### Step 1: Import Collection
1. Buka Postman
2. Click **"Import"** di kiri atas
3. Pilih **"Upload Files"**
4. Select file `docs/postman_collection.json`
5. Click **"Import"**

### Step 2: Import Environment (Optional)
1. Click **"Import"** lagi
2. Select file `docs/postman_environment.json`
3. Click **"Import"**
4. Pilih environment **"Karyawan & Kantor API - Development"**

### Step 3: Setup Environment Variables
Set base URL untuk development:
```
baseUrl = http://localhost:8080
```

### Step 4: Pastikan Server Running
```bash
# Via Docker Compose
docker-compose up

# Atau via Cargo
cargo run
```

## 🧪 Testing Workflow

### 1. Quick Test
Jalankan folder **"🔍 Health & Status"**:
- Root endpoint test
- Health check validation

### 2. Authentication Flow
Jalankan folder **"🔐 Authentication"**:
1. **Register User** - Membuat user baru
2. **Login User** - Mendapatkan JWT token (auto-saved)
3. **Get Current User Profile** - Verifikasi token

### 3. Complete CRUD Testing
Jalankan folder **"🧪 Test Scenarios > Complete Workflow Test"**:
- Automated end-to-end testing
- Unique test data generation
- Environment variable automation

### 4. Security Validation
Jalankan folder **"🧪 Test Scenarios > Security Tests"**:
- Test unauthorized access
- Invalid token validation
- Authentication bypass attempts

### 5. Advanced Security Testing
Jalankan folder **"🧪 Test Scenarios > Advanced Security Tests"**:
- **Rate Limiting**: Test 60 requests/minute limit
- **Security Headers**: Validate all security headers
- **CSRF Protection**: Test origin header validation
- **SQL Injection**: Test malicious SQL payload blocking
- **XSS Protection**: Test script injection sanitization

## 🛡️ Security Features Testing

### Rate Limiting Testing
Test rate limiting dengan menjalankan request berulang kali:
1. Jalankan "Test Rate Limiting" request
2. Jalankan berulang kali dengan cepat (>60 requests/minute)
3. Seharusnya mendapatkan 429 Too Many Requests

### Security Headers Validation
Test security headers dengan "Test Security Headers":
- Verifikasi X-Content-Type-Options: nosniff
- Verifikasi X-Frame-Options: DENY
- Verifikasi X-XSS-Protection: 1; mode=block
- Verifikasi Content-Security-Policy presence

### Injection Protection Testing
Test berbagai injection attacks:
- **SQL Injection**: `'; DROP TABLE users; --`
- **XSS**: `<script>alert('XSS')</script>`
- **NoSQL Injection**: `{"$ne": "admin"}`

### CSRF Protection Testing
Test CSRF protection dengan:
- Request tanpa Origin header (should be blocked)
- Request dengan invalid Origin (should be blocked)

## 🔐 Authentication Guide

### JWT Token Flow
1. **Register** atau **Login** untuk mendapatkan token
2. Token otomatis tersimpan di environment variable `jwtToken`
3. Semua protected endpoints menggunakan Bearer Authentication
4. Token berlaku 24 jam

### Manual Token Setup
Jika perlu set token manual:
1. Copy token dari login response
2. Set environment variable `jwtToken`
3. Atau set di Authorization tab: Bearer Token

## 📊 Endpoint Categories

### Health & Status
- `GET /` - Hello world
- `GET /health` - Health check

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/user/me` - Current user profile

### Jabatan Management (Protected)
- `GET /api/jabatans` - List all job positions
- `POST /api/jabatans` - Create job position
- `GET /api/jabatans/{id}` - Get job position by ID
- `PUT /api/jabatans/{id}` - Update job position
- `DELETE /api/jabatans/{id}` - Delete job position

### Kantor Management (Protected)
- `GET /api/kantors` - List all offices
- `POST /api/kantors` - Create office
- `GET /api/kantors/{id}` - Get office by ID
- `PUT /api/kantors/{id}` - Update office
- `DELETE /api/kantors/{id}` - Delete office

### Karyawan Management (Protected)
- `GET /api/karyawans` - List all employees
- `POST /api/karyawans` - Create employee
- `POST /api/karyawans/with-photo` - Create employee with photo
- `GET /api/karyawans/with-kantor` - List employees with office info
- `GET /api/karyawans/{id}` - Get employee by ID
- `GET /api/karyawans/{id}/with-kantor` - Get employee with office info
- `PUT /api/karyawans/{id}` - Update employee
- `DELETE /api/karyawans/{id}` - Delete employee
- `POST /api/karyawans/{id}/photo` - Upload employee photo
- `DELETE /api/karyawans/{id}/photo` - Delete employee photo

### File Access
- `GET /uploads/karyawan/photos/{filename}` - Get employee photo

### Security Information
- `GET /.well-known/security.txt` - Security policy information (if configured)

## 🛡️ Security Features Overview

### Implemented Security Protections

#### 1. Rate Limiting
- **Limit**: 60 requests per minute per IP address
- **Response**: 429 Too Many Requests when exceeded
- **Applied to**: All endpoints

#### 2. CORS Protection
- **Development**: Allows localhost:3000
- **Production**: Configurable allowed origins
- **CSRF Protection**: Origin header validation for state-changing requests

#### 3. Injection Prevention
- **SQL Injection**: 
  - Parameterized queries with SeaORM
  - Pattern detection and blocking
  - Blocks: SQL keywords, UNION, SELECT, DROP, ALTER
- **NoSQL Injection**:
  - MongoDB operator filtering
  - Blocks: $ne, $gt, $lt, $in, $nin, $where, $expr, etc.

#### 4. XSS Protection
- **HTML Sanitization**: Ammonia library removes malicious content
- **Security Headers**: X-XSS-Protection, Content-Security-Policy
- **Input Sanitization**: Automatic on all text inputs

#### 5. Security Headers
- **X-Content-Type-Options**: nosniff (prevents MIME sniffing)
- **X-Frame-Options**: DENY (prevents clickjacking)
- **X-XSS-Protection**: 1; mode=block (XSS protection)
- **Content-Security-Policy**: Comprehensive CSP rules

#### 6. Input Validation
- **Email Validation**: RFC compliant email format checking
- **String Constraints**: Length limits, character validation
- **File Validation**: Type checking, size limits, security scanning
- **Path Validation**: Prevents directory traversal attacks

## 🛠️ Advanced Usage

### Environment Variables
Collection menggunakan variables untuk automation:
- `baseUrl` - API base URL
- `jwtToken` - Authentication token
- `kantorId` - Office ID for testing
- `karyawanId` - Employee ID for testing
- `testUsername`, `testEmail` - Generated test credentials

### Automated Testing
Collection includes automated test scripts:
```javascript
// Example: Check successful response
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Example: Save token for subsequent requests
if (pm.response.code === 200) {
    const jsonData = pm.response.json();
    pm.environment.set('jwtToken', jsonData.data.token);
}
```

### Photo Upload Testing
Untuk test photo upload:
1. Buka request **"Create Karyawan with Photo"** atau **"Upload Karyawan Photo"**
2. Di Body > form-data, click pada field `foto`
3. Pilih file gambar (JPEG/PNG/GIF, max 5MB)
4. Send request

## 🔧 Troubleshooting

### Common Issues

**1. 401 Unauthorized**
- Pastikan sudah login dan token tersimpan
- Check Authorization header: `Bearer {{jwtToken}}`
- Token mungkin expired (24 jam)

**2. 404 Not Found**
- Pastikan server running di `http://localhost:8080`
- Check baseUrl environment variable
- Verifikasi endpoint path

**3. 400 Validation Error**
- Check request body format
- Pastikan semua required fields ada
- Verifikasi data types (string untuk ID, dll)

**4. Photo Upload Failed**
- File size max 5MB
- Format harus JPEG/PNG/GIF
- Gunakan form-data bukan raw JSON

**5. 429 Too Many Requests**
- Rate limit exceeded (60 requests/minute)
- Wait for rate limit reset
- Implement request throttling in client

**6. 403 Forbidden (CSRF Protection)**
- Missing Origin header in POST/PUT/DELETE requests
- Add Origin header: `Origin: http://localhost:3000`
- Ensure CORS configuration allows your domain

**7. 400 Bad Request (Malicious Input)**
- Input contains potentially malicious content
- Check for SQL injection patterns in input
- Avoid special characters in usernames/names
- XSS content automatically sanitized

**8. Security Headers Missing**
- Check server configuration
- Verify security middleware is enabled
- All responses should include security headers

### Debug Tips
- Check Console untuk log messages
- Inspect Response untuk error details
- Use environment variables untuk consistent testing
- Run Health Check untuk verify server

## 📝 API Response Format

### Success Response
```json
{
    "success": true,
    "message": "Operation completed successfully",
    "data": {
        // Response data object
    },
    "errors": null
}
```

### Error Response
```json
{
    "success": false,
    "message": "Operation failed",
    "data": null,
    "errors": [
        "Error message 1",
        "Error message 2"
    ]
}
```

## 🎯 Best Practices

### General Testing
1. **Always Start with Health Check**: Verify server before testing
2. **Use Automated Workflow**: Run complete workflow tests regularly
3. **Check Security**: Validate authentication and authorization
4. **Environment Variables**: Use variables untuk consistent testing
5. **Photo Testing**: Test dengan file ukuran dan format berbeda
6. **Error Testing**: Test invalid data dan edge cases
7. **Token Management**: Monitor token expiry dan refresh

### Security Testing
1. **Rate Limiting**: Test with rapid successive requests
2. **Origin Headers**: Always include Origin header for POST/PUT/DELETE
3. **Malicious Input**: Test with SQL injection, XSS, and NoSQL injection payloads
4. **Authentication**: Test both valid and invalid tokens
5. **File Upload**: Test with various file types and sizes
6. **Security Headers**: Verify all responses include security headers
7. **CORS Testing**: Test cross-origin requests
8. **Input Boundaries**: Test with maximum length inputs and edge cases

### Production Deployment
1. **Environment Variables**: Configure production CORS origins
2. **Rate Limiting**: Adjust limits based on expected traffic
3. **Monitoring**: Implement logging for security events
4. **SSL/TLS**: Ensure HTTPS in production
5. **Secrets Management**: Use proper secret management for JWT keys
6. **Security Headers**: Verify all security headers in production
7. **Regular Testing**: Run security tests regularly

## 🌐 Integration dengan Tools Lain

### Swagger UI
1. Install swagger-ui-serve: `npm install -g swagger-ui-serve`
2. Run: `swagger-ui-serve docs/openapi.yaml`
3. Open browser ke URL yang ditampilkan

### VS Code REST Client
Copy request dari Postman ke .http files untuk VS Code testing

### Automated Testing
Integrate dengan CI/CD pipeline menggunakan Newman:
```bash
newman run docs/postman_collection.json -e docs/postman_environment.json
```