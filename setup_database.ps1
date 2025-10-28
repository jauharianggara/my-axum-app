# Script untuk menjalankan database migrations
Write-Host "🔄 Running database migrations..." -ForegroundColor Yellow

# Buat database jika belum ada
Write-Host "📋 Creating database if not exists..." -ForegroundColor Blue
$createDbCommand = @"
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS my_axum_db;"
"@

try {
    Invoke-Expression $createDbCommand
    Write-Host "✅ Database creation completed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Database creation skipped (already exists or manual creation required)" -ForegroundColor Yellow
}

# Jalankan migrations
Write-Host "🔄 Running migrations..." -ForegroundColor Blue
Set-Location migration
$env:DATABASE_URL = "mysql://root:password@localhost:3306/my_axum_db"

try {
    cargo run -- migrate up
    Write-Host "✅ Migrations completed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Migration failed: $_" -ForegroundColor Red
    Write-Host "💡 Please ensure:" -ForegroundColor Yellow
    Write-Host "   - MySQL server is running" -ForegroundColor Yellow
    Write-Host "   - Database credentials are correct in .env file" -ForegroundColor Yellow
    Write-Host "   - Database 'my_axum_db' exists" -ForegroundColor Yellow
    exit 1
}

Set-Location ..
Write-Host "🎉 Database setup completed!" -ForegroundColor Green