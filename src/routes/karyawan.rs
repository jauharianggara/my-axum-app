use axum::{
    routing::{get, post, put, delete},
    Router,
};
use crate::handlers::karyawan::{
    get_all_karyawan,
    get_karyawan_by_id,
    create_karyawan,
    update_karyawan,
    delete_karyawan,
};

pub fn create_karyawan_routes() -> Router {
    Router::new()
        .route("/", get(get_all_karyawan))
        .route("/{id}", get(get_karyawan_by_id))
        .route("/", post(create_karyawan))
        .route("/{id}", put(update_karyawan))
        .route("/{id}", delete(delete_karyawan))
}