use axum::{
    extract::{Request, State},
    http::StatusCode,
    middleware::Next,
    response::Response,
    Json,
};
use sea_orm::{DatabaseConnection, EntityTrait};

use crate::{
    models::{common::ApiResponse, user::Entity as UserEntity},
    services::auth::JwtService,
};

pub async fn jwt_auth_layer(
    State(db): State<DatabaseConnection>,
    request: Request,
    next: Next,
) -> Result<Response, (StatusCode, Json<ApiResponse<()>>)> {
    // Try to extract authorization header
    let auth_header = request
        .headers()
        .get(axum::http::header::AUTHORIZATION)
        .and_then(|header| header.to_str().ok())
        .and_then(|header| {
            if header.starts_with("Bearer ") {
                Some(header.trim_start_matches("Bearer "))
            } else {
                None
            }
        });

    let token = match auth_header {
        Some(token) => token,
        None => {
            return Err((
                StatusCode::UNAUTHORIZED,
                Json(ApiResponse::error(
                    "Unauthorized".to_string(),
                    vec!["Missing authorization header".to_string()],
                )),
            ));
        }
    };

    // Initialize JWT service
    let jwt_service = match JwtService::new() {
        Ok(service) => service,
        Err(_) => {
            return Err((
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(ApiResponse::error(
                    "Authentication error".to_string(),
                    vec!["JWT service initialization failed".to_string()],
                )),
            ));
        }
    };

    // Verify and extract user ID from token
    let user_id = match jwt_service.extract_user_id(token) {
        Ok(id) => id,
        Err(_) => {
            return Err((
                StatusCode::UNAUTHORIZED,
                Json(ApiResponse::error(
                    "Unauthorized".to_string(),
                    vec!["Invalid or expired token".to_string()],
                )),
            ));
        }
    };

    // Fetch user from database
    let user = match UserEntity::find_by_id(user_id).one(&db).await {
        Ok(Some(user)) => user,
        Ok(None) => {
            return Err((
                StatusCode::UNAUTHORIZED,
                Json(ApiResponse::error(
                    "Unauthorized".to_string(),
                    vec!["User not found".to_string()],
                )),
            ));
        }
        Err(_) => {
            return Err((
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(ApiResponse::error(
                    "Authentication error".to_string(),
                    vec!["Database error".to_string()],
                )),
            ));
        }
    };

    // Check if user is active
    if !user.is_active {
        return Err((
            StatusCode::FORBIDDEN,
            Json(ApiResponse::error(
                "Forbidden".to_string(),
                vec!["Account is not active".to_string()],
            )),
        ));
    }

    // Add user to request extensions
    let mut request = request;
    request.extensions_mut().insert(user);

    Ok(next.run(request).await)
}