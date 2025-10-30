# 📚 API Documentation Guide

Panduan lengkap untuk menggunakan dokumentasi API Karyawan & Kantor Management.

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

**Fitur Utama**:
- **Comprehensive**: Mencakup semua endpoint dari health check hingga file upload
- **Interactive**: Dapat digunakan untuk testing langsung (jika ada Swagger UI)
- **Detailed**: Schema lengkap dengan validation rules
- **Standard Compliant**: Mengikuti OpenAPI 3.0.3 standards

### 2. Postman Collection
File: `docs/postman_collection.json`

**Features**:
- 🚀 **Ready-to-use**: Import dan langsung bisa digunakan
- 🔧 **Automated Scripts**: Test scripts dan environment variable automation
- 🧪 **Testing Suites**: Complete workflow testing dan security validation
- 📋 **Examples**: Real request/response examples
- 🔐 **Authentication Flow**: Automated JWT token management

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

1. **Always Start with Health Check**: Verify server before testing
2. **Use Automated Workflow**: Run complete workflow tests regularly
3. **Check Security**: Validate authentication and authorization
4. **Environment Variables**: Use variables untuk consistent testing
5. **Photo Testing**: Test dengan file ukuran dan format berbeda
6. **Error Testing**: Test invalid data dan edge cases
7. **Token Management**: Monitor token expiry dan refresh

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