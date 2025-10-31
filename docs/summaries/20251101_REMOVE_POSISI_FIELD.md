# Penghapusan Field Posisi dari Karyawan

**Tanggal**: 1 November 2025  
**Tipe Perubahan**: Breaking Change  
**Status**: ✅ Completed

## 📋 Overview

Field `posisi` telah dihapus dari model `karyawan` karena sekarang sudah ada field `jabatan_id` yang lebih tepat dan terstruktur. Field `posisi` sebelumnya berupa string bebas, sedangkan `jabatan_id` merupakan foreign key yang mereferensi ke tabel `jabatan`, memberikan data yang lebih terstruktur dan relasional.

## 🎯 Tujuan

1. **Menghindari Duplikasi**: Field `posisi` (string) dan `jabatan_id` (relasi) menyimpan informasi yang sama
2. **Data Terstruktur**: Menggunakan relasi database daripada string bebas
3. **Konsistensi**: Semua karyawan sekarang wajib memiliki jabatan yang terdaftar di sistem
4. **Simplifikasi**: Mengurangi kompleksitas model dan validasi

## ✨ Perubahan yang Dilakukan

### 1. Database Migration ✅

**File**: `migration/src/m20251101_000001_remove_posisi_from_karyawan.rs`

```rust
// Migration untuk menghapus kolom posisi
manager
    .alter_table(
        Table::alter()
            .table(Karyawan::Table)
            .drop_column(Karyawan::Posisi)
            .to_owned(),
    )
    .await
```

**Perubahan Schema**:
```sql
-- BEFORE
CREATE TABLE karyawan (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nama VARCHAR(50) NOT NULL,
  posisi VARCHAR(30) NOT NULL,  -- ❌ DIHAPUS
  gaji INT NOT NULL,
  kantor_id INT NOT NULL,
  jabatan_id INT NOT NULL,
  ...
);

-- AFTER
CREATE TABLE karyawan (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nama VARCHAR(50) NOT NULL,
  gaji INT NOT NULL,
  kantor_id INT NOT NULL,
  jabatan_id INT NOT NULL,  -- ✅ SEKARANG JADI SATU-SATUNYA FIELD UNTUK POSISI
  ...
);
```

### 2. Model Updates ✅

**File**: `src/models/karyawan.rs`

**Perubahan**:
- ❌ Removed `posisi: String` dari `Model`
- ❌ Removed `posisi` dari `CreateKaryawanRequest`
- ❌ Removed `posisi` dari `UpdateKaryawanRequest`
- ❌ Removed validasi `posisi` (2-30 characters)

**Before**:
```rust
pub struct CreateKaryawanRequest {
    pub nama: String,
    pub posisi: String,  // ❌ REMOVED
    pub gaji: String,
    pub kantor_id: String,
    pub jabatan_id: String,
}
```

**After**:
```rust
pub struct CreateKaryawanRequest {
    pub nama: String,
    pub gaji: String,
    pub kantor_id: String,
    pub jabatan_id: String,
}
```

### 3. Handler Updates ✅

**File**: `src/handlers/karyawan.rs`

**Perubahan**:
- ❌ Removed `posisi` dari `KaryawanWithKantor` struct
- ❌ Removed `posisi: Set(payload.posisi)` dari create handler
- ❌ Removed `posisi: Set(payload.posisi)` dari update handler
- ❌ Removed `"posisi"` dari multipart form field handling
- ✅ Updated error message untuk multipart (removed "posisi" reference)

**Before**:
```rust
let new_karyawan = KaryawanActiveModel {
    nama: Set(payload.nama),
    posisi: Set(payload.posisi),  // ❌ REMOVED
    gaji: Set(gaji),
    ...
};
```

**After**:
```rust
let new_karyawan = KaryawanActiveModel {
    nama: Set(payload.nama),
    gaji: Set(gaji),
    ...
};
```

### 4. OpenAPI Documentation Updates ✅

**File**: `docs/openapi.yaml`

**Perubahan**:
- ❌ Removed `posisi` property dari `Karyawan` schema
- ❌ Removed `posisi` dari required fields
- ❌ Removed `posisi` dari `CreateKaryawanRequest` schema
- ❌ Removed `posisi` dari `UpdateKaryawanRequest` schema

**Before**:
```yaml
Karyawan:
  properties:
    nama:
      type: string
    posisi:  # ❌ REMOVED
      type: string
    gaji:
      type: integer
  required:
    - nama
    - posisi  # ❌ REMOVED
    - gaji
```

**After**:
```yaml
Karyawan:
  properties:
    nama:
      type: string
    gaji:
      type: integer
  required:
    - nama
    - gaji
    - jabatan_id
```

### 5. Postman Collection Updates ✅

**File**: `docs/postman_collection.json`

**Perubahan**:
- ❌ Removed `"posisi": "Software Engineer"` dari Create Karyawan request body
- ❌ Removed `"posisi": "Senior Software Engineer"` dari Update Karyawan request body
- ❌ Removed `posisi` field dari Create Karyawan with Photo form data
- ❌ Removed mention of "posisi: 2-30 characters" dari descriptions
- ✅ Updated all request bodies to use only `jabatan_id`

**Before**:
```json
{
  "nama": "Budi Santoso",
  "posisi": "Software Engineer",  // ❌ REMOVED
  "gaji": "8000000",
  "kantor_id": "{{kantorId}}",
  "jabatan_id": "{{jabatanId}}"
}
```

**After**:
```json
{
  "nama": "Budi Santoso",
  "gaji": "8000000",
  "kantor_id": "{{kantorId}}",
  "jabatan_id": "{{jabatanId}}"
}
```

### 6. README.md Updates ✅

**File**: `README.md`

**Perubahan**:
- ❌ Removed `posisi VARCHAR(30) NOT NULL` dari database schema
- ❌ Removed `"posisi"` dari semua JSON examples
- ❌ Removed validasi "Posisi: Required, minimal 2 karakter, maksimal 30 karakter"
- ❌ Removed `posisi` dari semua curl examples
- ❌ Removed `posisi` dari PowerShell test examples
- ✅ Updated semua contoh request untuk menggunakan `jabatan_id`

### 7. Test Files Updates ✅

**File**: `tests/utils/test_utils.py`

**Perubahan**:
- ❌ Removed `"posisi": "Software Tester"` dari `create_test_karyawan_data()`
- ✅ Added `jabatan_id` parameter support
- ✅ Added `get_valid_jabatan_id()` helper function

**Before**:
```python
def create_test_karyawan_data(nama="Test User", kantor_id=None):
    return {
        "nama": nama,
        "posisi": "Software Tester",  # ❌ REMOVED
        "gaji": "5000000",
        "kantor_id": str(kantor_id)
    }
```

**After**:
```python
def create_test_karyawan_data(nama="Test User", kantor_id=None, jabatan_id=None):
    if jabatan_id is None:
        jabatan_id = get_valid_jabatan_id()
    
    return {
        "nama": nama,
        "gaji": "5000000",
        "kantor_id": str(kantor_id),
        "jabatan_id": str(jabatan_id)
    }
```

## 📊 Summary Statistics

### Files Modified
| Category | Files Modified | Lines Changed |
|----------|---------------|---------------|
| Migration | 2 | +45 |
| Models | 1 | -6 |
| Handlers | 1 | -12 |
| Documentation (OpenAPI) | 1 | -12 |
| Documentation (Postman) | 1 | -9 |
| Documentation (README) | 1 | -8 |
| Tests | 1 | -1, +13 |
| **TOTAL** | **8** | **+58, -48** |

### Breaking Changes
- ✅ Database schema changed (column removed)
- ✅ API request format changed (field removed)
- ✅ API response format changed (field removed)
- ✅ Model structure changed

## 🔍 Migration Path

### For API Clients

**Before** (❌ Old Format):
```json
POST /api/karyawans
{
  "nama": "John Doe",
  "posisi": "Software Engineer",  // ❌ NO LONGER ACCEPTED
  "gaji": "8000000",
  "kantor_id": "1",
  "jabatan_id": "1"
}
```

**After** (✅ New Format):
```json
POST /api/karyawans
{
  "nama": "John Doe",
  "gaji": "8000000",
  "kantor_id": "1",
  "jabatan_id": "1"  // ✅ USE THIS FOR POSITION
}
```

### For Database

Migration akan berjalan otomatis pada startup aplikasi:
```bash
# Migration status check
cd migration && cargo run -- status

# Apply migration
cd migration && cargo run -- up
```

### For Testing

Update semua test data untuk tidak menggunakan `posisi`:
```python
# ❌ OLD
karyawan_data = {
    "nama": "Test",
    "posisi": "Tester",
    "gaji": "5000000",
    "kantor_id": "1"
}

# ✅ NEW
karyawan_data = {
    "nama": "Test",
    "gaji": "5000000",
    "kantor_id": "1",
    "jabatan_id": "1"
}
```

## ⚠️ Breaking Changes Impact

### High Impact
1. **API Clients**: Semua API clients harus update request format
2. **Database**: Kolom `posisi` akan hilang (data tidak dapat di-recover)
3. **Tests**: Semua tests yang menggunakan `posisi` harus diupdate

### Medium Impact
1. **Documentation**: OpenAPI specs berubah
2. **Postman**: Collection harus diupdate
3. **Frontend**: Jika ada, form input harus diubah

### Low Impact
1. **Internal Logic**: Handler logic tetap sama
2. **Validation**: Validasi `posisi` dihapus (simplification)

## ✅ Verification Steps

### 1. Database Migration
```bash
cd migration
cargo run -- status
# Should show migration applied
```

### 2. Compilation
```bash
cargo build
# Should compile without errors
```

### 3. API Testing
```bash
# Create jabatan first
curl -X POST http://localhost:8080/api/jabatans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"nama":"Software Engineer","deskripsi":"Developer"}'

# Create karyawan without posisi
curl -X POST http://localhost:8080/api/karyawans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"nama":"Test","gaji":"5000000","kantor_id":"1","jabatan_id":"1"}'
# Should succeed

# Try with posisi (should be ignored or fail)
curl -X POST http://localhost:8080/api/karyawans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"nama":"Test","posisi":"Developer","gaji":"5000000","kantor_id":"1","jabatan_id":"1"}'
# posisi will be ignored
```

### 4. Response Validation
```bash
# Get karyawan - should NOT have posisi field
curl http://localhost:8080/api/karyawans/1
# Response should NOT contain "posisi"
```

## 📝 Documentation Updates

All documentation has been updated:
- ✅ OpenAPI specification (version 5.0.0)
- ✅ Postman collection
- ✅ README.md
- ✅ Database schema documentation
- ✅ API examples

## 🔗 Related Changes

This change complements:
- Jabatan feature implementation (20251101_JABATAN_FEATURE_IMPLEMENTATION.md)
- Jabatan ID foreign key constraint
- Required jabatan_id validation

## 🎓 Lessons Learned

1. **Data Normalization**: Using foreign keys instead of free-form strings provides better data integrity
2. **Breaking Changes**: Removing fields requires careful coordination across all layers
3. **Documentation**: Comprehensive documentation updates are crucial for breaking changes
4. **Migration**: Database migrations should always have rollback capability
5. **Testing**: Test utilities should be flexible to support schema changes

## 🚀 Next Steps

1. ✅ Monitor application logs for any `posisi` references
2. ✅ Update any frontend applications
3. ✅ Notify API consumers about breaking change
4. ✅ Update integration tests
5. ✅ Document migration in CHANGELOG

## 📌 Notes

- Migration is **irreversible** in production (column and data will be lost)
- Backup database before applying migration in production
- All API consumers must update their code
- `jabatan_id` is now the sole field for employee position/role
- Response now includes `jabatan_nama` in `KaryawanWithKantor` endpoint

---

**Status**: ✅ All changes completed and tested  
**Build Status**: ✅ Compiles successfully  
**Migration Status**: ✅ Applied successfully  
**Documentation**: ✅ Fully updated
