# Karyawan & Kantor Management API

REST API untuk manajemen data karyawan dan kantor yang dibangun dengan Rust dan Axum framework.

## ✨ Fitur

- **CRUD Operations**: Create, Read, Update, Delete untuk karyawan dan kantor
- **Data Validation**: Validasi komprehensif untuk semua input data
- **JSON Responses**: Response API yang konsisten dalam format JSON
- **Error Handling**: Penanganan error yang informatif
- **Clean Architecture**: Struktur kode yang terorganisir dengan baik
- **Geographic Validation**: Validasi koordinat longitude dan latitude untuk kantor

## 🚀 Teknologi

- **Rust**: Bahasa pemrograman utama
- **Axum 0.8.6**: Modern web framework untuk Rust
- **Serde**: JSON serialization/deserialization
- **Validator**: Data validation dengan derive macros
- **Tokio**: Async runtime

## 📁 Struktur Project

```
src/
├── main.rs                 # Entry point aplikasi
├── handlers/               # HTTP request handlers
│   ├── mod.rs
│   ├── health.rs          # Health check handler
│   ├── karyawan.rs        # CRUD handlers untuk karyawan
│   └── kantor.rs          # CRUD handlers untuk kantor
├── models/                 # Data structures
│   ├── mod.rs
│   ├── common.rs          # Shared response models (ApiResponse)
│   ├── karyawan.rs        # Karyawan model & request DTOs
│   └── kantor.rs          # Kantor model & request DTOs
├── routes/                 # Route definitions
│   ├── mod.rs
│   ├── karyawan.rs        # Karyawan routes
│   └── kantor.rs          # Kantor routes
└── validators/             # Custom validation logic
    ├── mod.rs
    ├── karyawan.rs        # Karyawan validation functions
    └── kantor.rs          # Kantor validation functions
```

## 🛠️ Instalasi & Menjalankan

### Prerequisites
- Rust (1.70+)
- Cargo

### Steps

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd my-axum-app
   ```

2. **Install dependencies**
   ```bash
   cargo build
   ```

3. **Jalankan aplikasi**
   ```bash
   cargo run
   ```

   Server akan berjalan di: `http://localhost:8080`

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
| GET | `/api/karyawans/{id}` | Dapatkan karyawan berdasarkan ID |
| POST | `/api/karyawans` | Buat karyawan baru |
| PUT | `/api/karyawans/{id}` | Update karyawan |
| DELETE | `/api/karyawans/{id}` | Hapus karyawan |

#### Kantor Management
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/kantors` | Dapatkan semua kantor |
| GET | `/api/kantors/{id}` | Dapatkan kantor berdasarkan ID |
| POST | `/api/kantors` | Buat kantor baru |
| PUT | `/api/kantors/{id}` | Update kantor |
| DELETE | `/api/kantors/{id}` | Hapus kantor |

## 📝 Request/Response Format

### Karyawan Model
```json
{
  "id": 1,
  "nama": "Budi Santoso",
  "posisi": "Software Engineer", 
  "gaji": 8000000
}
```

### Kantor Model
```json
{
  "id": 1,
  "nama": "Kantor Pusat",
  "alamat": "Jl. Merdeka No.1, Jakarta",
  "longitude": 106.827153,
  "latitude": -6.175110
}
```

### Create Karyawan Request
```json
{
  "nama": "Nama Karyawan",
  "posisi": "Posisi Jabatan",
  "gaji": "8000000"
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
  - Maksimal 50,000,000 (50 juta)
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

### Manual Testing dengan PowerShell

**Test Karyawan:**
```powershell
# Get all karyawans
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans -UseBasicParsing

# Create new karyawan
$body = '{"nama":"John Doe","posisi":"Developer","gaji":"8000000"}'
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
curl -X POST http://localhost:8080/api/karyawans \
  -H "Content-Type: application/json" \
  -d '{"nama":"Jane Doe","posisi":"Manager","gaji":"12000000"}'

# Test kantor endpoints
curl http://localhost:8080/api/kantors
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

## 📖 Arsitektur

### Separation of Concerns:
- **Handlers**: Menangani HTTP requests dan responses
- **Models**: Data structures dan business logic  
- **Validators**: Custom validation logic
- **Routes**: Definisi routing yang terpisah dari main.rs

### Design Patterns:
- **Modular Architecture**: Setiap domain (karyawan, kantor) memiliki module terpisah
- **Dependency Injection**: Menggunakan Axum's dependency injection
- **Error Handling**: Centralized error handling dengan custom response types
- **Clean Code**: Separation of concerns dengan folder structure yang jelas

### Module Structure:
```
├── handlers/          # HTTP layer
├── models/           # Data layer
├── validators/       # Business logic layer
├── routes/          # Routing layer
└── main.rs         # Application setup
```

## 🎯 Features Teruji

### Karyawan Management:
- ✅ CRUD operations lengkap
- ✅ Validation gaji dengan string input
- ✅ Error handling untuk ID invalid
- ✅ Custom validation functions

### Kantor Management:
- ✅ CRUD operations lengkap
- ✅ Geographic coordinate validation
- ✅ Boundary value testing (-180/180, -90/90)
- ✅ Address dan nama validation

### Testing Coverage:
- ✅ Unit tests untuk validation functions
- ✅ Integration tests untuk semua endpoints
- ✅ Error handling tests
- ✅ Boundary value tests

## 🤝 Contributing

1. Fork repository
2. Buat feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buat Pull Request

## 📄 License

MIT License - lihat file LICENSE untuk detail lengkap.

---

**Author**: [Your Name]  
**Version**: 2.0.0  
**Last Updated**: October 2025