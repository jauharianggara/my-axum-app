# Karyawan Management API

REST API untuk manajemen data karyawan yang dibangun dengan Rust dan Axum framework.

## ✨ Fitur

- **CRUD Operations**: Create, Read, Update, Delete karyawan
- **Data Validation**: Validasi komprehensif untuk semua input data
- **JSON Responses**: Response API yang konsisten dalam format JSON
- **Error Handling**: Penanganan error yang informatif
- **Clean Architecture**: Struktur kode yang terorganisir dengan baik

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
│   └── karyawan/
│       └── mod.rs         # CRUD handlers untuk karyawan
├── models/                 # Data structures
│   ├── mod.rs
│   ├── common.rs          # Shared response models
│   └── karyawan/
│       └── mod.rs         # Karyawan model & request DTOs
├── routes/                 # Route definitions
│   ├── mod.rs
│   └── karyawan.rs        # Karyawan routes
└── validators/             # Custom validation logic
    ├── mod.rs
    └── karyawan/
        └── mod.rs         # Karyawan validation functions
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

   Server akan berjalan di: `http://localhost:3000`

## 📚 API Endpoints

### Base URL: `http://localhost:3000`

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| GET | `/api/karyawans` | Dapatkan semua karyawan |
| GET | `/api/karyawans/{id}` | Dapatkan karyawan berdasarkan ID |
| POST | `/api/karyawans` | Buat karyawan baru |
| PUT | `/api/karyawans/{id}` | Update karyawan |
| DELETE | `/api/karyawans/{id}` | Hapus karyawan |

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

### Create/Update Request
```json
{
  "nama": "Nama Karyawan",
  "posisi": "Posisi Jabatan",
  "gaji": "8000000"
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

### Validasi yang Diterapkan:
- **Nama**: Required, minimal 2 karakter
- **Posisi**: Required, minimal 2 karakter 
- **Gaji**: 
  - Required
  - Harus berupa string yang bisa dikonversi ke angka
  - Minimal 1,000,000 (1 juta)
  - Maksimal 50,000,000 (50 juta)
- **ID**: Harus berupa angka positif yang valid

### Contoh Error Validasi:
```json
{
  "success": false,
  "message": "Validation failed",
  "data": null,
  "errors": [
    "gaji: Gaji harus antara 1000000 dan 50000000"
  ]
}
```

## 🧪 Testing

### Manual Testing dengan PowerShell

1. **Test semua endpoint:**
   ```powershell
   # Get all karyawans
   Invoke-WebRequest -Uri http://localhost:3000/api/karyawans -UseBasicParsing
   
   # Get karyawan by ID
   Invoke-WebRequest -Uri http://localhost:3000/api/karyawans/1 -UseBasicParsing
   
   # Create new karyawan
   $body = '{"nama":"John Doe","posisi":"Developer","gaji":"8000000"}'
   Invoke-WebRequest -Uri http://localhost:3000/api/karyawans -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
   ```

2. **Test validasi:**
   ```powershell
   # Invalid gaji
   $body = '{"nama":"Test","posisi":"Tester","gaji":"abc"}'
   Invoke-WebRequest -Uri http://localhost:3000/api/karyawans -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
   ```

### Menggunakan curl (jika tersedia):
```bash
# Test endpoints
curl http://localhost:3000/api/karyawans
curl http://localhost:3000/api/karyawans/1
curl -X POST http://localhost:3000/api/karyawans \
  -H "Content-Type: application/json" \
  -d '{"nama":"Jane Doe","posisi":"Manager","gaji":"12000000"}'
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
- **Modular Architecture**: Setiap domain (karyawan) memiliki module terpisah
- **Dependency Injection**: Menggunakan Axum's dependency injection
- **Error Handling**: Centralized error handling dengan custom response types

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
**Version**: 1.0.0  
**Last Updated**: November 2024