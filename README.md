# Karyawan & Kantor Management API

REST API untuk manajemen data karyawan dan kantor yang dibangun dengan Rust dan Axum framework.

## ✨ Fitur Utama

- **CRUD Operations**: Create, Read, Update, Delete untuk karyawan dan kantor
- **Photo Upload Management**: Upload, update, dan delete foto karyawan dengan validasi keamanan
- **Database Integration**: MySQL database dengan Sea-ORM dan automated migrations
- **Comprehensive Validation**: Validasi data yang ketat dengan database existence check
- **Kantor Relationship**: Sistem kantor wajib untuk setiap karyawan (no freelancer)
- **JSON Responses**: Response API yang konsisten dalam format JSON
- **Error Handling**: Penanganan error yang informatif dan user-friendly
- **Clean Architecture**: Struktur kode yang terorganisir dengan separation of concerns
- **Geographic Validation**: Validasi koordinat longitude dan latitude untuk kantor
- **File Management**: Sistem upload file dengan keamanan dan validasi format
- **Comprehensive Testing**: Framework testing yang terorganisir dengan automation
- **Docker Support**: Full containerization dengan Docker Compose
- **Auto Migration**: Database schema auto-migration pada startup

## 🚀 Teknologi

- **Rust**: Bahasa pemrograman utama
- **Axum 0.8.6**: Modern web framework untuk Rust
- **Sea-ORM 1.1.0**: Modern ORM untuk Rust dengan MySQL support
- **MySQL**: Database relational untuk penyimpanan data
- **Serde**: JSON serialization/deserialization
- **Validator**: Data validation dengan derive macros
- **Tokio**: Async runtime
- **Tower-HTTP**: HTTP middleware untuk file serving
- **Multipart**: File upload handling dengan validasi keamanan
- **Docker**: Containerization dengan multi-stage builds
- **Docker Compose**: Orchestration untuk development environment

## 📁 Struktur Project

```
src/
├── main.rs                 # Entry point aplikasi dengan database connection
├── database.rs             # Database configuration dan connection pooling
├── handlers/               # HTTP request handlers
│   ├── mod.rs
│   ├── health.rs          # Health check handler
│   ├── karyawan.rs        # CRUD handlers untuk karyawan + foto upload
│   └── kantor.rs          # CRUD handlers untuk kantor
├── models/                 # Data structures (Sea-ORM entities)
│   ├── mod.rs
│   ├── common.rs          # Shared response models (ApiResponse)
│   ├── karyawan.rs        # Karyawan entity & request DTOs
│   └── kantor.rs          # Kantor entity & request DTOs
├── routes/                 # Route definitions
│   ├── mod.rs
│   ├── karyawan.rs        # Karyawan routes
│   └── kantor.rs          # Kantor routes
├── services/               # Business logic services
│   ├── mod.rs
│   └── file_upload.rs     # File upload service dengan validasi
└── validators/             # Custom validation logic
    ├── mod.rs
    ├── karyawan.rs        # Karyawan validation + database checks
    └── kantor.rs          # Kantor validation functions
migration/                  # Database migrations
├── src/
│   ├── lib.rs             # Migration manager
│   ├── main.rs            # Migration CLI
│   └── m2024*.rs          # Individual migration files
└── Cargo.toml             # Migration dependencies
tests/                      # Organized testing framework
├── api/                   # API functionality tests
│   ├── basic_api_test.py           # Core API tests
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
   
   # Edit DATABASE_URL sesuai kredensial MySQL Anda
   # DATABASE_URL=mysql://username:password@localhost:3306/my_axum_db
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

## 📝 Database Schema & API Format

### Database Tables

#### Karyawan Table
```sql
CREATE TABLE karyawan (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nama VARCHAR(50) NOT NULL,
  posisi VARCHAR(30) NOT NULL,
  gaji INT NOT NULL,
  kantor_id INT NOT NULL,                    -- WAJIB DIISI (no freelancer)
  foto_path VARCHAR(255) NULL,               -- Path ke file foto
  foto_original_name VARCHAR(255) NULL,      -- Nama file asli
  foto_size BIGINT NULL,                     -- Ukuran file dalam bytes
  foto_mime_type VARCHAR(255) NULL,          -- MIME type (image/jpeg, dll)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `idx_karyawan_kantor_id` (`kantor_id`),
  CONSTRAINT `fk_karyawan_kantor_id` FOREIGN KEY (`kantor_id`) 
    REFERENCES `kantor` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
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

### API Response Models

#### Karyawan Model
```json
{
  "id": 1,
  "nama": "Budi Santoso",
  "posisi": "Software Engineer", 
  "gaji": 8000000,
  "kantor_id": 2,
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
  "posisi": "Software Engineer", 
  "gaji": 8000000,
  "kantor_id": 2,
  "kantor_nama": "Kantor Jakarta",
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

### Request DTOs

#### Create Karyawan Request (JSON)
```json
{
  "nama": "Nama Karyawan",
  "posisi": "Posisi Jabatan",
  "gaji": "8000000",
  "kantor_id": "2"
}
```

#### Create Karyawan with Photo Request (Multipart Form)
```
Content-Type: multipart/form-data

Fields:
- nama: "Nama Karyawan"
- posisi: "Posisi Jabatan" 
- gaji: "8000000"
- kantor_id: "2"
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

### Karyawan Validation:
- **Nama**: Required, minimal 2 karakter, maksimal 50 karakter
- **Posisi**: Required, minimal 2 karakter, maksimal 30 karakter
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

### File Upload Validation:
- **File Size**: Maksimal 5MB
- **File Type**: Hanya JPEG, PNG, GIF yang diperbolehkan
- **MIME Type Check**: Validasi actual file content, bukan hanya ekstensi
- **Security**: Prevent upload file executable atau script
- **Naming**: Auto-generated filename untuk prevent collision
- **Storage**: Organized dalam struktur folder `/uploads/karyawan/photos/`

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
```powershell
# Master test runner (all tests)
python run_tests.py

# PowerShell automation
.\tests\scripts\simple_test.ps1

# Specific test suites
python tests\api\basic_api_test.py
python tests\photo\photo_upload_test.py
python tests\photo\photo_security_test.py
```

### Comprehensive Test Coverage:

#### 1. **API Functionality Tests** (`tests/api/`)
- ✅ **Basic API Tests**: Health checks, endpoint availability
- ✅ **Karyawan CRUD Tests**: Complete CRUD operations dengan validasi
- ✅ **Kantor CRUD Tests**: Complete CRUD operations dengan geographic validation
- ✅ **Relationship Tests**: Karyawan-kantor relationship testing
- ✅ **Database Validation Tests**: Kantor existence checking

#### 2. **Photo Upload Tests** (`tests/photo/`)
- ✅ **Upload Functionality**: Create dengan foto, upload ke existing karyawan
- ✅ **Security Validation**: Malicious file prevention, MIME type checking
- ✅ **Performance Tests**: Multiple upload, large file handling
- ✅ **File Management**: Delete, replace, cleanup operations

#### 3. **Interactive Testing** (`tests/html/`)
- ✅ **Web Form**: Browser-based testing form untuk manual verification
- ✅ **File Upload UI**: Drag-and-drop interface untuk foto testing

#### 4. **Test Automation** (`tests/scripts/`)
- ✅ **PowerShell Scripts**: Cross-platform automation untuk Windows
- ✅ **Master Runners**: Orchestrated test execution dengan reporting
- ✅ **Quick Tests**: Fast validation untuk development workflow

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

**Test Karyawan:**
```powershell
# Get all karyawans
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans -UseBasicParsing

# Get karyawan with kantor info
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans/with-kantor -UseBasicParsing

# Get specific karyawan
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans/2 -UseBasicParsing

# Create new karyawan (kantor_id WAJIB)
$body = '{"nama":"John Doe","posisi":"Developer","gaji":"8000000","kantor_id":"2"}'
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
# Test karyawan endpoints
curl http://localhost:8080/api/karyawans
curl http://localhost:8080/api/karyawans/2
curl http://localhost:8080/api/karyawans/2/with-kantor

# Create karyawan (kantor_id WAJIB)
curl -X POST http://localhost:8080/api/karyawans \
  -H "Content-Type: application/json" \
  -d '{"nama":"Jane Doe","posisi":"Manager","gaji":"12000000","kantor_id":"2"}'

# Upload photo
curl -X POST http://localhost:8080/api/karyawans/2/photo \
  -F "foto=@path/to/photo.jpg"

# Create karyawan with photo
curl -X POST http://localhost:8080/api/karyawans/with-photo \
  -F "nama=Test User" \
  -F "posisi=Developer" \
  -F "gaji=8000000" \
  -F "kantor_id=2" \
  -F "foto=@path/to/photo.jpg"

# Test kantor endpoints
curl http://localhost:8080/api/kantors
curl http://localhost:8080/api/kantors/2
curl -X POST http://localhost:8080/api/kantors \
  -H "Content-Type: application/json" \
  -d '{"nama":"Kantor Baru","alamat":"Jl. Baru No.123","longitude":107.6,"latitude":-6.9}'
```

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

### Business Logic Layer:
- **Services**: File upload service dengan keamanan dan validasi
- **Validators**: Database existence validation dan business rules
- **Custom Validation**: Comprehensive input validation dengan error messages
- **File Management**: Organized file storage dengan automatic cleanup

### Separation of Concerns:
- **Database**: Connection management dan ORM configuration
- **Handlers**: HTTP requests dan business logic orchestration
- **Models**: Sea-ORM entities dan request/response DTOs
- **Services**: Reusable business logic (file upload, etc.)
- **Validators**: Custom validation logic untuk business rules
- **Routes**: Definisi routing yang terpisah dari main.rs

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
├── models/           # Sea-ORM entity layer
├── services/         # Business logic layer (file upload, etc.)
├── validators/       # Business logic validation layer
├── routes/          # Routing layer
├── migration/        # Database schema management
└── main.rs         # Application setup dengan database initialization
```

## 🎯 Features Teruji

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
1. **✅ Freelancer Prevention**: Implemented kantor_id WAJIB requirement - no more freelancer allowed
2. **✅ Database Validation**: Added database existence check untuk kantor_id validation
3. **✅ Photo Upload Security**: Comprehensive file validation dengan MIME type checking
4. **✅ Test Organization**: Organized scattered test files into structured testing framework
5. **✅ File Management**: Automatic cleanup dan organized storage system
6. **✅ Foreign Key Constraints**: Updated to RESTRICT untuk prevent data inconsistency
7. **✅ Docker Build Issues**: Fixed Rust edition compatibility dan Cargo.lock handling
8. **✅ Route Parameter Syntax**: Changed `{id}` to `:id` untuk proper Axum routing
9. **✅ Variable Shadowing**: Fixed konflik nama variabel dalam handler parameters
10. **✅ Database Migration**: Implemented auto-migration pada container startup

### Current Limitations:
- Database seeding masih manual via init.sql
- Belum ada authentication/authorization system
- Belum ada pagination untuk large datasets
- Belum ada audit logging untuk data changes
- Photo resizing/thumbnail generation belum implemented

## 🚀 Future Enhancements:
- [ ] Authentication & Authorization dengan JWT
- [ ] Pagination dan filtering untuk endpoints
- [ ] Audit logging system
- [ ] API documentation dengan OpenAPI/Swagger
- [ ] Rate limiting dan caching
- [ ] Background job processing
- [ ] Email notifications
- [ ] **Photo Processing**: Image resizing, thumbnail generation
- [ ] **Advanced File Management**: Multiple photo support, gallery view
- [ ] **Enhanced Security**: File virus scanning, advanced validation
- [ ] **Performance**: Image optimization, lazy loading
- [ ] **User Management**: Role-based access control
- [ ] **Reporting**: Analytics dan reporting system

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
**Version**: 3.0.0  
**Last Updated**: October 29, 2025

## 📁 Documentation & Project Organization

### Project Structure Overview
- [docs/PROJECT_ORGANIZATION.md](docs/PROJECT_ORGANIZATION.md) - **Comprehensive project structure guide**

### Setup & Configuration Guides
- [docs/DATABASE_SETUP.md](docs/DATABASE_SETUP.md) - Panduan setup database lengkap
- [docs/DOCKER_README.md](docs/DOCKER_README.md) - Panduan Docker deployment lengkap
- [docs/SCHEMATHESIS_GUIDE.md](docs/SCHEMATHESIS_GUIDE.md) - Comprehensive Schemathesis testing guide
- [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md) - General testing guidelines

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