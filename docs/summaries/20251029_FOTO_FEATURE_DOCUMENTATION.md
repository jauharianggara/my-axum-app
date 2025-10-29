# 📸 Karyawan Photo Upload Feature

**📅 Created**: October 29, 2025  
**⏰ Last Updated**: October 29, 2025  
**📝 Status**: Complete ✅

## 🎯 Overview
Fitur upload foto untuk karyawan telah berhasil diimplementasikan dengan validasi lengkap dan penanganan file yang aman.

## 🗄️ Database Schema
Migration `m20241029_000003_add_foto_column_to_karyawan` telah diterapkan dengan kolom:

```sql
ALTER TABLE karyawan ADD COLUMN foto_path VARCHAR(255) NULL;
ALTER TABLE karyawan ADD COLUMN foto_original_name VARCHAR(255) NULL;
ALTER TABLE karyawan ADD COLUMN foto_size BIGINT NULL;
ALTER TABLE karyawan ADD COLUMN foto_mime_type VARCHAR(100) NULL;
```

## 🔧 Backend Implementation

### 1. Model Updates
- `src/models/karyawan.rs`: Menambah fields foto
- `src/handlers/karyawan.rs`: Handler baru untuk foto operations
- `src/services/file_upload.rs`: Service untuk file management
- `src/routes/karyawan.rs`: Routes baru untuk foto endpoints

### 2. File Upload Service (`src/services/file_upload.rs`)
**Features:**
- ✅ File type validation (JPEG, PNG, WebP only)
- ✅ File size validation (max 5MB)
- ✅ Unique filename generation dengan UUID
- ✅ Safe file storage di `uploads/karyawan/photos/`
- ✅ Automatic cleanup on errors
- ✅ Old file deletion saat update

**Validation Rules:**
```rust
- Allowed types: image/jpeg, image/png, image/webp
- Max size: 5MB (5,242,880 bytes)
- File naming: karyawan_{id}_{uuid}.{ext}
- Storage path: uploads/karyawan/photos/
```

### 3. New API Endpoints

#### `POST /api/karyawans/with-photo`
Create karyawan dengan foto (multipart/form-data)

**Request:**
```
Content-Type: multipart/form-data

Fields:
- nama: string (2-50 chars)
- posisi: string (2-30 chars) 
- gaji: string (1,000,000 - 100,000,000)
- kantor_id: string (positive integer)
- foto: file (JPEG/PNG/WebP, max 5MB)
```

**Response:**
```json
{
  "success": true,
  "message": "Karyawan created successfully with photo",
  "data": {
    "id": 1,
    "nama": "John Doe",
    "posisi": "Developer",
    "gaji": 5000000,
    "kantor_id": 1,
    "foto_path": "uploads/karyawan/photos/karyawan_1_uuid.jpg",
    "foto_original_name": "photo.jpg",
    "foto_size": 1234567,
    "foto_mime_type": "image/jpeg",
    "created_at": "2024-10-29T...",
    "updated_at": "2024-10-29T..."
  }
}
```

#### `POST /api/karyawans/{id}/photo`
Upload/update foto ke karyawan yang sudah ada

**Request:**
```
Content-Type: multipart/form-data

Fields:
- foto: file (JPEG/PNG/WebP, max 5MB)
```

#### `DELETE /api/karyawans/{id}/photo`
Hapus foto karyawan

**Response:**
```json
{
  "success": true,
  "message": "Photo deleted successfully for karyawan ID 1",
  "data": {
    "id": 1,
    "foto_path": null,
    "foto_original_name": null,
    "foto_size": null,
    "foto_mime_type": null,
    ...
  }
}
```

### 4. Enhanced Existing Endpoints
Semua endpoint existing sekarang include photo fields:

#### `GET /api/karyawans/with-kantor`
```json
{
  "success": true,
  "message": "List of karyawans with kantor retrieved successfully",
  "data": [
    {
      "id": 1,
      "nama": "John Doe",
      "posisi": "Developer", 
      "gaji": 5000000,
      "kantor_id": 1,
      "kantor_nama": "Kantor Pusat",
      "foto_path": "uploads/karyawan/photos/karyawan_1_uuid.jpg",
      "foto_original_name": "photo.jpg",
      "foto_size": 1234567,
      "foto_mime_type": "image/jpeg",
      "created_at": "2024-10-29T...",
      "updated_at": "2024-10-29T..."
    }
  ]
}
```

## 🛡️ Security & Validation

### File Upload Security
1. **Type Validation**: Hanya menerima image files (JPEG, PNG, WebP)
2. **Size Validation**: Maximum 5MB per file
3. **Filename Sanitization**: UUID-based naming untuk avoid conflicts
4. **Path Traversal Prevention**: Safe directory creation
5. **Error Cleanup**: Automatic file deletion on validation/database errors

### Input Validation
1. **Karyawan Data**: Validasi standard (nama, posisi, gaji, kantor_id)
2. **File Fields**: Validasi content-type dan file size
3. **Database Constraints**: Foreign key validation untuk kantor_id

## 📁 File Organization

```
my-axum-app/
├── uploads/                    # Static file serving
│   └── karyawan/
│       └── photos/            # Karyawan photos
│           ├── karyawan_1_uuid.jpg
│           └── karyawan_2_uuid.png
├── src/
│   ├── services/
│   │   ├── mod.rs
│   │   └── file_upload.rs     # File upload service
│   ├── handlers/
│   │   └── karyawan.rs        # Enhanced with photo handlers
│   ├── models/
│   │   └── karyawan.rs        # Added photo fields
│   └── routes/
│       └── karyawan.rs        # Added photo routes
└── migration/
    └── src/
        └── m20241029_000003_add_foto_column_to_karyawan.rs
```

## 🌐 Frontend Integration

### HTML Form Example
```html
<form action="/api/karyawans/with-photo" method="post" enctype="multipart/form-data">
    <input type="text" name="nama" required>
    <input type="text" name="posisi" required>
    <input type="text" name="gaji" required>
    <input type="text" name="kantor_id" required>
    <input type="file" name="foto" accept="image/*">
    <button type="submit">Create with Photo</button>
</form>
```

### JavaScript Fetch Example
```javascript
const formData = new FormData();
formData.append('nama', 'John Doe');
formData.append('posisi', 'Developer');
formData.append('gaji', '5000000');
formData.append('kantor_id', '1');
formData.append('foto', fileInput.files[0]);

fetch('/api/karyawans/with-photo', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🧪 Testing

### Manual Testing dengan Postman/Insomnia
1. **Create with Photo**: POST `/api/karyawans/with-photo`
   - Form-data dengan semua fields + foto file
2. **Upload Photo**: POST `/api/karyawans/1/photo`
   - Form-data dengan foto file
3. **Get with Photos**: GET `/api/karyawans/with-kantor`
4. **Delete Photo**: DELETE `/api/karyawans/1/photo`

### Automated Testing
```bash
# Install dependencies
pip install Pillow requests

# Run comprehensive tests
python test_photo_upload.py
```

## 🚀 Deployment Notes

### Production Considerations
1. **Static File Serving**: Nginx/Apache untuk serve uploaded files
2. **Storage**: Consider cloud storage (AWS S3, etc.) untuk production
3. **CDN**: CloudFlare/CloudFront untuk photo delivery
4. **Backup**: Regular backup dari uploads directory
5. **Monitoring**: File upload metrics dan error tracking

### Environment Variables
```env
# Optional: Custom upload directory
UPLOAD_DIR=uploads

# Optional: Max file size (bytes)
MAX_FILE_SIZE=5242880

# Optional: Allowed file types
ALLOWED_TYPES=image/jpeg,image/png,image/webp
```

## ✅ Implementation Status

| Feature | Status |
|---------|--------|
| Database Schema | ✅ Complete |
| File Upload Service | ✅ Complete |
| API Endpoints | ✅ Complete |
| Validation | ✅ Complete |
| Error Handling | ✅ Complete |
| File Cleanup | ✅ Complete |
| Static File Serving | ✅ Complete |
| Documentation | ✅ Complete |
| Testing Framework | ✅ Complete |

## 🎉 Summary

Fitur upload foto karyawan telah **berhasil diimplementasikan** dengan:

1. ✅ **Database schema** lengkap dengan kolom foto
2. ✅ **File upload service** dengan validasi keamanan
3. ✅ **REST API endpoints** untuk semua operasi foto
4. ✅ **Error handling** dan cleanup otomatis
5. ✅ **Static file serving** untuk akses foto
6. ✅ **Comprehensive validation** untuk input dan file
7. ✅ **Testing framework** untuk verifikasi functionality

API siap digunakan untuk upload, update, dan delete foto karyawan dengan validasi lengkap dan penanganan error yang robust!