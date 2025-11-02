# Request Logging Guide

Dokumentasi lengkap untuk request logging di Axum API.

## 📋 Tipe Logger yang Tersedia

### 1️⃣ **request_logger** (Detailed Logging) - AKTIF
Logger utama yang saat ini digunakan. Menampilkan informasi lengkap untuk setiap request.

**Output Format:**
```
╔═══════════════════════════════════════════════════════════════
║ 📥 INCOMING REQUEST
╠═══════════════════════════════════════════════════════════════
║ ⏰ Time       : 2025-11-02 15:30:45.123
║ 🌐 IP         : 192.168.1.100 (Socket: 192.168.1.100:54321)
║ 📍 Method     : GET
║ 🔗 Path       : /api/karyawans
║ ❓ Query      : page=1&limit=10
║ 📡 Protocol   : HTTP/1.1
║ 🔖 Origin     : http://localhost:3000
║ 📄 Content    : application/json
║ 🔍 User-Agent : Mozilla/5.0 ...
║ 🔗 Referer    : http://localhost:3000/dashboard
╠═══════════════════════════════════════════════════════════════
║ 📤 RESPONSE
╠═══════════════════════════════════════════════════════════════
║ ✅ Status     : 200 OK (SUCCESS)
║ ⏱️  Duration   : 45 ms
╚═══════════════════════════════════════════════════════════════
```

**Informasi yang Dicatat:**
- ⏰ Timestamp lengkap (sampai milidetik)
- 🌐 IP Address (client IP dan socket address)
- 📍 HTTP Method (GET, POST, PUT, DELETE, OPTIONS)
- 🔗 Request Path
- ❓ Query Parameters (jika ada)
- 📡 HTTP Protocol Version
- 🔖 Origin header (untuk CORS)
- 📄 Content-Type
- 🔍 User-Agent
- 🔗 Referer (jika ada)
- ✅ Response Status Code
- ⏱️  Response Time (dalam milidetik)

**Status Code Indicators:**
- ✅ 200-299: SUCCESS (hijau)
- 🔄 300-399: REDIRECT (biru)
- ⚠️  400-499: CLIENT ERROR (kuning)
- ❌ 500-599: SERVER ERROR (merah)
- ℹ️  Lainnya: INFO

### 2️⃣ **simple_request_logger** (Single Line)
Logger ringkas dalam satu baris (seperti Apache access log).

**Output Format:**
```
✅ [2025-11-02 15:30:45] 192.168.1.100 GET /api/karyawans - 200 (45 ms)
⚠️ [2025-11-02 15:31:12] 192.168.1.101 POST /api/auth/login - 401 (12 ms)
❌ [2025-11-02 15:32:05] 192.168.1.102 GET /api/invalid - 500 (89 ms)
```

**Cara Mengaktifkan:**
Edit `src/main.rs`, ganti:
```rust
.layer(from_fn(request_logger))
```
Menjadi:
```rust
.layer(from_fn(simple_request_logger))
```

### 3️⃣ **error_request_logger** (Errors Only)
Hanya mencatat request yang gagal (4xx dan 5xx).

**Output Format:**
```
❌ ERROR [2025-11-02 15:35:20] 192.168.1.100 GET /api/karyawans - 401
❌ ERROR [2025-11-02 15:35:45] 192.168.1.101 POST /api/karyawans - 500
```

**Cara Mengaktifkan:**
Edit `src/main.rs`, ganti:
```rust
.layer(from_fn(request_logger))
```
Menjadi:
```rust
.layer(from_fn(error_request_logger))
```

## 🔧 Konfigurasi

### Lokasi Logger Middleware
File: `src/middleware/logger.rs`

### Aktivasi di Main
File: `src/main.rs`
```rust
// Import logger
use middleware::logger::request_logger;

// Tambahkan layer
.layer(from_fn(request_logger))
```

### Enable ConnectInfo
Agar IP address bisa dicatat, pastikan server menggunakan `into_make_service_with_connect_info`:

```rust
use std::net::SocketAddr;

axum::serve(
    listener,
    app.into_make_service_with_connect_info::<SocketAddr>()
)
.await
.unwrap();
```

## 📊 Informasi yang Dicatat

### IP Address Detection
Logger otomatis mendeteksi IP address dengan prioritas:
1. **X-Forwarded-For** header (untuk reverse proxy)
2. **Socket Address** (direct connection)

Berguna untuk deployment dengan Apache/Nginx reverse proxy.

### Response Time
Diukur dalam milidetik menggunakan `std::time::Instant`.
- Akurasi tinggi untuk performance monitoring
- Otomatis dihitung dari request masuk sampai response keluar

### Headers Detection
- **Origin**: Untuk debugging CORS
- **User-Agent**: Identifikasi client (browser, curl, Postman, dll)
- **Referer**: Untuk tracking request source
- **Content-Type**: Tipe data request

## 🎯 Use Cases

### Development
Gunakan **request_logger** (detailed) untuk:
- ✅ Debugging API issues
- ✅ Understanding request flow
- ✅ CORS troubleshooting
- ✅ Performance monitoring

### Production
Pertimbangkan **simple_request_logger** untuk:
- ✅ Reduced log size
- ✅ Faster I/O
- ✅ Easier log parsing
- ✅ Machine-readable format

Atau **error_request_logger** untuk:
- ✅ Fokus pada errors
- ✅ Minimal disk usage
- ✅ Alert monitoring

## 📝 Contoh Output

### Success Request (GET)
```
╔═══════════════════════════════════════════════════════════════
║ 📥 INCOMING REQUEST
╠═══════════════════════════════════════════════════════════════
║ ⏰ Time       : 2025-11-02 10:30:15.456
║ 🌐 IP         : 127.0.0.1 (Socket: 127.0.0.1:52341)
║ 📍 Method     : GET
║ 🔗 Path       : /api/karyawans
║ 📡 Protocol   : HTTP/1.1
║ 🔖 Origin     : -
║ 📄 Content    : -
║ 🔍 User-Agent : curl/7.68.0
╠═══════════════════════════════════════════════════════════════
║ 📤 RESPONSE
╠═══════════════════════════════════════════════════════════════
║ ✅ Status     : 200 OK (SUCCESS)
║ ⏱️  Duration   : 23 ms
╚═══════════════════════════════════════════════════════════════
```

### Failed Request (POST)
```
╔═══════════════════════════════════════════════════════════════
║ 📥 INCOMING REQUEST
╠═══════════════════════════════════════════════════════════════
║ ⏰ Time       : 2025-11-02 10:31:22.789
║ 🌐 IP         : 192.168.1.50 (Socket: 192.168.1.50:45678)
║ 📍 Method     : POST
║ 🔗 Path       : /api/auth/login
║ 📡 Protocol   : HTTP/1.1
║ 🔖 Origin     : http://localhost:3000
║ 📄 Content    : application/json
║ 🔍 User-Agent : Mozilla/5.0 (Windows NT 10.0; Win64)
╠═══════════════════════════════════════════════════════════════
║ 📤 RESPONSE
╠═══════════════════════════════════════════════════════════════
║ ⚠️  Status     : 401 Unauthorized (CLIENT ERROR)
║ ⏱️  Duration   : 15 ms
╚═══════════════════════════════════════════════════════════════
```

### CORS Preflight (OPTIONS)
```
╔═══════════════════════════════════════════════════════════════
║ 📥 INCOMING REQUEST
╠═══════════════════════════════════════════════════════════════
║ ⏰ Time       : 2025-11-02 10:32:01.123
║ 🌐 IP         : 192.168.1.100 (Socket: 192.168.1.100:34567)
║ 📍 Method     : OPTIONS
║ 🔗 Path       : /api/karyawans
║ 📡 Protocol   : HTTP/1.1
║ 🔖 Origin     : http://nextjs.synergyinfinity.id
║ 📄 Content    : -
║ 🔍 User-Agent : Mozilla/5.0 (Chrome)
╠═══════════════════════════════════════════════════════════════
║ 📤 RESPONSE
╠═══════════════════════════════════════════════════════════════
║ ✅ Status     : 204 No Content (SUCCESS)
║ ⏱️  Duration   : 2 ms
╚═══════════════════════════════════════════════════════════════
```

## 🔍 Log Analysis

### Viewing Logs
Server logs ditampilkan di stdout (terminal). Untuk menyimpan ke file:

**Windows PowerShell:**
```powershell
cargo run 2>&1 | Tee-Object -FilePath logs/server.log
```

**Linux/Mac:**
```bash
cargo run 2>&1 | tee logs/server.log
```

### Filtering Logs
**Hanya errors:**
```powershell
cargo run 2>&1 | Select-String "ERROR"
```

**Hanya success:**
```powershell
cargo run 2>&1 | Select-String "SUCCESS"
```

**Specific path:**
```powershell
cargo run 2>&1 | Select-String "/api/karyawans"
```

### Performance Analysis
Untuk menganalisa response time:
```powershell
# Cari request yang lambat (>1000ms)
Get-Content server.log | Select-String "Duration.*[1-9]\d{3,} ms"
```

## 🎨 Customization

### Menambah Informasi Baru
Edit `src/middleware/logger.rs`, tambahkan di section "Extract request information":

```rust
// Contoh: Log request body size
let content_length = request
    .headers()
    .get("content-length")
    .and_then(|v| v.to_str().ok())
    .unwrap_or("0");

println!("║ 📦 Size       : {} bytes", content_length);
```

### Mengubah Format Output
Modify fungsi `request_logger` untuk custom format:
- Ubah emoji
- Ubah warna (di terminal yang support ANSI)
- Ubah layout box
- Tambah/kurangi informasi

### Integrasi dengan Log File
Untuk production, consider using logging framework:

**Tambah dependency di Cargo.toml:**
```toml
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

**Ganti println! dengan tracing:**
```rust
use tracing::{info, warn, error};

info!("Request from {} to {}", client_ip, path);
warn!("Slow response: {} ms", duration_ms);
error!("Request failed: {}", status_code);
```

## 🚀 Best Practices

### Development
- ✅ Gunakan detailed logger
- ✅ Monitor semua requests
- ✅ Check response times
- ✅ Debug CORS issues

### Staging
- ✅ Gunakan simple logger
- ✅ Log ke file
- ✅ Rotate logs daily
- ✅ Monitor errors khusus

### Production
- ✅ Gunakan simple atau error logger
- ✅ Log ke external service (ELK, CloudWatch)
- ✅ Set log retention policy
- ✅ Monitor anomali

## 📚 Resources

- Logger middleware: `src/middleware/logger.rs`
- Main configuration: `src/main.rs`
- Axum middleware docs: https://docs.rs/axum/latest/axum/middleware/
- Tower middleware: https://docs.rs/tower/latest/tower/
