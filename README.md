# Karyawan & Kantor Management API

REST API untuk manajemen data karyawan dan kantor yang dibangun dengan Rust dan Axum framework.

## ✨ Fitur

- **CRUD Operations**: Create, Read, Update, Delete untuk karyawan dan kantor
- **Database Integration**: MySQL database dengan Sea-ORM
- **Data Validation**: Validasi komprehensif untuk semua input data
- **JSON Responses**: Response API yang konsisten dalam format JSON
- **Error Handling**: Penanganan error yang informatif
- **Clean Architecture**: Struktur kode yang terorganisir dengan baik
- **Geographic Validation**: Validasi koordinat longitude dan latitude untuk kantor
- **Database Migrations**: Automated schema management
- **Connection Pooling**: Efficient database connection management
- **Docker Support**: Full containerization dengan Docker Compose
- **Relationship Management**: Support untuk relasi karyawan-kantor
- **Auto Migration**: Database schema auto-migration pada startup container

## 🚀 Teknologi

- **Rust**: Bahasa pemrograman utama
- **Axum 0.8.6**: Modern web framework untuk Rust
- **Sea-ORM 1.1.0**: Modern ORM untuk Rust dengan MySQL support
- **MySQL**: Database relational untuk penyimpanan data
- **Serde**: JSON serialization/deserialization
- **Validator**: Data validation dengan derive macros
- **Tokio**: Async runtime
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
│   ├── karyawan.rs        # CRUD handlers untuk karyawan
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
└── validators/             # Custom validation logic
    ├── mod.rs
    ├── karyawan.rs        # Karyawan validation functions
    └── kantor.rs          # Kantor validation functions
migration/                  # Database migrations
├── src/
│   ├── lib.rs             # Migration manager
│   ├── main.rs            # Migration CLI
│   └── m2024*.rs          # Individual migration files
└── Cargo.toml             # Migration dependencies
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
| PUT | `/api/karyawans/:id` | Update karyawan |
| DELETE | `/api/karyawans/:id` | Hapus karyawan |

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
  kantor_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `idx_karyawan_kantor_id` (`kantor_id`),
  CONSTRAINT `fk_karyawan_kantor` FOREIGN KEY (`kantor_id`) REFERENCES `kantor` (`id`)
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

### Create Karyawan Request
```json
{
  "nama": "Nama Karyawan",
  "posisi": "Posisi Jabatan",
  "gaji": "8000000",
  "kantor_id": "2"
}
```

### Create Kantor Request
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
  - Required
  - Harus berupa angka positif yang valid
  - Harus mereferensi kantor yang ada
- **ID**: Harus berupa angka positif yang valid

### Kantor Validation:
- **Nama**: Required, minimal 2 karakter, maksimal 100 karakter
- **Alamat**: Required, minimal 5 karakter, maksimal 200 karakter
- **Longitude**: Required, range -180 hingga 180
- **Latitude**: Required, range -90 hingga 90
- **ID**: Harus berupa angka positif yang valid

### Contoh Error Validasi:
```json
{
  "success": false,
  "message": "Validation failed",
  "data": null,
  "errors": [
    "gaji: Gaji harus antara 1000000 dan 50000000",
    "longitude: Longitude harus antara -180 hingga 180"
  ]
}
```

## 🧪 Testing

### Test Scripts Tersedia:

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

### Manual Testing dengan PowerShell

**Test Karyawan:**
```powershell
# Get all karyawans
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans -UseBasicParsing

# Get karyawan with kantor info
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans/with-kantor -UseBasicParsing

# Get specific karyawan
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans/2 -UseBasicParsing

# Create new karyawan
$body = '{"nama":"John Doe","posisi":"Developer","gaji":"8000000","kantor_id":"2"}'
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
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
curl -X POST http://localhost:8080/api/karyawans \
  -H "Content-Type: application/json" \
  -d '{"nama":"Jane Doe","posisi":"Manager","gaji":"12000000","kantor_id":"2"}'

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
```

## 📖 Arsitektur

### Database Layer:
- **Sea-ORM**: Modern ORM dengan type-safe query builder
- **Connection Pooling**: Efficient database connection management
- **Migrations**: Automated schema versioning dan management
- **Entity Models**: Type-safe database models dengan validations

### Separation of Concerns:
- **Database**: Connection management dan ORM configuration
- **Handlers**: HTTP requests dan database operations
- **Models**: Sea-ORM entities dan request/response DTOs
- **Validators**: Custom validation logic untuk business rules
- **Routes**: Definisi routing yang terpisah dari main.rs

### Design Patterns:
- **Repository Pattern**: Database operations encapsulated dalam Sea-ORM entities
- **Modular Architecture**: Setiap domain (karyawan, kantor) memiliki module terpisah
- **Dependency Injection**: Database connection di-inject ke handlers via Axum Extension
- **Error Handling**: Centralized error handling dengan custom response types
- **Clean Code**: Separation of concerns dengan folder structure yang jelas
- **Migration Pattern**: Database schema changes managed via versioned migrations

### Module Structure:
```
├── database.rs        # Database connection layer
├── handlers/          # HTTP layer dengan database operations
├── models/           # Sea-ORM entity layer
├── validators/       # Business logic layer
├── routes/          # Routing layer
├── migration/        # Database schema management
└── main.rs         # Application setup dengan database initialization
```

## 🎯 Features Teruji

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
- ✅ Validation gaji dengan string input
- ✅ Error handling untuk ID invalid
- ✅ Custom validation functions
- ✅ Database constraint validation
- ✅ Relationship queries dengan kantor
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
- ✅ Unit tests untuk validation functions
- ✅ Integration tests untuk semua endpoints
- ✅ Error handling tests
- ✅ Boundary value tests
- ✅ Relationship testing
- ✅ PowerShell test scripts

## 🛠️ Known Issues & Fixes

### Recently Fixed Issues:
1. **✅ Docker Build Issues**: Fixed Rust edition compatibility dan Cargo.lock handling
2. **✅ Route Parameter Syntax**: Changed `{id}` to `:id` untuk proper Axum routing
3. **✅ Variable Shadowing**: Fixed konflik nama variabel dalam handler parameters
4. **✅ Database Migration**: Implemented auto-migration pada container startup
5. **✅ Foreign Key Relations**: Added proper karyawan-kantor relationship

### Current Limitations:
- Database seeding masih manual via init.sql
- Belum ada authentication/authorization system
- Belum ada pagination untuk large datasets
- Belum ada audit logging untuk data changes

## 🚀 Future Enhancements:
- [ ] Authentication & Authorization dengan JWT
- [ ] Pagination dan filtering untuk endpoints
- [ ] Audit logging system
- [ ] API documentation dengan OpenAPI/Swagger
- [ ] Rate limiting dan caching
- [ ] Background job processing
- [ ] Email notifications
- [ ] File upload support untuk avatar karyawan

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
**Version**: 2.1.0  
**Last Updated**: October 29, 2025

## 📁 Additional Documentation

- [DATABASE_SETUP.md](DATABASE_SETUP.md) - Panduan setup database lengkap
- [DOCKER_README.md](DOCKER_README.md) - Panduan Docker deployment lengkap
- [README_NEW.md](README_NEW.md) - Additional project information