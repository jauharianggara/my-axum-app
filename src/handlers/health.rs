use axum::response::Json;

pub async fn health_check() -> Json<&'static str> {
    Json("🚀 Karyawan Management API - Server is running!")
}