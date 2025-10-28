use axum::{
    Router,
    routing::get,
};
use tokio::net::TcpListener;

// Import modules
mod models;
mod handlers;
mod validators;
mod routes;

use routes::create_karyawan_routes;
use handlers::health::health_check;

#[tokio::main]
async fn main() {
    // Build our application with routes
    let app = Router::new()
        .route("/", get(|| async { "Hello, World!" }))
        .route("/health", get(health_check))
        .nest("/api/karyawans", create_karyawan_routes())
        .nest("/api/kantors", routes::create_kantor_routes());

    // Run it with hyper on `0.0.0.0:8080`
    let listener = TcpListener::bind("0.0.0.0:8080").await.unwrap();
    println!("🚀 Server running on http://0.0.0.0:8080");
    axum::serve(listener, app).await.unwrap();
}
