# Quick Start: CORS Configuration

## 🚀 3 Steps to Configure CORS

### Step 1: Choose Your Mode

```bash
# Option A: Allow ALL (Testing Only - NOT SECURE!)
CORS_ORIGINS=*

# Option B: Localhost Development
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Option C: Production (Your Server)
CORS_ORIGINS=http://103.167.113.116:3000,http://103.167.113.116:5173
```

### Step 2: Update .env File

```bash
# Edit .env
notepad .env

# Add/Update this line:
CORS_ORIGINS=http://103.167.113.116:3000,http://103.167.113.116:5173
```

### Step 3: Start Server

```bash
cargo run
```

**Expected Output:**
```
✅ CORS origin added: http://103.167.113.116:3000
✅ CORS origin added: http://103.167.113.116:5173
🚀 Server running on http://0.0.0.0:8080
```

## ✅ Verify Configuration

```powershell
# Check environment
.\scripts\check_env.ps1

# Test CORS
.\scripts\test_production_cors.ps1
```

## 📝 Common Scenarios

### Scenario 1: "I just want to test quickly"

```bash
# .env
CORS_ORIGINS=*

# Start
cargo run

# ⚠️ Remember to change back after testing!
```

### Scenario 2: "I'm developing locally"

```bash
# .env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Start
cargo run
```

### Scenario 3: "I'm deploying to production"

```bash
# .env
CORS_ORIGINS=http://103.167.113.116:3000,http://103.167.113.116:5173
ENVIRONMENT=production

# Build and run
cargo build --release
cargo run --release
```

## 🐛 Troubleshooting

### Problem: "CORS error in browser"

**Solution:**
```bash
# 1. Check .env has correct origins
.\scripts\check_env.ps1

# 2. Restart server
# Stop (Ctrl+C) then: cargo run

# 3. Test CORS
.\scripts\test_production_cors.ps1
```

### Problem: "JWT not working with wildcard"

**This is expected!** Wildcard (`*`) disables credentials.

**Solution:**
```bash
# Use specific origins instead
CORS_ORIGINS=http://103.167.113.116:3000,http://103.167.113.116:5173
```

## 📚 More Help

- **Full Guide:** `docs/CORS_QUICK_REFERENCE.md`
- **Examples:** `.env.example`
- **Security:** `docs/SECURITY_IMPLEMENTATION.md`
