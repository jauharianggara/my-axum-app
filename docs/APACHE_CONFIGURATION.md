# Apache Reverse Proxy Configuration for Axum API

## 🌐 Domain Setup

**Domain:** axum.synergyinfinity.id  
**Backend:** Rust Axum API on port 8080  
**Frontend:** React/Next.js (if applicable)

## 📝 Apache VirtualHost Configuration

### Option 1: API Only (Recommended)

```apache
<VirtualHost *:80>
    ServerAdmin webmaster@synergyinfinity.id
    ServerName axum.synergyinfinity.id
    ServerAlias 41ecdf6f.axum.synergyinfinity.id
    
    ErrorLog "/www/wwwlogs/axum.synergyinfinity.id-error_log"
    CustomLog "/www/wwwlogs/axum.synergyinfinity.id-access_log" combined

    # Enable proxy modules
    ProxyPreserveHost On
    ProxyRequests Off
    
    # Reverse proxy to Axum backend
    ProxyPass / http://127.0.0.1:8080/
    ProxyPassReverse / http://127.0.0.1:8080/
    
    # WebSocket support (if needed in future)
    RewriteEngine On
    RewriteCond %{HTTP:Upgrade} =websocket [NC]
    RewriteRule /(.*) ws://127.0.0.1:8080/$1 [P,L]
    
    # Proxy headers
    RequestHeader set X-Forwarded-Proto "http"
    RequestHeader set X-Forwarded-Port "80"
    RequestHeader set X-Real-IP %{REMOTE_ADDR}s
    
    # Timeout settings for long requests
    ProxyTimeout 300
    
    # CORS headers (if Axum CORS is not enough)
    # Header always set Access-Control-Allow-Origin "*"
    # Header always set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
    # Header always set Access-Control-Allow-Headers "Authorization, Content-Type, Accept"
</VirtualHost>
```

### Option 2: With Frontend Static Files

```apache
<VirtualHost *:80>
    ServerAdmin webmaster@synergyinfinity.id
    DocumentRoot "/www/wwwroot/axum.synergyinfinity.id"
    ServerName axum.synergyinfinity.id
    ServerAlias 41ecdf6f.axum.synergyinfinity.id
    
    ErrorLog "/www/wwwlogs/axum.synergyinfinity.id-error_log"
    CustomLog "/www/wwwlogs/axum.synergyinfinity.id-access_log" combined

    # Enable proxy modules
    ProxyPreserveHost On
    ProxyRequests Off
    
    # Proxy API requests to Axum backend
    ProxyPass /api http://127.0.0.1:8080/api
    ProxyPassReverse /api http://127.0.0.1:8080/api
    
    ProxyPass /health http://127.0.0.1:8080/health
    ProxyPassReverse /health http://127.0.0.1:8080/health
    
    ProxyPass /uploads http://127.0.0.1:8080/uploads
    ProxyPassReverse /uploads http://127.0.0.1:8080/uploads
    
    # Serve frontend static files from DocumentRoot
    <Directory "/www/wwwroot/axum.synergyinfinity.id">
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
        DirectoryIndex index.html
        
        # Handle React/Next.js routing
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>
    
    # Proxy headers
    RequestHeader set X-Forwarded-Proto "http"
    RequestHeader set X-Forwarded-Port "80"
    RequestHeader set X-Real-IP %{REMOTE_ADDR}s
    
    # Security headers
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "DENY"
    Header always set X-XSS-Protection "1; mode=block"
    
    # DENY sensitive files
    <FilesMatch "^\.">
        Require all denied
    </FilesMatch>
    
    <Files ~ (\.user.ini|\.htaccess|\.git|\.env|\.svn|\.project|LICENSE|README.md|Cargo.toml|Cargo.lock)$>
        Require all denied
    </Files>
</VirtualHost>
```

### Option 3: With SSL/HTTPS (Production Recommended)

```apache
<VirtualHost *:443>
    ServerAdmin webmaster@synergyinfinity.id
    ServerName axum.synergyinfinity.id
    ServerAlias 41ecdf6f.axum.synergyinfinity.id
    
    ErrorLog "/www/wwwlogs/axum.synergyinfinity.id-error_log"
    CustomLog "/www/wwwlogs/axum.synergyinfinity.id-access_log" combined

    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /path/to/cert.pem
    SSLCertificateKeyFile /path/to/key.pem
    SSLCertificateChainFile /path/to/chain.pem
    
    # Enable proxy modules
    ProxyPreserveHost On
    ProxyRequests Off
    
    # Reverse proxy to Axum backend
    ProxyPass / http://127.0.0.1:8080/
    ProxyPassReverse / http://127.0.0.1:8080/
    
    # Proxy headers (HTTPS)
    RequestHeader set X-Forwarded-Proto "https"
    RequestHeader set X-Forwarded-Port "443"
    RequestHeader set X-Real-IP %{REMOTE_ADDR}s
    
    # Security headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "DENY"
    Header always set X-XSS-Protection "1; mode=block"
</VirtualHost>

# Redirect HTTP to HTTPS
<VirtualHost *:80>
    ServerName axum.synergyinfinity.id
    ServerAlias 41ecdf6f.axum.synergyinfinity.id
    
    RewriteEngine On
    RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]
</VirtualHost>
```

## 🔧 Apache Modules Required

Enable these Apache modules:

```bash
# Enable required modules
a2enmod proxy
a2enmod proxy_http
a2enmod proxy_wstunnel  # For WebSocket support
a2enmod headers
a2enmod rewrite
a2enmod ssl  # For HTTPS

# Restart Apache
systemctl restart apache2
# Or for some systems:
service httpd restart
```

## 📋 Configuration File Location

**Debian/Ubuntu:**
```bash
/etc/apache2/sites-available/axum.synergyinfinity.id.conf
```

**CentOS/RHEL:**
```bash
/etc/httpd/conf.d/axum.synergyinfinity.id.conf
```

**aaPanel/BT Panel:**
```bash
/www/server/panel/vhost/apache/axum.synergyinfinity.id.conf
```

## 🚀 Deployment Steps

### 1. Update .env for Production

```bash
# .env
ENVIRONMENT=production
HOST=127.0.0.1  # Or 0.0.0.0
PORT=8080

# CORS with your domain
CORS_ORIGINS=http://axum.synergyinfinity.id,https://axum.synergyinfinity.id,http://41ecdf6f.axum.synergyinfinity.id,https://41ecdf6f.axum.synergyinfinity.id

# Database
DATABASE_URL=mysql://axum:rahasia123@localhost:3306/my_axum_db

# JWT Secret (CHANGE THIS!)
JWT_SECRET=your-production-secret-minimum-32-characters-long
BCRYPT_COST=12

# Logging
RUST_LOG=info
```

### 2. Build Axum Application

```bash
# Build release version
cargo build --release

# Binary will be at:
# target/release/my-axum-app
```

### 3. Create Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/axum-api.service
```

```ini
[Unit]
Description=Axum API Service
After=network.target mysql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/www/wwwroot/axum-backend
Environment="RUST_LOG=info"
ExecStart=/www/wwwroot/axum-backend/target/release/my-axum-app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable axum-api
sudo systemctl start axum-api
sudo systemctl status axum-api
```

### 4. Configure Apache VirtualHost

```bash
# Edit/create vhost file
nano /www/server/panel/vhost/apache/axum.synergyinfinity.id.conf

# Copy one of the configurations above (Option 1 recommended)

# Test Apache configuration
apachectl configtest

# Restart Apache
systemctl restart apache2
# or
service httpd restart
```

### 5. Test Deployment

```bash
# Test local Axum
curl http://127.0.0.1:8080/health

# Test via Apache
curl http://axum.synergyinfinity.id/health

# Test API endpoint
curl http://axum.synergyinfinity.id/api/auth/login
```

## 🧪 Troubleshooting

### Issue 1: 502 Bad Gateway

**Cause:** Axum service not running

**Solution:**
```bash
# Check Axum service
systemctl status axum-api

# Check if port 8080 is listening
netstat -tulpn | grep 8080
ss -tulpn | grep 8080

# Restart service
systemctl restart axum-api
```

### Issue 2: CORS Errors

**Cause:** CORS_ORIGINS not configured correctly

**Solution:**
```bash
# Update .env
CORS_ORIGINS=http://axum.synergyinfinity.id,https://axum.synergyinfinity.id

# Restart Axum service
systemctl restart axum-api
```

### Issue 3: 404 Not Found

**Cause:** ProxyPass not configured

**Solution:**
Check Apache vhost has:
```apache
ProxyPass / http://127.0.0.1:8080/
ProxyPassReverse / http://127.0.0.1:8080/
```

### Issue 4: Apache Won't Start

**Cause:** Module not enabled

**Solution:**
```bash
# Enable proxy modules
a2enmod proxy proxy_http headers rewrite

# Restart Apache
systemctl restart apache2
```

## 📊 Testing Checklist

- [ ] Axum service running on port 8080
- [ ] Apache modules enabled (proxy, proxy_http, headers, rewrite)
- [ ] VirtualHost configured correctly
- [ ] CORS_ORIGINS includes your domain
- [ ] DNS pointing to your server
- [ ] Firewall allows port 80/443
- [ ] `/health` endpoint accessible
- [ ] `/api/auth/login` endpoint works
- [ ] Static files served (if applicable)
- [ ] SSL certificate installed (for HTTPS)

## 🔒 Security Recommendations

1. **Use HTTPS in production** (Option 3 configuration)
2. **Change JWT_SECRET** to strong random value
3. **Set specific CORS_ORIGINS** (no wildcard `*`)
4. **Enable firewall** to only allow necessary ports
5. **Use strong database passwords**
6. **Keep Rust and dependencies updated**
7. **Monitor logs** regularly

## 📝 Log Files

```bash
# Apache logs
tail -f /www/wwwlogs/axum.synergyinfinity.id-error_log
tail -f /www/wwwlogs/axum.synergyinfinity.id-access_log

# Axum logs (via systemd)
journalctl -u axum-api -f

# Or if using PM2/other process manager
pm2 logs axum-api
```

## 🎯 Performance Optimization

```apache
# Add to VirtualHost
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json
</IfModule>

# Cache static assets
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
</IfModule>
```

## 🌟 Final Configuration Summary

**Recommended for your setup:**

```apache
<VirtualHost *:80>
    ServerAdmin webmaster@synergyinfinity.id
    ServerName axum.synergyinfinity.id
    ServerAlias 41ecdf6f.axum.synergyinfinity.id
    
    ErrorLog "/www/wwwlogs/axum.synergyinfinity.id-error_log"
    CustomLog "/www/wwwlogs/axum.synergyinfinity.id-access_log" combined

    ProxyPreserveHost On
    ProxyRequests Off
    
    ProxyPass / http://127.0.0.1:8080/
    ProxyPassReverse / http://127.0.0.1:8080/
    
    RequestHeader set X-Forwarded-Proto "http"
    RequestHeader set X-Real-IP %{REMOTE_ADDR}s
    
    ProxyTimeout 300
</VirtualHost>
```

**Don't forget to:**
1. Enable Apache proxy modules
2. Update `.env` with domain CORS
3. Build and run Axum service
4. Restart Apache

Your API will be accessible at: `http://axum.synergyinfinity.id`
