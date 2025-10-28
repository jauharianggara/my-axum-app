-- Initialize database
CREATE DATABASE IF NOT EXISTS my_axum_db;
USE my_axum_db;

-- Grant privileges to user
GRANT ALL PRIVILEGES ON my_axum_db.* TO 'axum'@'%';
FLUSH PRIVILEGES;