use axum::{
    routing::{get, post, put, delete},
    Router,
    middleware::from_fn_with_state,
};
use sea_orm::DatabaseConnection;

use crate::handlers::jabatan::{
    get_all_jabatan, get_jabatan_by_id, create_jabatan, update_jabatan, delete_jabatan,
};
use crate::middleware::auth::jwt_auth_layer;

pub fn jabatan_routes(db: DatabaseConnection) -> Router<DatabaseConnection> {
    Router::new()
        .route("/", get(get_all_jabatan).post(create_jabatan))
        .route("/:id", get(get_jabatan_by_id).put(update_jabatan).delete(delete_jabatan))
        .layer(from_fn_with_state(db.clone(), jwt_auth_layer))
        .with_state(db)
}
