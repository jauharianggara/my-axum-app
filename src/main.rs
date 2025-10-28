use axum::{Router, routing::get, Extension};
use tokio::net::TcpListener;
use std::env;

// Import modules
mod database;
mod handlers;
mod models;
mod routes;
mod validators;

use database::establish_connection;
use handlers::health::health_check;
use routes::create_kantor_routes;
use routes::create_karyawan_routes;

#[tokio::main]
async fn main() {
    // Load environment variables
    dotenvy::dotenv().ok();
    
    // Establish database connection
    let db = match establish_connection().await {
        Ok(connection) => {
            println!("✅ Database connected successfully");
            connection
        }
        Err(err) => {
            eprintln!("❌ Failed to connect to database: {}", err);
            std::process::exit(1);
        }
    };

    // Build our application with routes
    let app = Router::new()
        .route("/", get(|| async { "Hello, World!" }))
        .route("/health", get(health_check))
        .nest("/api/karyawans", create_karyawan_routes())
        .nest("/api/kantors", create_kantor_routes())
        .layer(Extension(db));

    // Get host and port from environment or use defaults
    let host = env::var("HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
    let port = env::var("PORT").unwrap_or_else(|_| "8080".to_string());
    let bind_addr = format!("{}:{}", host, port);

    // Run it with hyper
    let listener = TcpListener::bind(&bind_addr).await.unwrap();
    println!("🚀 Server running on http://{}", bind_addr);
    axum::serve(listener, app).await.unwrap();
}
