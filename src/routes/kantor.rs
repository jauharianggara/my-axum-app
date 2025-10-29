use axum::{
    routing::{get, post, put, delete},
    Router,
};
use sea_orm::DatabaseConnection;
use crate::handlers::kantor::{
    get_all_kantor,
    get_kantor_by_id,
    create_kantor,
    update_kantor,
    delete_kantor,
};

pub fn create_kantor_routes() -> Router<DatabaseConnection> {
    Router::new()
        .route("/", get(get_all_kantor))
        .route("/:id", get(get_kantor_by_id))
        .route("/", post(create_kantor))
        .route("/:id", put(update_kantor))
        .route("/:id", delete(delete_kantor))
}