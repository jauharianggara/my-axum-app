#!/bin/bash

# Deployment Script for Axum API on Production Server
# Domain: axum.synergyinfinity.id

set -e

echo "=================================================="
echo "  Axum API Deployment Script"
echo "=================================================="
echo ""

# Configuration
APP_DIR="/www/wwwroot/axum-backend"
SERVICE_NAME="axum-api"
VHOST_FILE="/www/server/panel/vhost/apache/axum.synergyinfinity.id.conf"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Building Axum application...${NC}"
cargo build --release
echo -e "${GREEN}✓ Build completed${NC}"
echo ""

echo -e "${YELLOW}Step 2: Creating application directory...${NC}"
sudo mkdir -p $APP_DIR
sudo cp -r . $APP_DIR/
sudo chown -R www-data:www-data $APP_DIR
echo -e "${GREEN}✓ Files copied${NC}"
echo ""

echo -e "${YELLOW}Step 3: Installing systemd service...${NC}"
sudo cp axum-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
echo -e "${GREEN}✓ Service installed${NC}"
echo ""

echo -e "${YELLOW}Step 4: Configuring Apache...${NC}"
# Check if Apache modules are enabled
if ! apache2ctl -M 2>/dev/null | grep -q proxy_module; then
    echo "Enabling Apache modules..."
    sudo a2enmod proxy proxy_http headers rewrite ssl
    echo -e "${GREEN}✓ Modules enabled${NC}"
else
    echo -e "${GREEN}✓ Modules already enabled${NC}"
fi

# Copy vhost configuration
sudo cp apache-vhost.conf $VHOST_FILE

# Test Apache configuration
if sudo apachectl configtest 2>&1 | grep -q "Syntax OK"; then
    echo -e "${GREEN}✓ Apache configuration valid${NC}"
else
    echo -e "${RED}✗ Apache configuration error${NC}"
    exit 1
fi
echo ""

echo -e "${YELLOW}Step 5: Starting services...${NC}"
# Start Axum service
sudo systemctl start $SERVICE_NAME

# Wait for service to start
sleep 3

# Check service status
if systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${GREEN}✓ Axum service started${NC}"
else
    echo -e "${RED}✗ Axum service failed to start${NC}"
    echo "Check logs: journalctl -u $SERVICE_NAME -n 50"
    exit 1
fi

# Restart Apache
sudo systemctl restart apache2
echo -e "${GREEN}✓ Apache restarted${NC}"
echo ""

echo -e "${YELLOW}Step 6: Verifying deployment...${NC}"
# Test local Axum
if curl -s http://127.0.0.1:8080/health > /dev/null; then
    echo -e "${GREEN}✓ Axum backend responding${NC}"
else
    echo -e "${RED}✗ Axum backend not responding${NC}"
fi

# Test via Apache
if curl -s http://axum.synergyinfinity.id/health > /dev/null; then
    echo -e "${GREEN}✓ Apache reverse proxy working${NC}"
else
    echo -e "${YELLOW}⚠ Apache proxy might need DNS propagation${NC}"
fi
echo ""

echo "=================================================="
echo -e "${GREEN}Deployment completed!${NC}"
echo "=================================================="
echo ""
echo "Service Status:"
sudo systemctl status $SERVICE_NAME --no-pager
echo ""
echo "Useful Commands:"
echo "  - View logs: journalctl -u $SERVICE_NAME -f"
echo "  - Restart: sudo systemctl restart $SERVICE_NAME"
echo "  - Stop: sudo systemctl stop $SERVICE_NAME"
echo "  - Apache logs: tail -f /www/wwwlogs/axum.synergyinfinity.id-error_log"
echo ""
echo "API URLs:"
echo "  - Health: http://axum.synergyinfinity.id/health"
echo "  - Login: http://axum.synergyinfinity.id/api/auth/login"
echo ""
