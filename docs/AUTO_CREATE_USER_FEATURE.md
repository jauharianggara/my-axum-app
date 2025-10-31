# Auto-Create User untuk Karyawan

## Overview

Ketika mendaftarkan karyawan baru, sistem akan **otomatis membuat akun user** untuk karyawan tersebut dengan password default `12345678`.

## Fitur

### Automatic User Creation

Saat membuat karyawan baru (tanpa menyediakan `user_id`):

1. **Username Generation**: Dibuat dari nama karyawan (lowercase, tanpa spasi)
   - Contoh: "Budi Santoso" → username: `budisantoso`

2. **Email Generation**: Dibuat dari username dengan domain `@karyawan.local`
   - Contoh: `budisantoso@karyawan.local`

3. **Default Password**: `12345678` (di-hash menggunakan bcrypt)

4. **Full Name**: Menggunakan nama karyawan

5. **Status**: `is_active = true`

### Existing User Check

Jika username sudah ada di database:
- Sistem akan menggunakan user yang sudah ada
- Tidak membuat user baru
- Karyawan akan di-link ke user yang existing

### Manual User ID

Jika Anda menyediakan `user_id` saat create karyawan:
- Sistem **TIDAK** akan auto-create user
- Akan menggunakan user_id yang diberikan

## API Endpoints

### Create Karyawan (Auto-create User)

**Endpoint**: `POST /api/karyawans`

**Request Body**:
```json
{
  "nama": "Budi Santoso",
  "posisi": "Software Engineer",
  "gaji": "8000000",
  "kantor_id": "1"
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Karyawan created successfully",
  "data": {
    "id": 1,
    "nama": "Budi Santoso",
    "posisi": "Software Engineer",
    "gaji": 8000000,
    "kantor_id": 1,
    "user_id": 2,  // Auto-created user ID
    "created_by": 1,
    "updated_by": 1,
    "created_at": "2025-10-31T10:30:00Z",
    "updated_at": "2025-10-31T10:30:00Z"
  }
}
```

**Created User**:
- Username: `budisantoso`
- Email: `budisantoso@karyawan.local`
- Password: `12345678`
- Full Name: "Budi Santoso"

### Create Karyawan with Existing User

**Request Body**:
```json
{
  "nama": "Ahmad Wijaya",
  "posisi": "Manager",
  "gaji": "12000000",
  "kantor_id": "1",
  "user_id": "5"  // Use existing user
}
```

Sistem akan menggunakan user dengan ID 5, tidak membuat user baru.

### Create Karyawan with Photo (Auto-create User)

**Endpoint**: `POST /api/karyawans/with-photo`

**Request** (multipart/form-data):
```
nama: Siti Nurhaliza
posisi: Designer
gaji: 7500000
kantor_id: 2
foto: [binary file]
```

User akan otomatis dibuat dengan:
- Username: `sitinurhaliza`
- Email: `sitinurhaliza@karyawan.local`
- Password: `12345678`

## Login Karyawan

Setelah karyawan dibuat, karyawan dapat login menggunakan:

**Endpoint**: `POST /api/auth/login`

**Request**:
```json
{
  "username_or_email": "budisantoso",
  "password": "12345678"
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "user": {
      "id": 2,
      "username": "budisantoso",
      "email": "budisantoso@karyawan.local",
      "full_name": "Budi Santoso",
      "is_active": true,
      "created_at": "2025-10-31T10:30:00Z"
    },
    "token": "eyJhbGc...",
    "expires_in": 86400
  }
}
```

## Security Considerations

### Password Default

⚠️ **PENTING**: Password default `12345678` harus segera diganti setelah karyawan login pertama kali.

**Best Practices**:
1. Implementasikan "force change password" pada first login
2. Kirim notifikasi ke karyawan tentang akun mereka
3. Educate karyawan untuk menggunakan password yang kuat

### Username Collision

Jika ada 2 karyawan dengan nama yang sama (misal: "Ahmad Ahmad"):
- Username yang dibuat sama: `ahmadahmad`
- Karyawan kedua akan di-link ke user pertama yang sudah ada
- **Rekomendasi**: Gunakan NIP/NIK untuk generate username yang unik

## Implementation Details

### Code Flow

```rust
// 1. Check if user_id provided
if user_id.is_none() {
    // 2. Generate username from nama
    let username = nama.to_lowercase().replace(" ", "");
    
    // 3. Check if username exists
    match UserEntity::find()
        .filter(Column::Username.eq(&username))
        .one(&db)
        .await 
    {
        Ok(None) => {
            // 4. Create new user
            let password_hash = PasswordService::hash_password("12345678")?;
            let new_user = UserActiveModel {
                username: Set(username),
                email: Set(format!("{}@karyawan.local", username)),
                password_hash: Set(password_hash),
                full_name: Set(Some(nama.clone())),
                is_active: Set(true),
                ..Default::default()
            };
            user_id = Some(new_user.insert(&db).await?.id);
        }
        Ok(Some(existing)) => {
            // 5. Use existing user
            user_id = Some(existing.id);
        }
        Err(e) => return error
    }
}
```

### Database Tables

**users**:
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**karyawan**:
```sql
CREATE TABLE karyawan (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nama VARCHAR(50) NOT NULL,
    posisi VARCHAR(30) NOT NULL,
    gaji INT NOT NULL,
    kantor_id INT NOT NULL,
    user_id INT NULL UNIQUE,
    -- ... other fields
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);
```

## Testing

### Test Scenario 1: Auto-create User

```bash
# Create karyawan without user_id
curl -X POST http://localhost:8080/api/karyawans \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "Test User Auto",
    "posisi": "Tester",
    "gaji": "5000000",
    "kantor_id": "1"
  }'

# Login with auto-created user
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "testuserauto",
    "password": "12345678"
  }'
```

### Test Scenario 2: Duplicate Username

```bash
# Create first karyawan
curl -X POST http://localhost:8080/api/karyawans \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "John Doe",
    "posisi": "Developer",
    "gaji": "7000000",
    "kantor_id": "1"
  }'

# Create second karyawan with same name
curl -X POST http://localhost:8080/api/karyawans \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "John Doe",
    "posisi": "Designer",
    "gaji": "6500000",
    "kantor_id": "2"
  }'

# Both will have user_id pointing to same user
```

### Test Scenario 3: Manual User ID

```bash
# Create karyawan with existing user_id
curl -X POST http://localhost:8080/api/karyawans \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "Existing User Karyawan",
    "posisi": "Manager",
    "gaji": "10000000",
    "kantor_id": "1",
    "user_id": "5"
  }'
```

## Future Enhancements

1. **Unique Username Generation**:
   - Append number if username exists: `johndoe1`, `johndoe2`, etc.
   - Use employee ID/NIP for username generation

2. **Email Notification**:
   - Send welcome email with credentials
   - Include link to change password

3. **Password Policy**:
   - Force password change on first login
   - Implement password complexity requirements

4. **Bulk Import**:
   - CSV import with auto-create users
   - Batch user creation

5. **Username Customization**:
   - Allow custom username pattern
   - Configuration for email domain

## Troubleshooting

### Issue: User creation fails

**Error**: "Failed to create user account"

**Solution**:
- Check database permissions
- Verify bcrypt is working
- Check username/email uniqueness

### Issue: Cannot login with auto-created user

**Error**: "Invalid credentials"

**Solution**:
- Verify password is exactly `12345678`
- Check user `is_active = true`
- Verify username generation (no extra spaces)

### Issue: Multiple karyawan sharing same user

**Cause**: Same nama generates same username

**Solution**:
- Ensure unique names or use manual user_id
- Implement unique username generation with suffix

## Summary

✅ Auto-create user saat create karyawan (jika tidak ada user_id)
✅ Password default: `12345678`
✅ Username dari nama (lowercase, no spaces)
✅ Email: `{username}@karyawan.local`
✅ Reuse existing user jika username sudah ada
✅ Support manual user_id jika diperlukan
✅ Works untuk both regular dan with-photo endpoints
