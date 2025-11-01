# Secure Karyawan & Kantor Management API

Production-ready REST API dengan comprehensive security features untuk manajemen data karyawan, kantor, dan jabatan yang dibangun dengan Rust dan Axum framework.

## ✨ Fitur Utama

- **🛡️ Comprehensive Security**: Rate limiting, CORS, SQL/NoSQL injection prevention, XSS protection, security headers
- **🔐 JWT Authentication**: Sistem autentikasi lengkap dengan JWT token dan password hashing
- **👥 User Management**: Register, login, dan protected endpoints dengan bcrypt security
- **📊 User Tracking**: Setiap karyawan mencatat user yang membuat dan mengupdate (created_by/updated_by)
- **🏢 Jabatan Management**: Sistem manajemen jabatan (job position) untuk karyawan
- **📝 CRUD Operations**: Create, Read, Update, Delete untuk karyawan, kantor, dan jabatan
- **📸 Photo Upload Management**: Upload, update, dan delete foto karyawan dengan validasi keamanan
- **💾 Database Integration**: MySQL database dengan Sea-ORM dan automated migrations
- **✅ Comprehensive Validation**: Validasi data yang ketat dengan database existence check
- **🔗 Required Relationships**: Setiap karyawan wajib memiliki kantor dan jabatan (no freelancer)
- **🗄️ Foreign Key Constraints**: Relasi database antara karyawan-kantor, karyawan-jabatan, dan karyawan-user
- **📋 JSON Responses**: Response API yang konsisten dalam format JSON
- **🚨 Error Handling**: Penanganan error yang informatif dan user-friendly
- **🏗️ Clean Architecture**: Struktur kode yang terorganisir dengan separation of concerns
- **🌍 Geographic Validation**: Validasi koordinat longitude dan latitude untuk kantor
- **📁 File Management**: Sistem upload file dengan keamanan dan validasi format
- **🧪 Comprehensive Testing**: Framework testing yang terorganisir dengan automation (59 total tests)
- **🐳 Docker Support**: Full containerization dengan Docker Compose
- **🔄 Auto Migration**: Database schema auto-migration pada startup

## 🛡️ Comprehensive Security Features

### Rate Limiting
- **60 requests per minute per IP address**
- Mencegah abuse dan DoS attacks
- Return 429 Too Many Requests ketika limit terlampaui

### CORS Protection
- Konfigurasi CORS yang environment-aware
- Development: mengizinkan localhost:3000, localhost:5173, 127.0.0.1:3000
- Production: allowed origins yang configurable via CORS_ORIGINS environment variable
- CSRF protection melalui Origin header validation
- **Fleksible Configuration**: Set via .env file dengan comma-separated origins

### Injection Prevention
- **SQL Injection Protection**:
  - Parameterized queries dengan SeaORM ORM
  - Pattern detection dan blocking
  - Blocks malicious SQL keywords dan operators
- **NoSQL Injection Protection**:
  - MongoDB operator filtering
  - Blocks operators seperti $ne, $gt, $where, dll.

### XSS Protection
- **HTML Sanitization** dengan Ammonia library
- **Content Security Policy (CSP)** headers
- **X-XSS-Protection** headers
- Automatic input content sanitization

### Security Headers
- **X-Content-Type-Options**: nosniff (mencegah MIME sniffing)
- **X-Frame-Options**: DENY (mencegah clickjacking)
- **X-XSS-Protection**: 1; mode=block
- **Content-Security-Policy**: Comprehensive policy

### Input Validation
- Email format validation (RFC compliant)
- String length constraints dan character validation
- File type dan size validation dengan security scanning
- Path traversal prevention

## 🚀 Teknologi

- **Rust**: Bahasa pemrograman utama
- **Axum 0.8.6**: Modern web framework untuk Rust
- **Sea-ORM 1.1.0**: Modern ORM untuk Rust dengan MySQL support
- **JWT Authentication**: Custom HMAC-SHA256 JWT implementation untuk secure authentication
- **bcrypt**: Password hashing dengan secure salt rounds
- **MySQL**: Database relational untuk penyimpanan data
- **Serde**: JSON serialization/deserialization
- **Validator**: Data validation dengan derive macros
- **Tokio**: Async runtime
- **Tower-HTTP**: HTTP middleware untuk file serving
- **Multipart**: File upload handling dengan validasi keamanan
- **Docker**: Containerization dengan multi-stage builds
- **Docker Compose**: Orchestration untuk development environment

## � Dokumentasi API

### OpenAPI/Swagger
- **File**: `docs/openapi.yaml`
- **Format**: OpenAPI 3.0.3 specification
- **Includes**: 
  - Complete endpoint documentation
  - Request/response schemas
  - Authentication flows
  - Error codes and examples
  - Photo upload specifications

### Postman Collection
- **File**: `docs/postman_collection.json`
- **Features**:
  - Ready-to-use API collection
  - Automated authentication flow
  - Test scripts and validations
  - Environment variables setup
  - Complete workflow examples
  - Security validation tests

### Import ke Postman:
1. Buka Postman
2. Click "Import" 
3. Select `docs/postman_collection.json`
4. Set environment variable `baseUrl` ke `http://localhost:8080`
5. Run "Complete Workflow Test" untuk testing otomatis

### Swagger UI (Optional):
Untuk menggunakan Swagger UI, install swagger-ui dan arahkan ke `docs/openapi.yaml`

## �📁 Struktur Project

```
src/
├── main.rs                 # Entry point aplikasi dengan database connection
├── database.rs             # Database configuration dan connection pooling
├── handlers/               # HTTP request handlers
│   ├── mod.rs
│   ├── auth.rs            # Authentication handlers (register, login, me)
│   ├── health.rs          # Health check handler
│   ├── jabatan.rs         # CRUD handlers untuk jabatan (job positions)
│   ├── karyawan.rs        # CRUD handlers untuk karyawan + foto upload
│   └── kantor.rs          # CRUD handlers untuk kantor
├── models/                 # Data structures (Sea-ORM entities)
│   ├── mod.rs
│   ├── common.rs          # Shared response models (ApiResponse)
│   ├── jabatan.rs         # Jabatan entity & request DTOs
│   ├── karyawan.rs        # Karyawan entity & request DTOs
│   ├── kantor.rs          # Kantor entity & request DTOs
│   └── user.rs            # User entity untuk authentication system
├── routes/                 # Route definitions
│   ├── mod.rs
│   ├── auth.rs            # Authentication routes (register, login, me)
│   ├── jabatan.rs         # Jabatan routes
│   ├── karyawan.rs        # Karyawan routes
│   └── kantor.rs          # Kantor routes
├── services/               # Business logic services
│   ├── mod.rs
│   ├── auth.rs            # JWT token dan password hashing services
│   └── file_upload.rs     # File upload service dengan validasi
└── validators/             # Custom validation logic
    ├── mod.rs
    ├── jabatan.rs         # Jabatan validation functions
    ├── karyawan.rs        # Karyawan validation + database checks
    └── kantor.rs          # Kantor validation functions
migration/                  # Database migrations
├── src/
│   ├── lib.rs             # Migration manager
│   ├── main.rs            # Migration CLI
│   ├── m20241028_000001_create_karyawan_table.rs
│   ├── m20241028_000002_create_kantor_table.rs
│   ├── m20241029_000003_add_foto_column_to_karyawan.rs
│   ├── m20251028_090641_add_kantor_id_to_karyawan.rs
│   ├── m20251029_101303_make_kantor_id_required.rs
│   ├── m20251029_120000_create_users_table.rs
│   ├── m20251029_140819_change_timestamp_to_datetime.rs
│   ├── m20251031_095022_add_user_tracking_to_karyawan.rs
│   ├── m20251031_100041_add_user_tracking_to_kantor.rs
│   ├── m20251031_102506_add_user_id_to_karyawan.rs
│   ├── m20251031_110440_remove_user_id_unique_constraint.rs
│   ├── m20251031_194811_create_jabatan_table.rs
│   └── m20251031_194846_add_jabatan_id_to_karyawan.rs
└── Cargo.toml             # Migration dependencies
tests/                      # Organized testing framework
├── api/                   # API functionality tests
│   ├── basic_api_test.py           # Core API tests
│   ├── auth_test.py                # Auth tests
│   ├── karyawan_crud_test.py       # Karyawan CRUD tests
│   └── kantor_crud_test.py         # Kantor CRUD tests
├── photo/                 # Photo upload testing
│   ├── photo_upload_test.py        # Upload functionality
│   ├── photo_validation_test.py    # Security validation
│   ├── photo_performance_test.py   # Performance tests
│   └── photo_security_test.py      # Security tests
├── html/                  # Interactive testing
│   └── test_photo_form.html        # Web form for manual testing
├── scripts/               # Test automation
│   ├── simple_test.ps1             # PowerShell test runner
│   └── quick_test.ps1              # Quick validation script
├── utils/                 # Test utilities
│   └── test_utils.py               # Common test functions
└── README.md              # Testing documentation
uploads/                    # File upload directory
└── karyawan/
    └── photos/            # Karyawan photo storage
```

## 🛠️ Instalasi & Menjalankan

### Prerequisites
- **Rust (1.70+)** dan Cargo
- **MySQL Server** (8.0+) 
- **Docker & Docker Compose** (untuk containerized deployment)
- **Git** (opsional)

### Option 1: Docker Compose (Recommended)

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd my-axum-app
   ```

2. **Run dengan Docker Compose**
   ```bash
   # Build dan jalankan semua services (app + database)
   docker-compose up --build
   
   # Atau run di background
   docker-compose up -d --build
   ```

   Expected output:
   ```
   [+] Running 2/2
   ✔ Container my-axum-app-db-1   Healthy                                    
   ✔ Container my-axum-app-app-1  Started
   ```

   Server akan berjalan di: `http://localhost:8080`
   
   **Untuk setup Docker lengkap, lihat [DOCKER_README.md](DOCKER_README.md)**

### Option 2: Local Development

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd my-axum-app
   ```

2. **Setup MySQL Database**
   ```sql
   # Login ke MySQL
   mysql -u root -p
   
   # Buat database
   CREATE DATABASE my_axum_db;
   exit;
   ```

3. **Configure Environment**
   ```bash
   # Copy dan edit file .env
   cp .env.example .env
   
   # Edit konfigurasi sesuai kebutuhan:
   # DATABASE_URL=mysql://username:password@localhost:3306/my_axum_db
   # CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000
   # JWT_SECRET=your-super-secret-jwt-key
   # ENVIRONMENT=development
   ```

4. **Run Database Migrations**
   ```powershell
   # Jalankan setup script
   .\setup_database.ps1
   
   # Atau manual:
   cd migration
   cargo run -- up
   cd ..
   ```

5. **Install dependencies**
   ```bash
   cargo build
   ```

6. **Jalankan aplikasi**
   ```bash
   cargo run
   ```

   Expected output:
   ```
   🔌 Connecting to database: mysql://***:***@localhost:3306/my_axum_db
   ✅ Database connected successfully
   🚀 Server running on http://0.0.0.0:8080
   ```

   Server akan berjalan di: `http://localhost:8080`

💡 **Untuk panduan setup database lengkap, lihat [DATABASE_SETUP.md](DATABASE_SETUP.md)**

## 📚 API Endpoints

### Base URL: `http://localhost:8080`

#### Authentication
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/auth/register` | Register user baru |
| POST | `/api/auth/login` | Login dan dapatkan JWT token |
| GET | `/api/user/me` | Dapatkan profil user (protected) |

#### Health Check
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |

#### Karyawan Management
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/karyawans` | Dapatkan semua karyawan |
| GET | `/api/karyawans/with-kantor` | Dapatkan semua karyawan dengan info kantor |
| GET | `/api/karyawans/:id` | Dapatkan karyawan berdasarkan ID |
| GET | `/api/karyawans/:id/with-kantor` | Dapatkan karyawan dengan info kantor berdasarkan ID |
| POST | `/api/karyawans` | Buat karyawan baru |
| POST | `/api/karyawans/with-photo` | Buat karyawan baru dengan foto |
| PUT | `/api/karyawans/:id` | Update karyawan |
| POST | `/api/karyawans/:id/photo` | Upload/update foto karyawan |
| DELETE | `/api/karyawans/:id/photo` | Hapus foto karyawan |
| DELETE | `/api/karyawans/:id` | Hapus karyawan |

#### Static File Serving
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/uploads/karyawan/photos/:filename` | Akses foto karyawan |

#### Kantor Management
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/kantors` | Dapatkan semua kantor |
| GET | `/api/kantors/:id` | Dapatkan kantor berdasarkan ID |
| POST | `/api/kantors` | Buat kantor baru |
| PUT | `/api/kantors/:id` | Update kantor |
| DELETE | `/api/kantors/:id` | Hapus kantor |

#### Jabatan Management
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/jabatans` | Dapatkan semua jabatan |
| GET | `/api/jabatans/:id` | Dapatkan jabatan berdasarkan ID |
| POST | `/api/jabatans` | Buat jabatan baru |
| PUT | `/api/jabatans/:id` | Update jabatan |
| DELETE | `/api/jabatans/:id` | Hapus jabatan |

## 📝 Database Schema & API Format

### Database Tables

#### Users Table
```sql
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(100) NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `idx_users_username` (`username`),
  KEY `idx_users_email` (`email`)
);
```

#### Karyawan Table
```sql
CREATE TABLE karyawan (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nama VARCHAR(50) NOT NULL,
  gaji INT NOT NULL,
  kantor_id INT NOT NULL,                    -- WAJIB DIISI (no freelancer)
  jabatan_id INT NOT NULL,                   -- WAJIB DIISI (job position required)
  foto_path VARCHAR(255) NULL,               -- Path ke file foto
  foto_original_name VARCHAR(255) NULL,      -- Nama file asli
  foto_size BIGINT NULL,                     -- Ukuran file dalam bytes
  foto_mime_type VARCHAR(255) NULL,          -- MIME type (image/jpeg, dll)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `idx_karyawan_kantor_id` (`kantor_id`),
  KEY `idx_karyawan_jabatan_id` (`jabatan_id`),
  CONSTRAINT `fk_karyawan_kantor_id` FOREIGN KEY (`kantor_id`) 
    REFERENCES `kantor` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_karyawan_jabatan_id` FOREIGN KEY (`jabatan_id`) 
    REFERENCES `jabatan` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
);
```

#### Kantor Table  
```sql
CREATE TABLE kantor (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nama VARCHAR(100) NOT NULL,
  alamat VARCHAR(200) NOT NULL,
  longitude DECIMAL(10,7) NOT NULL,
  latitude DECIMAL(10,7) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### Jabatan Table  
```sql
CREATE TABLE jabatan (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nama VARCHAR(100) NOT NULL,
  deskripsi TEXT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### API Response Models

#### User Model
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-10-29T10:30:00Z",
  "updated_at": "2024-10-29T10:30:00Z"
}
```

#### Login Response
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true
  }
}
```

#### Karyawan Model
```json
{
  "id": 1,
  "nama": "Budi Santoso",
  "gaji": 8000000,
  "kantor_id": 2,
  "jabatan_id": 1,
  "foto_path": "uploads/karyawan/photos/1_photo_1699234567.jpg",
  "foto_original_name": "profile.jpg",
  "foto_size": 245760,
  "foto_mime_type": "image/jpeg",
  "created_at": "2024-10-28T10:30:00Z",
  "updated_at": "2024-10-28T10:30:00Z"
}
```

#### Karyawan dengan Kantor Model
```json
{
  "id": 1,
  "nama": "Budi Santoso",
  "gaji": 8000000,
  "kantor_id": 2,
  "jabatan_id": 1,
  "kantor_nama": "Kantor Jakarta",
  "jabatan_nama": "Software Engineer",
  "foto_path": "uploads/karyawan/photos/1_photo_1699234567.jpg",
  "foto_original_name": "profile.jpg",
  "foto_size": 245760,
  "foto_mime_type": "image/jpeg",
  "created_at": "2024-10-28T10:30:00Z",
  "updated_at": "2024-10-28T10:30:00Z"
}
```

#### Kantor Model
```json
{
  "id": 1,
  "nama": "Kantor Pusat",
  "alamat": "Jl. Merdeka No.1, Jakarta",
  "longitude": "106.8271530",
  "latitude": "-6.1751100",
  "created_at": "2024-10-28T10:30:00Z",
  "updated_at": "2024-10-28T10:30:00Z"
}
```

#### Jabatan Model
```json
{
  "id": 1,
  "nama": "Software Engineer",
  "deskripsi": "Bertanggung jawab untuk pengembangan dan pemeliharaan aplikasi perangkat lunak",
  "created_at": "2024-10-31T10:30:00Z",
  "updated_at": "2024-10-31T10:30:00Z"
}
```

### Request DTOs

#### Register Request
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

#### Login Request
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

#### Create Karyawan Request (JSON)
```json
{
  "nama": "Nama Karyawan",
  "gaji": "8000000",
  "kantor_id": "2",
  "jabatan_id": "1"
}
```

#### Create Karyawan with Photo Request (Multipart Form)
```
Content-Type: multipart/form-data

Fields:
- nama: "Nama Karyawan"
- gaji: "8000000"
- kantor_id: "2"
- jabatan_id: "1"
- foto: [binary file data] (JPEG/PNG/GIF, max 5MB)
```

#### Upload Photo Request (Multipart Form)
```
Content-Type: multipart/form-data

Fields:
- foto: [binary file data] (JPEG/PNG/GIF, max 5MB)
```

#### Create Kantor Request
```json
{
  "nama": "Nama Kantor",
  "alamat": "Alamat Lengkap Kantor",
  "longitude": 106.827153,
  "latitude": -6.175110
}
```

#### Create Jabatan Request
```json
{
  "nama": "Software Engineer",
  "deskripsi": "Bertanggung jawab untuk pengembangan dan pemeliharaan aplikasi perangkat lunak"
}
```

### API Response Format
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { /* response data */ },
  "errors": null
}
```

### Error Response Format
```json
{
  "success": false,
  "message": "Operation failed",
  "data": null,
  "errors": ["Error message 1", "Error message 2"]
}
```

## ✅ Validasi Data

### Authentication Validation:
- **Username**: Required, minimal 3 karakter, maksimal 50 karakter, unique
- **Email**: Required, format email valid, maksimal 100 karakter, unique
- **Password**: Required, minimal 6 karakter untuk security
- **Full Name**: Required, minimal 2 karakter, maksimal 100 karakter
- **JWT Token**: HMAC-SHA256 signature dengan 24 jam expiration

### Karyawan Validation:
- **Nama**: Required, minimal 2 karakter, maksimal 50 karakter
- **Gaji**: 
  - Required
  - Harus berupa string yang bisa dikonversi ke angka
  - Minimal 1,000,000 (1 juta)
  - Maksimal 100,000,000 (100 juta)
- **Kantor ID**: 
  - **WAJIB DIISI** (tidak boleh kosong atau 0)
  - Harus berupa angka positif yang valid
  - **Harus mereferensi kantor yang ada di database**
  - Database existence validation
- **Jabatan ID**: 
  - **WAJIB DIISI** (tidak boleh kosong atau 0)
  - Harus berupa angka positif yang valid
  - **Harus mereferensi jabatan yang ada di database**
  - Database existence validation
- **Foto** (opsional):
  - Format: JPEG, PNG, GIF
  - Ukuran maksimal: 5MB
  - Validasi MIME type dan ekstensi file
  - Security validation untuk prevent malicious files

### Kantor Validation:
- **Nama**: Required, minimal 2 karakter, maksimal 100 karakter
- **Alamat**: Required, minimal 5 karakter, maksimal 200 karakter
- **Longitude**: Required, range -180 hingga 180
- **Latitude**: Required, range -90 hingga 90
- **ID**: Harus berupa angka positif yang valid

### Jabatan Validation:
- **Nama**: Required, minimal 2 karakter, maksimal 100 karakter
- **Deskripsi**: Optional, maksimal 1000 karakter (TEXT field)
- **ID**: Harus berupa angka positif yang valid

### File Upload Validation:
- **File Size**: Maksimal 5MB
- **File Type**: Hanya JPEG, PNG, GIF yang diperbolehkan
- **MIME Type Check**: Validasi actual file content, bukan hanya ekstensi
- **Security**: Prevent upload file executable atau script
- **Naming**: Auto-generated filename untuk prevent collision
- **Storage**: Organized dalam struktur folder `/uploads/karyawan/photos/`

### Contoh Error Authentication:
```json
{
  "success": false,
  "message": "Invalid credentials",
  "data": null,
  "errors": [
    "Username atau password salah"
  ]
}
```

### Contoh Error Token:
```json
{
  "success": false,
  "message": "Authentication required",
  "data": null,
  "errors": [
    "Token tidak valid atau expired"
  ]
}
```

### Contoh Error Validasi:
```json
{
  "success": false,
  "message": "Validation failed",
  "data": null,
  "errors": [
    "gaji: Gaji harus antara 1000000 dan 100000000",
    "kantor_id: kantor_id wajib diisi dan harus berupa angka positif yang valid"
  ]
}
```

### Contoh Error Database Validation:
```json
{
  "success": false,
  "message": "Invalid kantor_id",
  "data": null,
  "errors": [
    "Kantor dengan ID 999 tidak ditemukan di database"
  ]
}
```

### Contoh Error File Upload:
```json
{
  "success": false,
  "message": "Failed to upload photo",
  "data": null,
  "errors": [
    "File size exceeds maximum allowed size of 5MB"
  ]
}
```

## 🧪 Testing

### Organized Testing Framework

Project ini memiliki **testing framework yang terorganisir** dengan struktur folder yang rapi dan automation scripts:

```
tests/
├── api/                   # API functionality tests
├── photo/                 # Photo upload comprehensive tests
├── html/                  # Interactive browser testing
├── scripts/               # PowerShell automation
├── utils/                 # Common test utilities
└── README.md              # Testing documentation
```

#### Quick Start Testing:

**1. 🔒 Security Validation (Recommended First Step):**
```bash
# Quick security check (5 essential tests)
python tests/quick_validation.py
# Expected output: 100% pass rate for production readiness

# Comprehensive security testing (36 security tests)
python tests/security_tests.py
# Tests: Rate limiting, CORS, injection prevention, XSS, security headers
```

**2. 🔐 Authentication Testing:**
```bash
# JWT authentication tests (18 auth tests)
python tests/auth_tests.py
# Tests: User registration, login/logout, token validation, protected endpoints
```

**3. 📊 Complete Test Suite:**
```bash
# Master test runner (59 total tests)
python tests/master_test_runner.py --auto-start
# Features: Auto-starts server, runs all test categories, comprehensive reporting
```

**5. Legacy API Testing:**
```powershell
# Master test runner (all tests)
python run_tests.py

# Test JWT Authentication
python simple_jwt_test.py

# PowerShell automation
.\tests\scripts\simple_test.ps1

# Specific test suites
python tests\api\basic_api_test.py
python tests\api\auth_test.py
python tests\photo\photo_upload_test.py
python tests\photo\photo_security_test.py
```

### Security Testing Summary:

#### 🛡️ **Comprehensive Security Tests (36 tests)**
- ✅ **Rate Limiting**: 60 requests/minute validation
- ✅ **CORS Protection**: Environment-aware configuration testing
- ✅ **SQL Injection**: Pattern detection and parameterized query validation
- ✅ **NoSQL Injection**: MongoDB operator filtering tests
- ✅ **XSS Protection**: HTML sanitization and CSP header validation
- ✅ **Security Headers**: Complete security headers validation
- ✅ **CSRF Protection**: Origin header validation tests

#### 🔐 **Authentication Tests (18 tests)**
- ✅ **User Registration**: Security validation dan input sanitization
- ✅ **Login Flow**: Credential verification dan JWT generation
- ✅ **Token Management**: Validation, expiry, dan refresh handling
- ✅ **Protected Endpoints**: Access control dan authorization testing

#### ⚡ **Quick Validation (5 tests)**
- ✅ **Production Readiness**: Critical security feature validation
- ✅ **Essential Functionality**: Core API functionality checks
- ✅ **100% Pass Rate Required**: For production deployment

### Legacy Schemathesis Testing

Project ini juga include **Schemathesis** - property-based testing tool untuk comprehensive API testing:

#### Schemathesis Quick Start:
```powershell
# Docker + Schemathesis Integration (Recommended)
.\docker_with_schemathesis.ps1

# Standalone Schemathesis (API harus sudah running)
.\run_schemathesis_tests.ps1

# Manual Python script
python schemathesis_test.py
```

#### Schemathesis Features:
- ✅ **Property-based testing** dengan random data generation
- ✅ **Comprehensive endpoint coverage** untuk semua API routes
- ✅ **Edge case detection** dan boundary value testing
- ✅ **Response validation** untuk format dan status codes
- ✅ **Custom hooks** untuk valid test data generation
- ✅ **Integration dengan Docker** untuk full environment testing

**📖 Untuk panduan lengkap testing, lihat [tests/README.md](tests/README.md)**

### Manual Testing Scripts

Legacy Test Scripts:

1. **Test Karyawan API:**
   ```powershell
   .\test_karyawan_api.ps1
   ```

2. **Test Kantor API:**
   ```powershell
   .\test_kantor_simple.ps1
   ```

3. **Test All APIs:**
   ```powershell
   .\test_all_apis.ps1
   ```

4. **Test Relationships:**
   ```powershell
   .\test_relationships.ps1
   ```

5. **Test Validation:**
   ```powershell
   .\test_validation.ps1
   ```

6. **Test Kantor Required:**
   ```powershell
   python test_kantor_required.py
   ```

### Manual Testing dengan PowerShell

**Test Authentication:**
```powershell
# Register new user
$body = '{"username":"testuser","email":"test@example.com","password":"password123","full_name":"Test User"}'
Invoke-WebRequest -Uri http://localhost:8080/api/auth/register -Method POST -Body $body -ContentType "application/json" -UseBasicParsing

# Login and get JWT token
$body = '{"username":"testuser","password":"password123"}'
$response = Invoke-WebRequest -Uri http://localhost:8080/api/auth/login -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
$token = ($response.Content | ConvertFrom-Json).token

# Access protected endpoint
$headers = @{ "Authorization" = "Bearer $token" }
Invoke-WebRequest -Uri http://localhost:8080/api/user/me -Headers $headers -UseBasicParsing
```

**Test Karyawan:**
```powershell
# Get all karyawans
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans -UseBasicParsing

# Get karyawan with kantor info
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans/with-kantor -UseBasicParsing

# Get specific karyawan
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans/2 -UseBasicParsing

# Create new karyawan (kantor_id and jabatan_id WAJIB)
$body = '{"nama":"John Doe","gaji":"8000000","kantor_id":"2","jabatan_id":"1"}'
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans -Method POST -Body $body -ContentType "application/json" -UseBasicParsing

# Upload photo to existing karyawan
$form = @{
    foto = Get-Item "path/to/photo.jpg"
}
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans/2/photo -Method POST -Form $form
```

**Test Kantor:**
```powershell
# Get all kantors
Invoke-WebRequest -Uri http://localhost:8080/api/kantors -UseBasicParsing

# Create new kantor
$body = '{"nama":"Kantor Cabang","alamat":"Jl. Test No.1","longitude":106.8,"latitude":-6.2}'
Invoke-WebRequest -Uri http://localhost:8080/api/kantors -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
```

### Menggunakan curl (jika tersedia):
```bash
# Test authentication endpoints
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123","full_name":"Test User"}'

curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# Get JWT token and use for protected endpoint
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' | \
  jq -r '.token')

curl -H "Authorization: Bearer $TOKEN" http://localhost:8080/api/user/me

# Test karyawan endpoints
curl http://localhost:8080/api/karyawans
curl http://localhost:8080/api/karyawans/2
curl http://localhost:8080/api/karyawans/2/with-kantor

# Create karyawan (kantor_id and jabatan_id WAJIB)
curl -X POST http://localhost:8080/api/karyawans \
  -H "Content-Type: application/json" \
  -d '{"nama":"Jane Doe","gaji":"12000000","kantor_id":"2","jabatan_id":"1"}'

# Upload photo
curl -X POST http://localhost:8080/api/karyawans/2/photo \
  -F "foto=@path/to/photo.jpg"

# Create karyawan with photo
curl -X POST http://localhost:8080/api/karyawans/with-photo \
  -F "nama=Test User" \
  -F "gaji=8000000" \
  -F "kantor_id=2" \
  -F "jabatan_id=1" \
  -F "foto=@path/to/photo.jpg"

# Test kantor endpoints
curl http://localhost:8080/api/kantors
curl http://localhost:8080/api/kantors/2
curl -X POST http://localhost:8080/api/kantors \
  -H "Content-Type: application/json" \
  -d '{"nama":"Kantor Baru","alamat":"Jl. Baru No.123","longitude":107.6,"latitude":-6.9}'
```

## ⚙️ Environment Variables Configuration

API mendukung konfigurasi fleksibel melalui environment variables di file `.env`:

### Database Configuration
```env
DATABASE_URL=mysql://username:password@localhost:3306/database_name
```

### Server Configuration  
```env
PORT=8080
HOST=0.0.0.0
```

### JWT Authentication
```env
JWT_SECRET=your-super-secret-jwt-key-make-sure-it-is-at-least-256-bits-long-for-security
JWT_EXPIRE_HOURS=24
```

### CORS Configuration
```env
# Comma-separated list of allowed origins
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000

# Environment setting
ENVIRONMENT=development
```

### Example Configurations

#### Development (.env)
```env
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000
DATABASE_URL=mysql://axum:rahasia123@localhost:3306/my_axum_db
JWT_SECRET=your-development-secret-key
```

#### Production
```env
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://api.yourdomain.com
DATABASE_URL=mysql://prod_user:secure_password@prod_server:3306/prod_database
JWT_SECRET=your-super-secure-production-secret-key-at-least-256-bits
```

**📖 Detailed CORS Configuration Guide**: See `docs/CORS_CONFIGURATION_GUIDE.md` for comprehensive CORS setup instructions.

## 🔧 Development

### Menjalankan dalam mode development:
```bash
cargo watch -x run
```

### Check code quality:
```bash
cargo check
cargo clippy
cargo fmt
```

### Database Operations:
```bash
# Check migration status
cd migration && cargo run -- status

# Run pending migrations  
cd migration && cargo run -- up

# Rollback last migration
cd migration && cargo run -- down

# Reset all migrations
cd migration && cargo run -- reset
```

### Docker Development:
```bash
# Build only
docker-compose build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Rebuild and restart
docker-compose down && docker-compose up --build

# Full Docker + Schemathesis testing
.\docker_with_schemathesis.ps1
```

## 📖 Arsitektur

### Database Layer:
- **Sea-ORM**: Modern ORM dengan type-safe query builder
- **Connection Pooling**: Efficient database connection management
- **Migrations**: Automated schema versioning dan management
- **Entity Models**: Type-safe database models dengan validations
- **Foreign Key Constraints**: RESTRICT policy untuk data integrity
- **Authentication Schema**: Users table dengan unique constraints dan indexes

### Security Layer:
- **JWT Authentication**: Custom HMAC-SHA256 implementation dengan secure token generation
- **Password Security**: bcrypt hashing dengan secure salt rounds
- **Token Validation**: Bearer token authentication untuk protected endpoints
- **Input Validation**: Comprehensive validation untuk authentication endpoints
- **ARM64 Compatibility**: Custom JWT implementation untuk ARM64 Windows environment

### Business Logic Layer:
- **Services**: File upload service dengan keamanan dan validasi
- **Validators**: Database existence validation dan business rules
- **Custom Validation**: Comprehensive input validation dengan error messages
- **File Management**: Organized file storage dengan automatic cleanup

### Separation of Concerns:
- **Database**: Connection management dan ORM configuration
- **Authentication**: JWT service dan password hashing dalam services layer
- **Handlers**: HTTP requests dan business logic orchestration
- **Models**: Sea-ORM entities dan request/response DTOs
- **Services**: Reusable business logic (authentication, file upload, etc.)
- **Validators**: Custom validation logic untuk business rules
- **Routes**: Definisi routing yang terpisah dari main.rs
- **Middleware**: Authentication middleware untuk protected endpoints

### Design Patterns:
- **Repository Pattern**: Database operations encapsulated dalam Sea-ORM entities
- **Service Layer Pattern**: Business logic separated dalam service modules
- **Modular Architecture**: Setiap domain (karyawan, kantor) memiliki module terpisah
- **Dependency Injection**: Database connection di-inject ke handlers via Axum Extension
- **Error Handling**: Centralized error handling dengan custom response types
- **Clean Code**: Separation of concerns dengan folder structure yang jelas
- **Migration Pattern**: Database schema changes managed via versioned migrations

### Security & File Management:
- **File Upload Security**: MIME type validation, size limits, malicious file prevention
- **Organized Storage**: Structured file organization (`/uploads/karyawan/photos/`)
- **Unique Naming**: Timestamp-based naming untuk prevent collision
- **Cleanup**: Automatic file cleanup saat delete karyawan atau replace foto
- **Validation**: Multiple layers of validation (extension, MIME, size, content)

### Module Structure:
```
├── database.rs        # Database connection layer
├── handlers/          # HTTP layer dengan business logic
│   ├── auth.rs       # Authentication handlers (register, login, me)
│   ├── health.rs     # Health check
│   ├── karyawan.rs   # Karyawan CRUD
│   └── kantor.rs     # Kantor CRUD
├── models/           # Sea-ORM entity layer
│   ├── user.rs       # User authentication model
│   ├── karyawan.rs   # Karyawan model
│   └── kantor.rs     # Kantor model
├── services/         # Business logic layer
│   ├── auth.rs       # JWT dan password services
│   └── file_upload.rs # File upload service
├── validators/       # Business logic validation layer
├── routes/          # Routing layer
│   ├── auth.rs       # Authentication routes
│   ├── karyawan.rs   # Karyawan routes
│   └── kantor.rs     # Kantor routes
├── migration/        # Database schema management
└── main.rs         # Application setup dengan database initialization
```

## 🎯 Features Teruji

### JWT Authentication System:
- ✅ **User Registration** dengan password hashing menggunakan bcrypt
- ✅ **User Login** dengan credential validation dan JWT token generation
- ✅ **Protected Endpoints** dengan Bearer token authentication
- ✅ **Custom JWT Implementation** HMAC-SHA256 untuk ARM64 Windows compatibility
- ✅ **Password Security** dengan bcrypt secure salt rounds
- ✅ **Token Validation** dengan proper error handling dan user feedback
- ✅ **Database Integration** dengan users table dan proper indexes

### Photo Upload & File Management:
- ✅ **File Upload** dengan multipart form data handling
- ✅ **Security Validation** dengan MIME type checking dan malicious file prevention
- ✅ **File Size Limits** maksimal 5MB dengan proper error handling
- ✅ **Supported Formats** JPEG, PNG, GIF dengan content validation
- ✅ **Organized Storage** dalam struktur `/uploads/karyawan/photos/`
- ✅ **Unique Naming** dengan timestamp untuk prevent collision
- ✅ **Automatic Cleanup** saat delete karyawan atau replace foto
- ✅ **Database Integration** foto metadata tersimpan di database

### Enhanced Validation System:
- ✅ **Kantor ID Validation** dengan database existence check
- ✅ **Required Kantor** - tidak ada freelancer yang diperbolehkan
- ✅ **Database Constraint Validation** dengan foreign key RESTRICT
- ✅ **Comprehensive Error Messages** yang informatif dan user-friendly
- ✅ **Input Sanitization** dan security validation
- ✅ **Business Rules Enforcement** di multiple layers

### Organized Testing Framework:
- ✅ **Structured Test Directory** dengan organized test suites
- ✅ **Authentication Testing** comprehensive untuk register, login, protected endpoints
- ✅ **API Testing** comprehensive untuk semua endpoints
- ✅ **Photo Upload Testing** dengan security dan performance tests
- ✅ **Interactive Testing** dengan HTML form untuk manual verification
- ✅ **PowerShell Automation** untuk Windows environment
- ✅ **Master Test Runners** dengan orchestrated execution
- ✅ **Test Utilities** untuk reusable testing functions

### Docker & Containerization:
- ✅ Multi-stage Docker build dengan Rust nightly
- ✅ Auto-migration pada container startup
- ✅ Docker Compose dengan MySQL service
- ✅ Health checks dan proper dependency management
- ✅ Non-root user security dalam container
- ✅ Production-ready deployment setup

### Database Integration:
- ✅ MySQL connection dengan Sea-ORM
- ✅ Automated migrations untuk schema management
- ✅ Connection pooling untuk performance
- ✅ Type-safe database operations
- ✅ Auto-generated timestamps (created_at, updated_at)
- ✅ Foreign key relationships (karyawan → kantor)

### Karyawan Management:
- ✅ CRUD operations lengkap dengan database persistence
- ✅ **Kantor ID WAJIB** - tidak ada freelancer (kantor_id = 0 rejected)
- ✅ **Database Validation** untuk kantor existence checking
- ✅ Validation gaji dengan string input dan range checking
- ✅ Error handling untuk ID invalid dan custom error messages
- ✅ **Photo Upload Integration** dengan create dan update operations
- ✅ **Photo Management** upload, update, delete dengan security validation
- ✅ Database constraint validation dengan foreign key RESTRICT
- ✅ Relationship queries dengan kantor information
- ✅ Endpoint dengan dan tanpa kantor info

### Kantor Management:
- ✅ CRUD operations lengkap dengan database persistence
- ✅ Geographic coordinate validation (Decimal precision)
- ✅ Boundary value testing (-180/180, -90/90)
- ✅ Address dan nama validation
- ✅ Database constraint validation

### API Routing & Endpoints:
- ✅ Proper Axum routing dengan `:id` parameters
- ✅ Fixed variable shadowing bugs
- ✅ RESTful API design
- ✅ Consistent JSON response format
- ✅ Comprehensive error handling

### Testing Coverage:
- ✅ **Organized Test Framework** dengan structured directories
- ✅ **Authentication Tests** untuk JWT system end-to-end
- ✅ **API Functionality Tests** untuk semua endpoints
- ✅ **Photo Upload Tests** dengan security dan performance coverage
- ✅ **Interactive Testing** dengan HTML forms
- ✅ **PowerShell Automation** untuk Windows environment
- ✅ **Legacy Schemathesis** property-based testing
- ✅ **Validation Tests** untuk kantor required dan database checks
- ✅ **Error Handling Tests** comprehensive error scenarios
- ✅ **Boundary Value Tests** untuk edge cases
- ✅ **Relationship Testing** karyawan-kantor integration
- ✅ **Automated Docker + API integration testing**

## 🛠️ Known Issues & Fixes

### Recently Fixed Issues:
1. **✅ Comprehensive Security Implementation**: Rate limiting, CORS, injection prevention, XSS protection, security headers
2. **✅ Environment-Based CORS Configuration**: Flexible CORS_ORIGINS support untuk development dan production
3. **✅ JWT Authentication System**: Implemented complete authentication dengan register, login, protected endpoints
4. **✅ Security Testing Framework**: 59 total tests (36 security + 18 auth + 5 quick validation)
5. **✅ Password Security**: bcrypt hashing dengan secure salt rounds untuk user passwords
6. **✅ Custom JWT Implementation**: HMAC-SHA256 JWT untuk ARM64 Windows compatibility
7. **✅ Freelancer Prevention**: Implemented kantor_id WAJIB requirement - no more freelancer allowed
8. **✅ Database Validation**: Added database existence check untuk kantor_id validation
9. **✅ Photo Upload Security**: Comprehensive file validation dengan MIME type checking dan malicious file prevention
10. **✅ Test Organization**: Organized scattered test files into structured testing framework
11. **✅ File Management**: Automatic cleanup dan organized storage system
12. **✅ Foreign Key Constraints**: Updated to RESTRICT untuk prevent data inconsistency
13. **✅ Docker Build Issues**: Fixed Rust edition compatibility dan Cargo.lock handling
14. **✅ Route Parameter Syntax**: Changed `{id}` to `:id` untuk proper Axum routing
15. **✅ Variable Shadowing**: Fixed konflik nama variabel dalam handler parameters
16. **✅ Database Migration**: Implemented auto-migration pada container startup

### Current Limitations:
- Database seeding masih manual via init.sql
- Belum ada role-based authorization system (hanya basic authentication)
- Belum ada pagination untuk large datasets
- Belum ada audit logging untuk data changes
- Photo resizing/thumbnail generation belum implemented
- Belum ada password reset functionality
- JWT token refresh mechanism belum implemented

## 🚀 Future Enhancements:
- [ ] Role-based Authorization dengan JWT claims
- [ ] JWT Token Refresh mechanism
- [ ] Password Reset functionality dengan email verification
- [ ] Pagination dan filtering untuk endpoints
- [ ] Audit logging system
- [ ] Rate limiting per-user (currently per-IP)
- [ ] API versioning strategy
- [ ] Background job processing
- [ ] Email notifications
- [ ] **Photo Processing**: Image resizing, thumbnail generation
- [ ] **Advanced File Management**: Multiple photo support, gallery view
- [ ] **Enhanced Security**: File virus scanning, advanced validation
- [ ] **Performance**: Image optimization, lazy loading, caching
- [ ] **User Management**: Role-based access control, user groups
- [ ] **Reporting**: Analytics dan reporting system
- [ ] **Monitoring**: Application performance monitoring, logging

## 🤝 Contributing

1. Fork repository
2. Buat feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buat Pull Request

## 📄 License

MIT License - lihat file LICENSE untuk detail lengkap.

---

**Author**: [jauharianggara]  
**Version**: 6.0.0  
**Last Updated**: November 1, 2025  
**Security Status**: ✅ Production Ready (100% Security Implementation)

## 📁 Documentation & Project Organization

### Project Structure Overview
- [docs/PROJECT_ORGANIZATION.md](docs/PROJECT_ORGANIZATION.md) - **Comprehensive project structure guide**

### Setup & Configuration Guides
- [docs/README.md](docs/README.md) - **Main documentation directory guide**
- [docs/SECURITY_IMPLEMENTATION.md](docs/SECURITY_IMPLEMENTATION.md) - **Comprehensive security implementation guide**
- [docs/SECURITY_STATUS_REPORT.md](docs/SECURITY_STATUS_REPORT.md) - **Production security status report**
- [docs/CORS_CONFIGURATION_GUIDE.md](docs/CORS_CONFIGURATION_GUIDE.md) - **Environment-based CORS configuration**
- [docs/DATABASE_SETUP.md](docs/DATABASE_SETUP.md) - Panduan setup database lengkap
- [docs/DOCKER_README.md](docs/DOCKER_README.md) - Panduan Docker deployment lengkap
- [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md) - General testing guidelines
- [docs/API_DOCUMENTATION_GUIDE.md](docs/API_DOCUMENTATION_GUIDE.md) - API documentation dan testing procedures

### Testing Framework
- [tests/README.md](tests/README.md) - Organized testing framework documentation
- [docs/test-results/](docs/test-results/) - Test execution results

### Feature Documentation
- [docs/summaries/20251029_FOTO_FEATURE_DOCUMENTATION.md](docs/summaries/20251029_FOTO_FEATURE_DOCUMENTATION.md) - Photo upload feature documentation
- [docs/summaries/20251029_KANTOR_VALIDATION_SUMMARY.md](docs/summaries/20251029_KANTOR_VALIDATION_SUMMARY.md) - Kantor validation implementation
- [docs/summaries/20251029_KANTOR_REQUIRED_SUMMARY.md](docs/summaries/20251029_KANTOR_REQUIRED_SUMMARY.md) - Kantor required enforcement
- [docs/summaries/20251029_TEST_ORGANIZATION_SUMMARY.md](docs/summaries/20251029_TEST_ORGANIZATION_SUMMARY.md) - Testing framework organization
- [docs/summaries/20251029_IMPLEMENTATION_SUMMARY.md](docs/summaries/20251029_IMPLEMENTATION_SUMMARY.md) - Overall implementation details

### Legacy References
- [legacy-tests/](legacy-tests/) - Legacy test files (superseded by organized tests/)
- [README_NEW.md](README_NEW.md) - Additional project information

### Quick Navigation
- **For Setup**: Check `docs/` folder for configuration guides
- **For Testing**: Use `tests/` framework and check `docs/test-results/`
- **For Development**: See `docs/summaries/` for feature implementation details
- **For Scripts**: Use `scripts/` folder for automation tools