use axum::{Router, routing::get, middleware::from_fn_with_state, middleware::from_fn};
use tokio::net::TcpListener;
use std::env;
use tower_http::cors::CorsLayer;
use axum::http::{Method, HeaderValue, HeaderName};

// Import modules
mod database;
mod handlers;
mod models;
mod routes;
mod validators;
mod services;
mod middleware;

use database::establish_connection;
use handlers::health::health_check;
use routes::{create_kantor_routes, create_karyawan_routes, public_auth_routes, auth_routes, jabatan_routes};
use middleware::auth::jwt_auth_layer;
use middleware::security::{security_headers, csrf_protection};

// Helper function to get CORS origins from environment variables
fn get_cors_origins() -> Vec<HeaderValue> {
    let cors_origins = env::var("CORS_ORIGINS")
        .unwrap_or_else(|_| {
            // Default values based on environment
            if env::var("ENVIRONMENT").unwrap_or_default() == "production" {
                "https://yourdomain.com,https://www.yourdomain.com".to_string()
            } else {
                "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000".to_string()
            }
        });

    cors_origins
        .split(',')
        .filter_map(|origin| {
            let trimmed = origin.trim();
            if !trimmed.is_empty() {
                match trimmed.parse::<HeaderValue>() {
                    Ok(header_value) => Some(header_value),
                    Err(e) => {
                        eprintln!("⚠️ Invalid CORS origin '{}': {}", trimmed, e);
                        None
                    }
                }
            } else {
                None
            }
        })
        .collect()
}

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
        .nest_service("/uploads", tower_http::services::ServeDir::new("uploads"))
        // Public authentication routes (no auth required)
        .nest("/api/auth", public_auth_routes())
        // Protected authentication routes (auth required)  
        .nest("/api/user", auth_routes())
        // Protected API routes (auth required)
        .nest(
            "/api/karyawans", 
            create_karyawan_routes()
                .layer(from_fn_with_state(db.clone(), jwt_auth_layer))
        )
        .nest(
            "/api/kantors", 
            create_kantor_routes()
                .layer(from_fn_with_state(db.clone(), jwt_auth_layer))
        )
        .nest(
            "/api/jabatans", 
            jabatan_routes(db.clone())
        )
        // Security middleware layers (applied in reverse order)
        .layer(from_fn(security_headers))  // Security headers
        .layer(from_fn(csrf_protection))   // CSRF protection
        // Add CORS layer to allow frontend requests
        .layer(
            CorsLayer::new()
                .allow_origin(get_cors_origins())
                .allow_methods([
                    Method::GET,
                    Method::POST,
                    Method::PUT,
                    Method::DELETE,
                    Method::OPTIONS,
                ])
                .allow_headers([
                    HeaderName::from_static("authorization"),
                    HeaderName::from_static("content-type"),
                    HeaderName::from_static("accept"),
                    HeaderName::from_static("x-csrf-token"),  // Allow CSRF token header
                ])
                .allow_credentials(true)
        )
        .with_state(db);

    // Get host and port from environment or use defaults
    let host = env::var("HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
    let port = env::var("PORT").unwrap_or_else(|_| "8080".to_string());
    let bind_addr = format!("{}:{}", host, port);

    // Run it with hyper
    let listener = TcpListener::bind(&bind_addr).await.unwrap();
    println!("🚀 Server running on http://{}", bind_addr);
    axum::serve(listener, app).await.unwrap();
}
