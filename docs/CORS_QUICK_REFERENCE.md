# CORS Configuration Quick Reference

## 🚀 Quick Setup

### Option 1: Allow ALL Origins (Testing Only - ⚠️ NOT SECURE!)
```bash
# .env
CORS_ORIGINS=*
```

**Use case:** Quick testing, no authentication needed
**Limitation:** Credentials (JWT tokens) will be DISABLED

### Option 2: Localhost Development
```bash
# .env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000
```

**Use case:** Development with authentication
**Benefit:** Full credential support

### Option 3: Production with IP (Your Server)
```bash
# .env
CORS_ORIGINS=http://103.167.113.116:3000,http://103.167.113.116:5173,https://103.167.113.116:3000,https://103.167.113.116:5173
```

**Use case:** Production deployment with IP address
**Note:** Include both HTTP and HTTPS if using SSL

### Option 4: Production with Domain
```bash
# .env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://api.yourdomain.com
```

**Use case:** Production with custom domain
**Benefit:** Professional setup

## 🧪 Testing Commands

### Check Environment Configuration
```powershell
.\scripts\check_env.ps1
```

### Test CORS with Localhost
```powershell
.\scripts\test_cors_config.ps1
```

### Test CORS with Production Server
```powershell
.\scripts\test_production_cors.ps1

# Or with custom URL
.\scripts\test_production_cors.ps1 -ServerUrl "http://103.167.113.116:8080" -FrontendUrl "http://103.167.113.116:3000"
```

### Manual CORS Test (curl)
```powershell
curl -H "Origin: http://103.167.113.116:3000" `
     -H "Access-Control-Request-Method: POST" `
     -X OPTIONS `
     -I `
     http://103.167.113.116:8080/api/auth/login
```

## 📊 Configuration Comparison

| Configuration | Credentials | Security | Use Case | Production Ready |
|---------------|-------------|----------|----------|------------------|
| `CORS_ORIGINS=*` | ❌ Disabled | ⚠️ Low | Quick testing | ❌ NO |
| Specific URLs | ✅ Enabled | ✅ High | All | ✅ YES |
| Default (dev) | ✅ Enabled | ⚠️ Medium | Development | ❌ NO |

## ⚠️ Important Notes

### Wildcard Limitations
When using `CORS_ORIGINS=*`:
- ❌ Cannot use Authorization headers
- ❌ Cannot use cookies
- ❌ JWT authentication won't work properly
- ✅ Only for public APIs or testing

### Security Best Practices
1. Never use `*` in production
2. Always specify exact origins (no wildcards in middle)
3. Include protocol (http/https)
4. Include port if not default (80/443)
5. No trailing slashes

### Common Mistakes

❌ **WRONG:**
```bash
CORS_ORIGINS=http://103.167.113.116:3000/  # Trailing slash
CORS_ORIGINS=http://localhost:3000, http://localhost:5173  # Spaces
CORS_ORIGINS=103.167.113.116:3000  # Missing protocol
```

✅ **CORRECT:**
```bash
CORS_ORIGINS=http://103.167.113.116:3000,http://103.167.113.116:5173
```

## 🔧 Troubleshooting

### Issue: CORS Error in Browser
**Symptom:** "blocked by CORS policy" in console

**Solution:**
1. Check `.env` has correct CORS_ORIGINS
2. Restart server after changing `.env`
3. Clear browser cache
4. Test with: `.\scripts\test_cors_config.ps1`

### Issue: JWT Not Working with Wildcard
**Symptom:** Authorization header ignored

**Solution:**
Use specific origins instead of `*`:
```bash
CORS_ORIGINS=http://103.167.113.116:3000,http://103.167.113.116:5173
```

### Issue: Origin Not Matching
**Symptom:** CORS error even with configured origin

**Check:**
- Exact protocol match (http vs https)
- Exact port match (:3000 vs :5173)
- No trailing slash
- No typos in URL

## 📝 Workflow Examples

### Development Workflow
```bash
# 1. Set development CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# 2. Start server
cargo run

# 3. Test
.\scripts\test_cors_config.ps1
```

### Production Deployment
```bash
# 1. Update .env for production
CORS_ORIGINS=http://103.167.113.116:3000,http://103.167.113.116:5173
ENVIRONMENT=production

# 2. Build and run
cargo build --release
cargo run --release

# 3. Test
.\scripts\test_production_cors.ps1
```

### Quick Testing (Temporary)
```bash
# 1. Temporarily allow all
CORS_ORIGINS=*

# 2. Test your frontend
# 3. Change back to specific origins!
CORS_ORIGINS=http://103.167.113.116:3000
```

## 🎯 Decision Tree

```
Need CORS for...
├─ Quick testing without auth?
│  └─ Use: CORS_ORIGINS=*
│
├─ Local development with auth?
│  └─ Use: CORS_ORIGINS=http://localhost:3000,http://localhost:5173
│
├─ Production with IP?
│  └─ Use: CORS_ORIGINS=http://103.167.113.116:3000,http://103.167.113.116:5173
│
└─ Production with domain?
   └─ Use: CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 🔍 Verification Steps

After configuring CORS:

1. ✅ Check `.env` file exists
2. ✅ Run: `.\scripts\check_env.ps1`
3. ✅ Restart server
4. ✅ Run: `.\scripts\test_cors_config.ps1`
5. ✅ Test from actual frontend
6. ✅ Check browser DevTools Network tab

## 📚 Additional Resources

- **Full Guide:** `docs/CORS_CONFIGURATION_GUIDE.md`
- **Security Guide:** `docs/SECURITY_IMPLEMENTATION.md`
- **API Documentation:** `docs/API_DOCUMENTATION_GUIDE.md`
- **Testing Guide:** `docs/TESTING_GUIDE.md`
