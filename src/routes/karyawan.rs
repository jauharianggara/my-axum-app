use axum::{
    routing::{get, post, put, delete},
    Router,
};
use sea_orm::DatabaseConnection;
use crate::handlers::karyawan::{
    get_all_karyawan,
    get_all_karyawan_with_kantor,
    get_karyawan_by_id,
    get_karyawan_with_kantor_by_id,
    create_karyawan,
    create_karyawan_with_photo,
    upload_karyawan_photo,
    delete_karyawan_photo,
    update_karyawan,
    delete_karyawan,
};

pub fn create_karyawan_routes() -> Router<DatabaseConnection> {
    Router::new()
        .route("/", get(get_all_karyawan))
        .route("/with-kantor", get(get_all_karyawan_with_kantor))
        .route("/:id", get(get_karyawan_by_id))
        .route("/:id/with-kantor", get(get_karyawan_with_kantor_by_id))
        .route("/", post(create_karyawan))
        .route("/with-photo", post(create_karyawan_with_photo))
        .route("/:id/photo", post(upload_karyawan_photo))
        .route("/:id/photo", delete(delete_karyawan_photo))
        .route("/:id", put(update_karyawan))
        .route("/:id", delete(delete_karyawan))
}