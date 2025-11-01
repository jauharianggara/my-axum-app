# Jabatan Feature Implementation Summary

## Date
2025-11-01

## Update Notice
**Last Updated**: 2025-11-01 - Updated to reflect removal of `posisi` field (see [20251101_REMOVE_POSISI_FIELD.md](./20251101_REMOVE_POSISI_FIELD.md))

## Overview
Added a new `jabatan` (job position) table and integrated it with the `karyawan` table as a mandatory field. Every employee must now have a job position assigned through `jabatan_id` field. The old `posisi` field has been completely removed.

## Database Changes

### New Table: `jabatan`
```sql
CREATE TABLE `jabatan` (
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `nama_jabatan` varchar(100) NOT NULL,
    `deskripsi` text NULL,
    `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Modified Table: `karyawan`
- Added column: `jabatan_id` int NOT NULL
- Added foreign key constraint:
  ```sql
  CONSTRAINT `fk_karyawan_jabatan_id` FOREIGN KEY (`jabatan_id`) 
  REFERENCES `jabatan` (`id`) 
  ON DELETE RESTRICT 
  ON UPDATE CASCADE
  ```

## Migrations Created
1. **m20251031_194811_create_jabatan_table.rs** - Creates the jabatan table
2. **m20251031_194846_add_jabatan_id_to_karyawan.rs** - Adds jabatan_id to karyawan with these steps:
   - Add jabatan_id as nullable column
   - Insert default jabatan ("Staff") 
   - Update existing karyawan to reference default jabatan
   - Make jabatan_id NOT NULL
   - Add foreign key constraint

## Code Changes

### New Files
1. **src/models/jabatan.rs** - Jabatan entity model with:
   - `Model` struct for database representation
   - `CreateJabatanRequest` and `UpdateJabatanRequest` DTOs
   - Field validations (nama_jabatan: 2-100 chars, deskripsi: max 500 chars)

2. **src/handlers/jabatan.rs** - CRUD handlers for jabatan:
   - `get_all_jabatan()` - List all jabatan
   - `get_jabatan_by_id(id)` - Get single jabatan
   - `create_jabatan(data)` - Create new jabatan
   - `update_jabatan(id, data)` - Update jabatan
   - `delete_jabatan(id)` - Delete jabatan (blocked if in use by FK constraint)

3. **src/routes/jabatan.rs** - Jabatan API routes with JWT authentication

4. **tests/scripts/test_jabatan.ps1** - Comprehensive test script (needs fixing for quotes)

### Modified Files
1. **src/models/karyawan.rs**
   - Added `jabatan_id: i32` field to Model
   - Added `Jabatan` relation in `enum Relation`
   - Added `Related<super::jabatan::Entity>` implementation
   - Added `jabatan_id` validation to Create/UpdateKaryawanRequest

2. **src/handlers/karyawan.rs**
   - Added `jabatan_id` and `jabatan_nama` to `KaryawanWithKantor` struct
   - Added `jabatan_id` parsing and validation in:
     * `create_karyawan()`
     * `update_karyawan()`
     * `create_karyawan_with_photo()`
   - Added `validate_jabatan_id_exists()` calls to ensure jabatan exists

3. **src/validators/karyawan.rs**
   - Added `validate_jabatan_id()` function
   - Added `validate_jabatan_id_exists()` async function

4. **src/main.rs**
   - Added jabatan routes: `/api/jabatans`

5. **src/models/mod.rs** - Export jabatan module
6. **src/handlers/mod.rs** - Export jabatan module  
7. **src/routes/mod.rs** - Export jabatan_routes

## API Endpoints

All jabatan endpoints require JWT authentication (Bearer token in Authorization header).

### GET /api/jabatans
List all jabatan
```json
{
  "success": true,
  "message": "List of jabatan retrieved successfully",
  "data": [
    {
      "id": 1,
      "nama_jabatan": "Staff",
      "deskripsi": "Jabatan Default",
      "created_at": "2025-11-01T02:59:51Z",
      "updated_at": "2025-11-01T02:59:51Z"
    }
  ]
}
```

### GET /api/jabatans/:id
Get jabatan by ID
```json
{
  "success": true,
  "message": "Jabatan with ID 1 retrieved successfully",
  "data": {
    "id": 1,
    "nama_jabatan": "Staff",
    "deskripsi": "Jabatan Default",
    "created_at": "2025-11-01T02:59:51Z",
    "updated_at": "2025-11-01T02:59:51Z"
  }
}
```

### POST /api/jabatans
Create new jabatan

**Request:**
```json
{
  "nama_jabatan": "Manager",
  "deskripsi": "Jabatan manajer"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Jabatan created successfully",
  "data": {
    "id": 2,
    "nama_jabatan": "Manager",
    "deskripsi": "Jabatan manajer",
    "created_at": "2025-11-01T03:11:00Z",
    "updated_at": "2025-11-01T03:11:00Z"
  }
}
```

### PUT /api/jabatans/:id
Update jabatan

**Request:**
```json
{
  "nama_jabatan": "Senior Manager",
  "deskripsi": "Manajer senior departemen"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Jabatan with ID 1 updated successfully",
  "data": {
    "id": 1,
    "nama_jabatan": "Senior Manager",
    "deskripsi": "Manajer senior departemen",
    "created_at": "2025-11-01T02:59:51Z",
    "updated_at": "2025-11-01T03:15:00Z"
  }
}
```

### DELETE /api/jabatans/:id
Delete jabatan

**Note:** Cannot delete jabatan if it's being used by any karyawan (foreign key constraint)

**Success Response:**
```json
{
  "success": true,
  "message": "Jabatan with ID 2 deleted successfully",
  "data": null
}
```

**Error (FK constraint):**
```json
{
  "success": false,
  "message": "Failed to delete jabatan",
  "errors": ["Database error: foreign key constraint fails"]
}
```

## Karyawan API Changes

### POST /api/karyawans
Now requires `jabatan_id` field:

**Request:**
```json
{
  "nama": "Budi Santoso",
  "gaji": "15000000",
  "kantor_id": "1",
  "jabatan_id": "1"   ← REQUIRED FIELD (posisi no longer used)
}
```

### PUT /api/karyawans/:id
Now requires `jabatan_id` field in update requests

## Validation Rules

### Jabatan
- `nama_jabatan`: 
  - Required
  - Length: 2-100 characters
- `deskripsi`:
  - Optional
  - Max length: 500 characters

### Karyawan (new validation)
- `jabatan_id`:
  - Required
  - Must be a positive integer
  - Must exist in jabatan table

## Testing

### Successful Tests
✅ Create jabatan  
✅ Get all jabatan  
✅ Get jabatan by ID  
✅ Update jabatan  
✅ Create karyawan with jabatan_id  
✅ Foreign key constraint prevents deletion of jabatan in use  
✅ Can delete unused jabatan

### Test Commands
```powershell
# Login
$loginBody = '{"username_or_email":"testuser","password":"password123"}'
$login = Invoke-RestMethod -Uri http://localhost:8080/api/auth/login -Method Post -Body $loginBody -ContentType "application/json"
$token = $login.data.token
$headers = @{"Authorization" = "Bearer $token"; "Content-Type" = "application/json"}

# Create jabatan
$jabatanBody = '{"nama_jabatan":"Manager","deskripsi":"Jabatan manajer"}'
$jabatan = Invoke-RestMethod -Uri http://localhost:8080/api/jabatans -Method Post -Body $jabatanBody -Headers $headers

# Create karyawan with jabatan
$karyawanBody = '{"nama":"Budi Santoso","gaji":"15000000","kantor_id":"1","jabatan_id":"1"}'
$karyawan = Invoke-RestMethod -Uri http://localhost:8080/api/karyawans -Method Post -Body $karyawanBody -Headers $headers
```

## Database Verification
```sql
-- Check jabatan table
SELECT * FROM jabatan;

-- Check karyawan with jabatan_id
SELECT id, nama, kantor_id, jabatan_id 
FROM karyawan 
ORDER BY id DESC LIMIT 5;

-- Verify foreign key constraint
SHOW CREATE TABLE karyawan;
```

## Notes
1. Default jabatan "Staff" was created during migration to handle existing karyawan records
2. All existing karyawan were assigned jabatan_id = 1 (Staff)
3. Foreign key constraint with `ON DELETE RESTRICT` prevents deletion of jabatan in use
4. `ON UPDATE CASCADE` propagates jabatan ID changes to karyawan
5. The jabatan feature is fully integrated with the karyawan management system

## Breaking Changes
⚠️ **IMPORTANT**: The karyawan create/update endpoints now REQUIRE the `jabatan_id` field. 
Any existing clients must be updated to include this field.

## Next Steps (Optional Enhancements)
- [ ] Add jabatan_nama to karyawan list responses (currently shows only jabatan_id)
- [ ] Add filter/search by jabatan in karyawan endpoints
- [ ] Add statistics endpoint: count karyawan per jabatan
- [ ] Update OpenAPI documentation
- [ ] Update Postman collection
- [ ] Add comprehensive integration tests
