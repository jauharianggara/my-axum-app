# User Tracking Implementation Summary

**Date**: October 31, 2025  
**Feature**: User Tracking in Karyawan Table

## 📋 Overview

Implementasi sistem tracking untuk mencatat user yang membuat dan mengupdate data karyawan. Setiap record karyawan sekarang menyimpan informasi `created_by` dan `updated_by` yang mereferensi ke user yang sedang login.

## 🎯 Objectives

1. ✅ Track user yang membuat karyawan baru
2. ✅ Track user yang mengupdate data karyawan
3. ✅ Maintain referential integrity dengan foreign key constraints
4. ✅ Automatic update saat create/update operations
5. ✅ Include user tracking info dalam API responses

## 🔧 Implementation Details

### 1. Database Migration

**File**: `migration/src/m20251031_095022_add_user_tracking_to_karyawan.rs`

Added two new columns to `karyawan` table:
- `created_by` (INTEGER, nullable) - References users.id
- `updated_by` (INTEGER, nullable) - References users.id

**Foreign Key Constraints**:
- `fk_karyawan_created_by`: ON DELETE SET NULL, ON UPDATE CASCADE
- `fk_karyawan_updated_by`: ON DELETE SET NULL, ON UPDATE CASCADE

```sql
-- Equivalent SQL
ALTER TABLE karyawan 
  ADD COLUMN created_by INTEGER NULL,
  ADD COLUMN updated_by INTEGER NULL;

ALTER TABLE karyawan
  ADD CONSTRAINT fk_karyawan_created_by 
  FOREIGN KEY (created_by) REFERENCES users(id)
  ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE karyawan
  ADD CONSTRAINT fk_karyawan_updated_by 
  FOREIGN KEY (updated_by) REFERENCES users(id)
  ON DELETE SET NULL ON UPDATE CASCADE;
```

### 2. Model Updates

**File**: `src/models/karyawan.rs`

Updated `Model` struct:
```rust
pub struct Model {
    pub id: i32,
    pub nama: String,
    pub posisi: String,
    pub gaji: i32,
    pub kantor_id: i32,
    pub foto_path: Option<String>,
    pub foto_original_name: Option<String>,
    pub foto_size: Option<i64>,
    pub foto_mime_type: Option<String>,
    pub created_by: Option<i32>,      // NEW
    pub updated_by: Option<i32>,      // NEW
    pub created_at: DateTimeWithTimeZone,
    pub updated_at: DateTimeWithTimeZone,
}
```

Updated `Relation` enum to include user relationships:
```rust
pub enum Relation {
    Kantor,
    CreatedByUser,    // NEW
    UpdatedByUser,    // NEW
}
```

### 3. Handler Updates

**File**: `src/handlers/karyawan.rs`

All create/update handlers now extract the authenticated user and set tracking fields:

#### create_karyawan
```rust
pub async fn create_karyawan(
    State(db): State<DatabaseConnection>,
    Extension(user): Extension<User>,  // Extract authenticated user
    ExtractJson(payload): ExtractJson<CreateKaryawanRequest>,
) -> Json<ApiResponse<Karyawan>> {
    let new_karyawan = KaryawanActiveModel {
        nama: Set(payload.nama),
        posisi: Set(payload.posisi),
        gaji: Set(gaji),
        kantor_id: Set(kantor_id),
        created_by: Set(Some(user.id)),    // Set created_by
        updated_by: Set(Some(user.id)),    // Set updated_by
        // ... other fields
    };
}
```

#### update_karyawan
```rust
pub async fn update_karyawan(
    Path(id_str): Path<String>,
    State(db): State<DatabaseConnection>,
    Extension(user): Extension<User>,  // Extract authenticated user
    ExtractJson(payload): ExtractJson<UpdateKaryawanRequest>,
) -> Json<ApiResponse<Karyawan>> {
    let mut updated_karyawan: KaryawanActiveModel = existing_karyawan.into();
    updated_karyawan.nama = Set(payload.nama);
    updated_karyawan.posisi = Set(payload.posisi);
    updated_karyawan.gaji = Set(gaji);
    updated_karyawan.kantor_id = Set(kantor_id);
    updated_karyawan.updated_by = Set(Some(user.id));  // Update updated_by
}
```

#### create_karyawan_with_photo
```rust
pub async fn create_karyawan_with_photo(
    State(db): State<DatabaseConnection>,
    Extension(user): Extension<User>,
    mut multipart: Multipart,
) -> Json<ApiResponse<Karyawan>> {
    let new_karyawan = KaryawanActiveModel {
        // ... form data
        created_by: Set(Some(user.id)),
        updated_by: Set(Some(user.id)),
        // ... photo fields
    };
}
```

#### upload_karyawan_photo
```rust
pub async fn upload_karyawan_photo(
    Path(id_str): Path<String>,
    State(db): State<DatabaseConnection>,
    Extension(user): Extension<User>,
    mut multipart: Multipart,
) -> Json<ApiResponse<Karyawan>> {
    let mut updated_karyawan: KaryawanActiveModel = existing_karyawan.into();
    // ... photo updates
    updated_karyawan.updated_by = Set(Some(user.id));
}
```

#### delete_karyawan_photo
```rust
pub async fn delete_karyawan_photo(
    Path(id_str): Path<String>,
    State(db): State<DatabaseConnection>,
    Extension(user): Extension<User>,
) -> Json<ApiResponse<Karyawan>> {
    let mut updated_karyawan: KaryawanActiveModel = existing_karyawan.into();
    // ... remove photo fields
    updated_karyawan.updated_by = Set(Some(user.id));
}
```

### 4. Response Model Updates

Updated `KaryawanWithKantor` struct:
```rust
#[derive(Serialize, Deserialize, Debug)]
pub struct KaryawanWithKantor {
    pub id: i32,
    pub nama: String,
    pub posisi: String,
    pub gaji: i32,
    pub kantor_id: i32,
    pub kantor_nama: Option<String>,
    pub foto_path: Option<String>,
    pub foto_original_name: Option<String>,
    pub foto_size: Option<i64>,
    pub foto_mime_type: Option<String>,
    pub created_by: Option<i32>,        // NEW
    pub updated_by: Option<i32>,        // NEW
    pub created_at: DateTimeWithTimeZone,
    pub updated_at: DateTimeWithTimeZone,
}
```

### 5. Documentation Updates

**OpenAPI Spec** (`docs/openapi.yaml`):
- Added `created_by` field to Karyawan schema
- Added `updated_by` field to Karyawan schema
- Updated descriptions and examples

**README.md**:
- Added "User Tracking" to features list
- Added "Foreign Key Constraints" to features
- Updated feature descriptions

## 🧪 Testing

**Test File**: `tests/api/user_tracking_test.py`

Comprehensive test covering:
1. ✅ User login and token retrieval
2. ✅ Create karyawan - verify created_by set correctly
3. ✅ Update karyawan - verify updated_by updated correctly
4. ✅ Get karyawan with full tracking info
5. ✅ Cleanup test data

**Test Results**:
```
✅ created_by correctly set to logged-in user!
✅ updated_by correctly set to logged-in user!
✅ updated_by correctly updated!
```

## 📊 Database Schema

### Karyawan Table (Updated)
```
+--------------------+-----------+--------+
| Column             | Type      | Null   |
+--------------------+-----------+--------+
| id                 | INT       | NO     |
| nama               | VARCHAR   | NO     |
| posisi             | VARCHAR   | NO     |
| gaji               | INT       | NO     |
| kantor_id          | INT       | NO     |
| foto_path          | VARCHAR   | YES    |
| foto_original_name | VARCHAR   | YES    |
| foto_size          | BIGINT    | YES    |
| foto_mime_type     | VARCHAR   | YES    |
| created_by         | INT       | YES    | ← NEW
| updated_by         | INT       | YES    | ← NEW
| created_at         | DATETIME  | NO     |
| updated_at         | DATETIME  | NO     |
+--------------------+-----------+--------+

Foreign Keys:
- kantor_id → kantor(id)
- created_by → users(id)  ← NEW
- updated_by → users(id)  ← NEW
```

## 🔄 API Response Example

### Before (without user tracking):
```json
{
  "success": true,
  "message": "Karyawan created successfully",
  "data": {
    "id": 61,
    "nama": "Budi Santoso",
    "posisi": "Software Engineer",
    "gaji": 8000000,
    "kantor_id": 2,
    "created_at": "2025-10-31T09:58:24Z",
    "updated_at": "2025-10-31T09:58:24Z"
  }
}
```

### After (with user tracking):
```json
{
  "success": true,
  "message": "Karyawan created successfully",
  "data": {
    "id": 61,
    "nama": "Budi Santoso",
    "posisi": "Software Engineer",
    "gaji": 8000000,
    "kantor_id": 2,
    "created_by": 1,        ← NEW
    "updated_by": 1,        ← NEW
    "created_at": "2025-10-31T09:58:24Z",
    "updated_at": "2025-10-31T09:58:24Z"
  }
}
```

## 🎯 Benefits

1. **Audit Trail**: Complete history of who created and modified each karyawan
2. **Accountability**: Track user actions for compliance and security
3. **Data Integrity**: Foreign key constraints ensure valid user references
4. **Automatic**: No manual intervention needed - handled by middleware
5. **Flexible**: Nullable fields allow for data migration and edge cases
6. **Transparent**: User tracking visible in all API responses

## 🔐 Security Considerations

1. ✅ User extracted from JWT middleware (authenticated only)
2. ✅ Foreign key cascade on user update
3. ✅ SET NULL on user deletion (preserve karyawan data)
4. ✅ Protected endpoints require valid JWT token
5. ✅ User tracking cannot be manipulated by client

## 📝 Migration Path

For existing karyawan records:
- `created_by` and `updated_by` will be NULL
- Future updates will set `updated_by` to current user
- Optional: Run data migration to populate historical data if needed

## ✅ Completion Checklist

- [x] Database migration created and applied
- [x] Model updated with new fields
- [x] Relations defined for user lookup
- [x] All create handlers updated
- [x] All update handlers updated
- [x] Response models updated
- [x] OpenAPI documentation updated
- [x] README updated
- [x] Test script created
- [x] Testing completed successfully
- [x] Documentation summary created

## 🚀 Next Steps (Optional Enhancements)

1. Add endpoints to get karyawan by creator user
2. Add user name/email in response (join users table)
3. Add permission check (e.g., only creator can delete)
4. Add audit log table for detailed change tracking
5. Add created_by/updated_by to kantor table as well

## 📚 Related Files

- Migration: `migration/src/m20251031_095022_add_user_tracking_to_karyawan.rs`
- Model: `src/models/karyawan.rs`
- Handlers: `src/handlers/karyawan.rs`
- Middleware: `src/middleware/auth.rs`
- Test: `tests/api/user_tracking_test.py`
- Docs: `docs/openapi.yaml`, `README.md`