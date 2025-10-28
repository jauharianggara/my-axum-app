# Docker Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- 8080 and 3306 ports available

## Quick Start

### 1. Build and Run with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f app
```

### 2. Build Docker Image Only
```bash
# Build the application image
docker build -t my-axum-app .

# Run with external MySQL
docker run -p 8080:8080 \
  -e DATABASE_URL=mysql://axum:rahasia123@host.docker.internal:3306/my_axum_db \
  my-axum-app
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | Required |
| `HOST` | Server bind address | 0.0.0.0 |
| `PORT` | Server port | 8080 |
| `RUST_LOG` | Log level | info |

## Docker Compose Services

### app
- **Port**: 8080
- **Health Check**: GET /health
- **Auto Migration**: Runs database migrations on startup

### db (MySQL)
- **Port**: 3306
- **Database**: my_axum_db
- **User**: axum
- **Password**: rahasia123
- **Health Check**: mysqladmin ping

## API Endpoints

After deployment, the API will be available at:
- Health Check: http://localhost:8080/health
- Karyawan: http://localhost:8080/api/karyawans
- Kantor: http://localhost:8080/api/kantors

## Useful Commands

```bash
# Stop services
docker-compose down

# Remove volumes (data will be lost)
docker-compose down -v

# Rebuild and restart
docker-compose up --build --force-recreate

# View application logs
docker-compose logs -f app

# View database logs
docker-compose logs -f db

# Execute commands in running container
docker-compose exec app /bin/bash
docker-compose exec db mysql -u axum -p my_axum_db

# Check container status
docker-compose ps
```

## Troubleshooting

### Migration Issues
If migrations fail:
```bash
# Check database connectivity
docker-compose exec app curl -f http://localhost:8080/health

# Run migration manually
docker-compose exec app /usr/local/bin/migration migrate up
```

### Database Connection Issues
```bash
# Check MySQL health
docker-compose exec db mysqladmin ping -u axum -p

# Check if database exists
docker-compose exec db mysql -u axum -p -e "SHOW DATABASES;"
```

### Container Issues
```bash
# Restart specific service
docker-compose restart app

# View container resources
docker stats
```

## Production Considerations

1. **Security**:
   - Change default passwords
   - Use secrets management
   - Enable SSL/TLS

2. **Performance**:
   - Use production MySQL configuration
   - Set appropriate resource limits
   - Enable connection pooling

3. **Monitoring**:
   - Add application metrics
   - Set up log aggregation
   - Configure alerts

4. **Backup**:
   - Regular database backups
   - Volume backup strategy
   - Disaster recovery plan