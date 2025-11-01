# Database Setup Guide

Panduan untuk setup MySQL database untuk aplikasi Karyawan & Kantor Management API.

## Prerequisites

1. **MySQL Server** sudah terinstall dan berjalan
2. **Rust** dan **Cargo** sudah terinstall
3. **Git** (opsional, untuk version control)

## 🔧 Setup Instructions

### 1. Konfigurasi Database Credentials

Edit file `.env` dan sesuaikan dengan kredensial MySQL Anda:

```env
# Database Configuration
DATABASE_URL=mysql://username:password@localhost:3306/my_axum_db

# Server Configuration  
PORT=8080
HOST=0.0.0.0
```

**Ganti:**
- `username` dengan username MySQL Anda (default: `root`)
- `password` dengan password MySQL Anda
- `localhost:3306` dengan host dan port MySQL jika berbeda

### 2. Buat Database

Login ke MySQL dan buat database:

```sql
mysql -u root -p
CREATE DATABASE my_axum_db;
exit;
```

### 3. Jalankan Migrations

Gunakan PowerShell script yang sudah disediakan:

```powershell
.\setup_database.ps1
```

**Atau jalankan secara manual:**

```powershell
# Set environment variable
$env:DATABASE_URL = "mysql://root:password@localhost:3306/my_axum_db"

# Masuk ke folder migration
cd migration

# Install dependencies
cargo build

# Jalankan migrations
cargo run -- migrate up

# Kembali ke root folder
cd ..
```

### 4. Verifikasi Tabel

Login ke MySQL dan periksa tabel yang terbuat:

```sql
mysql -u root -p my_axum_db

SHOW TABLES;
-- Output yang diharapkan:
-- +------------------------+
-- | Tables_in_my_axum_db   |
-- +------------------------+
-- | jabatan                |
-- | kantor                 |
-- | karyawan               |
-- | seaql_migrations       |
-- | users                  |
-- +------------------------+

DESCRIBE karyawan;
-- +------------+------------+------+-----+-------------------+-------------------+
-- | Field      | Type       | Null | Key | Default           | Extra             |
-- +------------+------------+------+-----+-------------------+-------------------+
-- | id         | int        | NO   | PRI | NULL              | auto_increment    |
-- | nama       | varchar(50)| NO   |     | NULL              |                   |
-- | jabatan_id | int        | NO   | MUL | NULL              |                   |
-- | gaji       | int        | NO   |     | NULL              |                   |
-- | kantor_id  | int        | NO   | MUL | NULL              |                   |
-- | foto       | varchar(255)| YES |     | NULL              |                   |
-- | user_id    | int        | YES  | UNI | NULL              |                   |
-- | created_by | int        | NO   |     | NULL              |                   |
-- | updated_by | int        | NO   |     | NULL              |                   |
-- | created_at | timestamp  | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
-- | updated_at | timestamp  | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
-- +------------+------------+------+-----+-------------------+-------------------+

DESCRIBE jabatan;
-- +------------+--------------+------+-----+-------------------+-------------------+
-- | Field      | Type         | Null | Key | Default           | Extra             |
-- +------------+--------------+------+-----+-------------------+-------------------+
-- | id         | int          | NO   | PRI | NULL              | auto_increment    |
-- | nama       | varchar(100) | NO   |     | NULL              |                   |
-- | deskripsi  | text         | YES  |     | NULL              |                   |
-- | created_by | int          | NO   |     | NULL              |                   |
-- | updated_by | int          | NO   |     | NULL              |                   |
-- | created_at | timestamp    | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
-- | updated_at | timestamp    | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
-- +------------+--------------+------+-----+-------------------+-------------------+

DESCRIBE kantor;
-- +------------+--------------+------+-----+-------------------+-------------------+
-- | Field      | Type         | Null | Key | Default           | Extra             |
-- +------------+--------------+------+-----+-------------------+-------------------+
-- | id         | int          | NO   | PRI | NULL              | auto_increment    |
-- | nama       | varchar(100) | NO   |     | NULL              |                   |
-- | alamat     | varchar(200) | NO   |     | NULL              |                   |
-- | longitude  | decimal(10,7)| NO   |     | NULL              |                   |
-- | latitude   | decimal(10,7)| NO   |     | NULL              |                   |
-- | created_by | int          | NO   |     | NULL              |                   |
-- | updated_by | int          | NO   |     | NULL              |                   |
-- | created_at | timestamp    | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
-- | updated_at | timestamp    | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
-- +------------+--------------+------+-----+-------------------+-------------------+
```

## 🚀 Menjalankan Aplikasi

Setelah database setup berhasil:

```powershell
# Jalankan aplikasi
cargo run
```

Output yang diharapkan:
```
🔌 Connecting to database: mysql://***:***@localhost:3306/my_axum_db
✅ Database connected successfully
🚀 Server running on http://0.0.0.0:8080
```

## 📊 Test Database Operations

### Test Karyawan API:

```powershell
# GET all karyawans (should return empty array initially)
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans -UseBasicParsing

# POST create new karyawan
$body = '{"nama":"John Doe","jabatan_id":"1","gaji":"8000000","kantor_id":"1"}'
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans -Method POST -Body $body -ContentType "application/json" -UseBasicParsing

# GET karyawan by ID
Invoke-WebRequest -Uri http://localhost:8080/api/karyawans/1 -UseBasicParsing
```

### Test Jabatan API:

```powershell
# GET all jabatans (should return empty array initially)
Invoke-WebRequest -Uri http://localhost:8080/api/jabatans -UseBasicParsing

# POST create new jabatan
$body = '{"nama":"Software Engineer","deskripsi":"Develops and maintains software applications"}'
Invoke-WebRequest -Uri http://localhost:8080/api/jabatans -Method POST -Body $body -ContentType "application/json" -UseBasicParsing

# GET jabatan by ID
Invoke-WebRequest -Uri http://localhost:8080/api/jabatans/1 -UseBasicParsing
```

### Test Kantor API:

```powershell
# GET all kantors (should return empty array initially)
Invoke-WebRequest -Uri http://localhost:8080/api/kantors -UseBasicParsing

# POST create new kantor
$body = '{"nama":"Kantor Pusat","alamat":"Jl. Merdeka No.1","longitude":106.827153,"latitude":-6.175110}'
Invoke-WebRequest -Uri http://localhost:8080/api/kantors -Method POST -Body $body -ContentType "application/json" -UseBasicParsing

# GET kantor by ID
Invoke-WebRequest -Uri http://localhost:8080/api/kantors/1 -UseBasicParsing
```

## 🛠️ Troubleshooting

### Error: "Failed to connect to database"

1. **Check MySQL service:**
   ```powershell
   # Windows - check if MySQL service is running
   Get-Service | Where-Object {$_.Name -like "*mysql*"}
   ```

2. **Check credentials:**
   - Pastikan username/password di `.env` benar
   - Test koneksi manual: `mysql -u root -p`

3. **Check database exists:**
   ```sql
   SHOW DATABASES;
   ```

### Error: "Database does not exist"

```sql
CREATE DATABASE my_axum_db;
```

### Error: "Table doesn't exist"

Re-run migrations:
```powershell
cd migration
cargo run -- migrate refresh
cd ..
```

### Error: "Access denied"

1. Create MySQL user with proper permissions:
   ```sql
   CREATE USER 'axum_user'@'localhost' IDENTIFIED BY 'secure_password';
   GRANT ALL PRIVILEGES ON my_axum_db.* TO 'axum_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. Update `.env` with new credentials:
   ```env
   DATABASE_URL=mysql://axum_user:secure_password@localhost:3306/my_axum_db
   ```

## 📝 Migration Commands

```powershell
cd migration

# Check migration status
cargo run -- migrate status

# Run all pending migrations
cargo run -- migrate up

# Rollback last migration
cargo run -- migrate down

# Rollback all migrations
cargo run -- migrate reset

# Fresh start (reset + up)
cargo run -- migrate refresh
```

## 🔍 Database Schema

### Jabatan Table:
- `id`: Primary key, auto-increment
- `nama`: VARCHAR(100), job position name
- `deskripsi`: TEXT, job position description (optional)
- `created_by`: INT, user who created the record
- `updated_by`: INT, user who last updated the record
- `created_at`: TIMESTAMP, creation time
- `updated_at`: TIMESTAMP, last update time

### Karyawan Table:
- `id`: Primary key, auto-increment
- `nama`: VARCHAR(50), employee name
- `jabatan_id`: INT, foreign key to jabatan table
- `gaji`: INT, salary amount
- `kantor_id`: INT, foreign key to kantor table
- `foto`: VARCHAR(255), photo filename (optional)
- `user_id`: INT, foreign key to users table (optional)
- `created_by`: INT, user who created the record
- `updated_by`: INT, user who last updated the record
- `created_at`: TIMESTAMP, creation time
- `updated_at`: TIMESTAMP, last update time

### Kantor Table:
- `id`: Primary key, auto-increment
- `nama`: VARCHAR(100), office name
- `alamat`: VARCHAR(200), office address
- `longitude`: DECIMAL(10,7), geographic longitude
- `latitude`: DECIMAL(10,7), geographic latitude
- `created_by`: INT, user who created the record
- `updated_by`: INT, user who last updated the record
- `created_at`: TIMESTAMP, creation time
- `updated_at`: TIMESTAMP, last update time

## 🎯 Features

✅ **Full CRUD Operations** untuk semua tabel (jabatan, karyawan, kantor, users)
✅ **Relational Database Design** dengan foreign key constraints
✅ **Job Position Management** dengan tabel jabatan terpisah
✅ **User Authentication & Authorization** dengan JWT
✅ **User Tracking** untuk audit trail (created_by, updated_by)
✅ **Photo Upload** untuk karyawan dengan validasi file
✅ **Data Validation** dengan custom validators
✅ **Auto-generated timestamps** 
✅ **Geographic coordinate validation**
✅ **Proper error handling** dengan JSON responses
✅ **Database connection pooling**
✅ **Migration system** untuk schema management

---

**Catatan:** Pastikan MySQL server berjalan sebelum menjalankan aplikasi. Database akan otomatis diinisialisasi dengan migrations.