use axum::{Router, routing::get, middleware::from_fn_with_state, middleware::from_fn};
use tokio::net::TcpListener;
use std::env;
use tower_http::cors::{CorsLayer, Any};
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
// Returns (origins, is_wildcard)
fn get_cors_origins() -> (Vec<HeaderValue>, bool) {
    if let Ok(origins_str) = env::var("CORS_ORIGINS") {
        let trimmed = origins_str.trim();
        
        // Check if wildcard
        if trimmed == "*" {
            println!("⚠️  WARNING: CORS set to allow ALL origins (*)");
            println!("⚠️  This is NOT secure for production!");
            println!("⚠️  Credentials will be DISABLED for security");
            return (vec![HeaderValue::from_static("*")], true);
        }
        
        // Parse comma-separated origins
        let mut valid_origins = Vec::new();
        for origin in trimmed.split(',') {
            let origin = origin.trim();
            if !origin.is_empty() {
                match origin.parse::<HeaderValue>() {
                    Ok(header_value) => {
                        valid_origins.push(header_value);
                        println!("✅ CORS origin added: {}", origin);
                    }
                    Err(e) => {
                        eprintln!("⚠️  Invalid CORS origin '{}': {}", origin, e);
                    }
                }
            }
        }
        
        if !valid_origins.is_empty() {
            return (valid_origins, false);
        }
    }

    // Fallback based on environment
    let environment = env::var("ENVIRONMENT").unwrap_or_else(|_| "development".to_string());
    
    if environment == "production" {
        println!("⚠️  Production mode: Using restricted CORS (localhost only)");
        println!("⚠️  Please set CORS_ORIGINS in .env for production!");
    } else {
        println!("ℹ️  Development mode: Using default CORS origins");
    }
    
    // Default development origins
    let defaults = vec![
        "https://nextjs.synergyinfinity.id/".parse().unwrap(),
        "http://localhost:5173".parse().unwrap(),
        "http://nextjs.synergyinfinity.id/".parse().unwrap(),
    ];
    
    (defaults, false)
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
        .with_state(db);
        // Add CORS layer to allow frontend requests
        /**
        .layer({
            let (cors_origins, is_wildcard) = get_cors_origins();
            
            if is_wildcard {
                // Wildcard mode - allow any origin (NOT for production!)
                CorsLayer::new()
                    .allow_origin(Any)
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
                        HeaderName::from_static("x-csrf-token"),
                    ])
                    .allow_credentials(false)  // MUST be false with Any origin
            } else {
                // Specific origins mode (recommended)
                CorsLayer::new()
                    .allow_origin(cors_origins)
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
                        HeaderName::from_static("x-csrf-token"),
                    ])
                    .allow_credentials(true)
            }
        })
         */
        

    // Get host and port from environment or use defaults
    let host = env::var("HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
    let port = env::var("PORT").unwrap_or_else(|_| "8080".to_string());
    let bind_addr = format!("{}:{}", host, port);

    // Run it with hyper
    let listener = TcpListener::bind(&bind_addr).await.unwrap();
    println!("🚀 Server running on http://{}", bind_addr);
    axum::serve(listener, app).await.unwrap();
}
