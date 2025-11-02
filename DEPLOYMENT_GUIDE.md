# Quick Deployment Guide - Production Server

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Server with Apache installed
- MySQL database running
- Domain: axum.synergyinfinity.id pointing to server

### Step 1: Enable Apache Modules

```bash
sudo a2enmod proxy proxy_http headers rewrite
sudo systemctl restart apache2
```

### Step 2: Copy Apache Configuration

```bash
# Copy the vhost configuration
sudo cp apache-vhost.conf /www/server/panel/vhost/apache/axum.synergyinfinity.id.conf

# Test configuration
sudo apachectl configtest

# Restart Apache
sudo systemctl restart apache2
```

### Step 3: Update .env for Production

```bash
# Edit .env file
nano .env

# Update these values:
ENVIRONMENT=production
HOST=127.0.0.1
PORT=8080
CORS_ORIGINS=http://axum.synergyinfinity.id,https://axum.synergyinfinity.id
DATABASE_URL=mysql://axum:rahasia123@localhost:3306/my_axum_db
JWT_SECRET=change-this-to-secure-random-string-min-32-chars
BCRYPT_COST=12
RUST_LOG=info
```

### Step 4: Build and Deploy

```bash
# Build release version
cargo build --release

# Create application directory
sudo mkdir -p /www/wwwroot/axum-backend
sudo cp -r . /www/wwwroot/axum-backend/
sudo chown -R www-data:www-data /www/wwwroot/axum-backend
```

### Step 5: Setup Systemd Service

```bash
# Copy service file
sudo cp axum-api.service /etc/systemd/system/

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable axum-api
sudo systemctl start axum-api

# Check status
sudo systemctl status axum-api
```

### Step 6: Test Deployment

```bash
# Test local backend
curl http://127.0.0.1:8080/health

# Test via Apache/domain
curl http://axum.synergyinfinity.id/health

# Should return:
# {"status":"healthy","timestamp":"..."}
```

## ✅ Verification Checklist

- [ ] Apache proxy modules enabled
- [ ] VirtualHost configuration copied
- [ ] .env file updated with production settings
- [ ] Application built with `cargo build --release`
- [ ] Files copied to `/www/wwwroot/axum-backend`
- [ ] Systemd service installed and running
- [ ] Apache restarted
- [ ] Health check responds at http://127.0.0.1:8080/health
- [ ] Domain accessible at http://axum.synergyinfinity.id/health

## 🐛 Troubleshooting

### Issue: 502 Bad Gateway

```bash
# Check if Axum service is running
sudo systemctl status axum-api

# Check logs
journalctl -u axum-api -n 50

# Restart service
sudo systemctl restart axum-api
```

### Issue: Apache Configuration Error

```bash
# Test Apache config
sudo apachectl configtest

# Check Apache error log
tail -f /www/wwwlogs/axum.synergyinfinity.id-error_log
```

### Issue: CORS Errors

```bash
# Update .env with correct domain
CORS_ORIGINS=http://axum.synergyinfinity.id,https://axum.synergyinfinity.id

# Restart Axum service
sudo systemctl restart axum-api
```

### Issue: Port 8080 Already in Use

```bash
# Check what's using port 8080
sudo netstat -tulpn | grep 8080

# Or use ss
sudo ss -tulpn | grep 8080

# Kill process if needed
sudo kill -9 <PID>
```

## 📊 Monitoring

```bash
# View Axum logs
journalctl -u axum-api -f

# View Apache access logs
tail -f /www/wwwlogs/axum.synergyinfinity.id-access_log

# View Apache error logs
tail -f /www/wwwlogs/axum.synergyinfinity.id-error_log

# Check service status
sudo systemctl status axum-api
```

## 🔄 Update/Redeploy

```bash
# Pull latest code
git pull

# Rebuild
cargo build --release

# Copy new binary
sudo cp target/release/my-axum-app /www/wwwroot/axum-backend/target/release/

# Restart service
sudo systemctl restart axum-api
```

## 🎯 Final URLs

- **API Health:** http://axum.synergyinfinity.id/health
- **Auth Login:** http://axum.synergyinfinity.id/api/auth/login
- **All Karyawan:** http://axum.synergyinfinity.id/api/karyawans
- **All Kantor:** http://axum.synergyinfinity.id/api/kantors

## 🔒 Security Notes

1. Change `JWT_SECRET` to a strong random string
2. Use HTTPS in production (install SSL certificate)
3. Set `CORS_ORIGINS` to specific domains (no wildcard `*`)
4. Use strong database passwords
5. Keep system updated: `sudo apt update && sudo apt upgrade`

## 📝 Service Management Commands

```bash
# Start service
sudo systemctl start axum-api

# Stop service
sudo systemctl stop axum-api

# Restart service
sudo systemctl restart axum-api

# View status
sudo systemctl status axum-api

# Enable on boot
sudo systemctl enable axum-api

# Disable on boot
sudo systemctl disable axum-api

# View logs
journalctl -u axum-api -f
```

---

**Deployment Time:** ~5 minutes  
**Status:** ✅ Ready for Production
