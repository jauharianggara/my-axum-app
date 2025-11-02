# Environment Configuration Guide

This directory contains environment configuration files for different deployment scenarios.

## Available Configuration Files

### 📄 config.yaml
Complete YAML configuration with all available options. Use this as a reference for understanding all configuration parameters.

### 📄 .env.development
Local development environment configuration.
- Database: Local MySQL
- CORS: Allows localhost origins
- Logging: Debug level with pretty format
- Rate limiting: Disabled/relaxed

**Usage:**
```bash
cp .env.development .env
cargo run
```

### 📄 .env.staging
Staging/testing environment configuration.
- Database: Staging database
- CORS: Staging domains + localhost
- Logging: Info level
- Rate limiting: Moderate

**Usage:**
```bash
cp .env.staging .env
cargo run
```

### 📄 .env.production
Production environment configuration.
- Database: Production database
- CORS: Specific production domains only
- Logging: Info level
- Rate limiting: Strict

**Usage:**
```bash
cp .env.production .env
cargo build --release
./target/release/my-axum-app
```

## Quick Start

### 1️⃣ Choose Your Environment

**Development:**
```powershell
Copy-Item .env.development .env
```

**Staging:**
```powershell
Copy-Item .env.staging .env
```

**Production:**
```powershell
Copy-Item .env.production .env
```

### 2️⃣ Update Critical Values

Edit `.env` and update these REQUIRED fields:

```env
# Database password
DB_PASSWORD=your_secure_password

# JWT Secret (minimum 32 characters)
JWT_SECRET=your-super-secret-jwt-key-min-32-chars

# CORS Origins (your actual domains)
CORS_ORIGINS=https://your-frontend.com,https://api.your-domain.com
```

### 3️⃣ Generate Secure JWT Secret

**Windows PowerShell:**
```powershell
$bytes = New-Object byte[] 32
(New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($bytes)
[Convert]::ToBase64String($bytes)
```

**Linux/Mac:**
```bash
openssl rand -base64 32
```

### 4️⃣ Verify Configuration

```powershell
.\scripts\check_env.ps1
```

## Configuration Options Explained

### 🔒 Security

**JWT_SECRET:**
- Minimum 32 characters
- Use cryptographically secure random string
- Different secret for each environment

**CORS_ORIGINS:**
- `*` = Allow all (⚠️ NOT for production)
- Specific domains = Recommended for production
- Comma-separated list for multiple domains

### 🗄️ Database

**DATABASE_URL Format:**
```
mysql://username:password@host:port/database
```

**Connection Pool:**
- Development: 5 connections
- Staging: 8 connections
- Production: 10 connections

### 📁 File Uploads

**UPLOAD_MAX_SIZE:**
- Default: 5242880 bytes (5MB)
- Adjust based on requirements

**ALLOWED_EXTENSIONS:**
- Comma-separated list
- Example: `jpg,jpeg,png,gif`

### 🚦 Rate Limiting

**Development:**
- Usually disabled or very high limits
- `RATE_LIMIT_ENABLED=false`

**Production:**
- Enabled with strict limits
- `RATE_LIMIT_REQUESTS_PER_MIN=60`

### 📊 Logging

**LOG_LEVEL Options:**
- `trace`: Most verbose
- `debug`: Development debugging
- `info`: General information (recommended for production)
- `warn`: Warnings only
- `error`: Errors only

**LOG_FORMAT:**
- `json`: Machine-readable (production)
- `pretty`: Human-readable (development)

## Docker Deployment

Use `docker-compose.env.yml` for containerized deployment:

```bash
# Create .env for Docker
cp .env.production .env

# Edit database and secrets
nano .env

# Start services
docker-compose -f docker-compose.env.yml up -d
```

## Environment Variables Priority

Configuration is loaded in this order (later overrides earlier):

1. `config.yaml` (defaults)
2. `.env` file
3. System environment variables
4. Command-line arguments

## Security Best Practices

### ✅ DO:
- Use different JWT secrets for each environment
- Use strong database passwords (min 16 chars, mixed case, numbers, symbols)
- Enable HTTPS in production (SSL_ENABLED=true)
- Use specific CORS origins in production
- Keep `.env` files out of version control
- Rotate secrets regularly

### ❌ DON'T:
- Commit `.env` files to Git
- Use `CORS_ORIGINS=*` in production
- Use weak JWT secrets
- Share secrets between environments
- Use default passwords in production

## Troubleshooting

### Port Already In Use
```powershell
# Check what's using the port
Get-NetTCPConnection -LocalPort 8080
# Kill the process
Stop-Process -Id <PID> -Force
```

### Database Connection Failed
```powershell
# Test MySQL connection
mysql -u axum -p -h localhost my_axum_db
# Check DATABASE_URL format
```

### CORS Errors
```powershell
# Test CORS configuration
.\scripts\test_cors_config.ps1
# Verify origins in .env
```

## Quick Reference

| Environment | Use Case | CORS | Logging | Rate Limit |
|-------------|----------|------|---------|------------|
| Development | Local dev | Localhost | Debug | Disabled |
| Staging | Testing | Staging + Local | Info | Moderate |
| Production | Live | Specific domains | Info | Strict |

## Additional Resources

- 📖 [Full Deployment Guide](../DEPLOYMENT_GUIDE.md)
- 🔒 [Security Documentation](../docs/SECURITY_IMPLEMENTATION.md)
- 🧪 [Testing Guide](../docs/TESTING_GUIDE.md)
- 🌐 [CORS Configuration](../docs/CORS_CONFIGURATION_GUIDE.md)
- 🐳 [Docker Guide](../docs/DOCKER_README.md)
