# CORS Configuration Guide

## 🌐 CORS Environment Variable Configuration

API sekarang mendukung konfigurasi CORS melalui environment variables, membuatnya lebih fleksibel dan mudah dikonfigurasi tanpa perlu mengubah kode.

## ⚙️ Environment Variables

### CORS_ORIGINS
**Format**: Comma-separated list of allowed origins
**Default Development**: `http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000`
**Default Production**: `https://yourdomain.com,https://www.yourdomain.com`

### ENVIRONMENT
**Format**: String value
**Values**: `development` atau `production`
**Default**: `development`

## 📝 Configuration Examples

### 1. Development Configuration (.env)
```env
# Development mode
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000
```

### 2. Production Configuration
```env
# Production mode
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://api.yourdomain.com
```

### 3. Multiple Domain Configuration
```env
# Support multiple domains and subdomains
CORS_ORIGINS=https://app.example.com,https://admin.example.com,https://api.example.com,https://dashboard.example.com
```

### 4. Mixed Environment (Development + Staging)
```env
# Development with staging server
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,https://staging.yourdomain.com
```

## 🛡️ Security Considerations

### 1. Production Security
- ✅ **Always use HTTPS** dalam production
- ✅ **Specify exact domains** - jangan gunakan wildcard (*)
- ✅ **Minimal required origins** - hanya tambahkan domain yang benar-benar diperlukan
- ✅ **Regular review** - review daftar origins secara berkala

### 2. Development Security
- ✅ **Localhost variants** - include semua localhost variants yang diperlukan
- ✅ **Port specificity** - specify exact ports untuk development servers
- ✅ **No wildcards** - bahkan dalam development, hindari wildcard

## 🔧 Configuration Process

### 1. Automatic Fallback
Jika `CORS_ORIGINS` tidak diset, sistem akan menggunakan default values berdasarkan `ENVIRONMENT`:

- **Development**: `http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000`
- **Production**: `https://yourdomain.com,https://www.yourdomain.com`

### 2. Error Handling
- Invalid URLs akan di-skip dengan warning log
- Empty values akan diabaikan
- Malformed headers akan diabaikan dengan error log

### 3. Dynamic Loading
Configuration dibaca saat server startup, restart diperlukan untuk perubahan configuration.

## 🧪 Testing CORS Configuration

### 1. Test dengan Browser
```javascript
// Test dari browser console
fetch('http://localhost:8080/api/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Origin': 'http://localhost:3000'
  },
  body: JSON.stringify({
    username: 'test',
    email: 'test@example.com',
    password: 'password123',
    full_name: 'Test User'
  })
})
```

### 2. Test dengan Python
```python
import requests

response = requests.post(
    'http://localhost:8080/api/auth/register',
    headers={
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000'  # Allowed origin
    },
    json={
        'username': 'test',
        'email': 'test@example.com',
        'password': 'password123',
        'full_name': 'Test User'
    }
)
print(f"Status: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
```

### 3. Test Invalid Origin
```python
import requests

response = requests.post(
    'http://localhost:8080/api/auth/register',
    headers={
        'Content-Type': 'application/json',
        'Origin': 'https://malicious-site.com'  # Not allowed
    },
    json={
        'username': 'test',
        'email': 'test@example.com',
        'password': 'password123',
        'full_name': 'Test User'
    }
)
# Should return 403 Forbidden
print(f"Status: {response.status_code}")
```

## 🚀 Deployment Examples

### 1. Docker Environment
```dockerfile
ENV ENVIRONMENT=production
ENV CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 2. Kubernetes ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  ENVIRONMENT: "production"
  CORS_ORIGINS: "https://yourdomain.com,https://www.yourdomain.com,https://api.yourdomain.com"
```

### 3. Cloud Platform Environment
```bash
# Heroku
heroku config:set ENVIRONMENT=production
heroku config:set CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# AWS
aws ssm put-parameter --name "/app/ENVIRONMENT" --value "production"
aws ssm put-parameter --name "/app/CORS_ORIGINS" --value "https://yourdomain.com,https://www.yourdomain.com"
```

## 🔍 Troubleshooting

### 1. CORS Errors in Browser
**Problem**: `Access to fetch at 'API_URL' from origin 'ORIGIN' has been blocked by CORS policy`

**Solutions**:
- Verify origin is listed in `CORS_ORIGINS`
- Check spelling and exact URL match
- Ensure protocol (http/https) matches
- Verify port numbers if specified

### 2. 403 Forbidden Responses
**Problem**: API returns 403 for valid requests

**Solutions**:
- Check if `Origin` header is being sent
- Verify origin is in allowed list
- Test with curl including Origin header

### 3. Environment Variable Not Loading
**Problem**: Configuration not taking effect

**Solutions**:
- Restart server after .env changes
- Verify .env file is in correct location
- Check for typos in variable names
- Use `env` command to verify variables are set

## 📋 Migration Guide

### From Hard-coded CORS to Environment Configuration

1. **Backup current configuration**
2. **Update .env file** with CORS_ORIGINS
3. **Test configuration** in development
4. **Deploy to staging** for validation
5. **Deploy to production** with production origins

### Example Migration
**Before**:
```rust
// Hard-coded in main.rs
.allow_origin([
    "http://localhost:3000".parse::<HeaderValue>().unwrap(),
    "https://yourdomain.com".parse::<HeaderValue>().unwrap(),
])
```

**After**:
```rust
// Dynamic from environment
.allow_origin(get_cors_origins())
```

```env
# In .env file
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## ✅ Best Practices Summary

1. **Environment-Specific Configuration**: Gunakan environment variables
2. **Principle of Least Privilege**: Minimal origins yang diperlukan
3. **Regular Review**: Review CORS configuration secara berkala
4. **Testing**: Test CORS configuration di semua environment
5. **Documentation**: Document semua allowed origins dan alasannya
6. **Monitoring**: Monitor CORS-related errors di production logs

Konfigurasi CORS yang fleksibel ini membuat aplikasi lebih mudah di-deploy dan di-maintain across different environments! 🎯