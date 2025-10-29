use axum::{
    routing::{get, post},
    Router,
};
use sea_orm::DatabaseConnection;

use crate::handlers::auth;

pub fn public_auth_routes() -> Router<DatabaseConnection> {
    Router::new()
        .route("/register", post(auth::register))
        .route("/login", post(auth::login))
}

pub fn auth_routes() -> Router<DatabaseConnection> {
    Router::new()
        .route("/me", get(auth::me))
}