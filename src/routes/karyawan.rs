use axum::{
    routing::{get, post, put, delete},
    Router,
};
use crate::handlers::karyawan::{
    get_all_karyawan,
    get_all_karyawan_with_kantor,
    get_karyawan_by_id,
    get_karyawan_with_kantor_by_id,
    create_karyawan,
    update_karyawan,
    delete_karyawan,
};

pub fn create_karyawan_routes() -> Router {
    Router::new()
        .route("/", get(get_all_karyawan))
        .route("/with-kantor", get(get_all_karyawan_with_kantor))
        .route("/:id", get(get_karyawan_by_id))
        .route("/:id/with-kantor", get(get_karyawan_with_kantor_by_id))
        .route("/", post(create_karyawan))
        .route("/:id", put(update_karyawan))
        .route("/:id", delete(delete_karyawan))
}