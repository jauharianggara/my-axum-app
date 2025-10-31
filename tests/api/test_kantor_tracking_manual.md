# Manual Testing Guide - Kantor User Tracking

## Prerequisites
1. Start the server: `cargo run`
2. Database should be running with migrations applied

## Test Steps

### 1. Login
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "testuser",
    "password": "password123"
  }'
```

Expected response:
```json
{
  "status": "success",
  "message": "...",
  "data": {
    "token": "<JWT_TOKEN>",
    "user": {
      "id": 1,
      ...
    }
  }
}
```

Save the `token` value for next requests.

### 2. Create Kantor (with user tracking)
```bash
curl -X POST http://localhost:8080/api/kantors \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -d '{
    "nama": "Kantor Test User Tracking",
    "alamat": "Jl. Test User Tracking No. 123",
    "longitude": 106.8456,
    "latitude": -6.2088
  }'
```

Expected response should include:
- `created_by`: 1 (matches logged in user ID)
- `updated_by`: 1 (matches logged in user ID)

### 3. Update Kantor (should update updated_by)
```bash
curl -X PUT http://localhost:8080/api/kantors/<KANTOR_ID> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -d '{
    "nama": "Kantor Updated",
    "alamat": "Jl. Updated No. 456",
    "longitude": 106.8500,
    "latitude": -6.2100
  }'
```

Expected response should include:
- `created_by`: 1 (unchanged from creation)
- `updated_by`: 1 (updated to current user)

### 4. Get Kantor Details
```bash
curl -X GET http://localhost:8080/api/kantors/<KANTOR_ID> \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

Should return full kantor data with `created_by` and `updated_by` fields.

### 5. Cleanup - Delete Test Kantor
```bash
curl -X DELETE http://localhost:8080/api/kantors/<KANTOR_ID> \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

## Verification Checklist

✅ **Create kantor**
- `created_by` is set to logged-in user ID
- `updated_by` is set to logged-in user ID

✅ **Update kantor**
- `created_by` remains unchanged
- `updated_by` is updated to current user ID

✅ **Multi-user test** (if admin user exists)
- Login as different user
- Update same kantor
- Verify `created_by` stays original user
- Verify `updated_by` changes to new user

## PowerShell Version

### 1. Login
```powershell
$loginResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/auth/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"username_or_email":"testuser","password":"password123"}'

$token = $loginResponse.data.token
$userId = $loginResponse.data.user.id
Write-Host "Logged in as user ID: $userId"
```

### 2. Create Kantor
```powershell
$createResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/kantors" `
  -Method POST `
  -Headers @{ Authorization = "Bearer $token" } `
  -ContentType "application/json" `
  -Body '{"nama":"Kantor Test","alamat":"Jl. Test No. 123","longitude":106.8456,"latitude":-6.2088}'

$kantorId = $createResponse.data.id
Write-Host "Created kantor ID: $kantorId"
Write-Host "Created by: $($createResponse.data.created_by)"
Write-Host "Updated by: $($createResponse.data.updated_by)"
```

### 3. Update Kantor
```powershell
$updateResponse = Invoke-RestMethod -Uri "http://localhost:8080/api/kantors/$kantorId" `
  -Method PUT `
  -Headers @{ Authorization = "Bearer $token" } `
  -ContentType "application/json" `
  -Body '{"nama":"Kantor Updated","alamat":"Jl. Updated No. 456","longitude":106.8500,"latitude":-6.2100}'

Write-Host "Updated kantor"
Write-Host "Created by: $($updateResponse.data.created_by)"
Write-Host "Updated by: $($updateResponse.data.updated_by)"
```

### 4. Delete Kantor
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/api/kantors/$kantorId" `
  -Method DELETE `
  -Headers @{ Authorization = "Bearer $token" }

Write-Host "Deleted kantor ID: $kantorId"
```
