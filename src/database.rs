use sea_orm::{Database, DatabaseConnection, DbErr};
use std::env;

pub async fn establish_connection() -> Result<DatabaseConnection, DbErr> {
    // Load environment variables
    dotenvy::dotenv().ok();
    
    let database_url = env::var("DATABASE_URL")
        .unwrap_or_else(|_| "mysql://axum:rahasia123@localhost:3306/my_axum_db".to_string());
    
    println!("🔌 Connecting to database: {}", database_url.replace("://", "://***:***@"));
    
    Database::connect(&database_url).await
}

//pub type DatabasePool = DatabaseConnection;