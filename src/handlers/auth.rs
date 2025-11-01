use axum::{
    extract::{Request, State},
    http::StatusCode,
    Json,
};
use sea_orm::{
    ActiveModelTrait, ColumnTrait, DatabaseConnection, EntityTrait, QueryFilter, Set,
};
use validator::Validate;

use crate::{
    models::{
        common::ApiResponse,
        user::{
            Entity as UserEntity, LoginRequest, LoginResponse, RegisterRequest, UserResponse,
            Model as UserModel,
        },
    },
    services::auth::{JwtService, PasswordService},
    validators::security::SecurityValidator,
};

pub async fn register(
    State(db): State<DatabaseConnection>,
    Json(request): Json<RegisterRequest>,
) -> Result<Json<ApiResponse<UserResponse>>, (StatusCode, Json<ApiResponse<()>>)> {
    // Validate request
    if let Err(errors) = request.validate() {
        let error_messages: Vec<String> = errors
            .field_errors()
            .iter()
            .flat_map(|(_, field_errors)| {
                field_errors.iter().map(|error| {
                    error.message.clone().unwrap_or_else(|| "Validation error".into()).to_string()
                })
            })
            .collect();

        return Err((
            StatusCode::BAD_REQUEST,
            Json(ApiResponse::error(
                "Validation failed".to_string(),
                error_messages,
            )),
        ));
    }

    // Security validation
    let sanitized_username = match SecurityValidator::validate_username(&request.username) {
        Ok(username) => username,
        Err(_) => {
            return Err((
                StatusCode::BAD_REQUEST,
                Json(ApiResponse::error(
                    "Security validation failed".to_string(),
                    vec!["Username contains invalid characters or security threats".to_string()],
                )),
            ));
        }
    };

    let sanitized_email = match SecurityValidator::validate_email(&request.email) {
        Ok(email) => email,
        Err(_) => {
            return Err((
                StatusCode::BAD_REQUEST,
                Json(ApiResponse::error(
                    "Security validation failed".to_string(),
                    vec!["Email format is invalid or contains security threats".to_string()],
                )),
            ));
        }
    };

    let sanitized_full_name = match &request.full_name {
        Some(name) => match SecurityValidator::sanitize_string(name) {
            Ok(sanitized) => Some(sanitized),
            Err(_) => {
                return Err((
                    StatusCode::BAD_REQUEST,
                    Json(ApiResponse::error(
                        "Security validation failed".to_string(),
                        vec!["Full name contains security threats".to_string()],
                    )),
                ));
            }
        },
        None => None,
    };

    // Check if username already exists
    if let Ok(Some(_)) = UserEntity::find()
        .filter(crate::models::user::Column::Username.eq(&sanitized_username))
        .one(&db)
        .await
    {
        return Err((
            StatusCode::CONFLICT,
            Json(ApiResponse::error(
                "Registration failed".to_string(),
                vec!["Username sudah digunakan".to_string()],
            )),
        ));
    }

    // Check if email already exists
    if let Ok(Some(_)) = UserEntity::find()
        .filter(crate::models::user::Column::Email.eq(&sanitized_email))
        .one(&db)
        .await
    {
        return Err((
            StatusCode::CONFLICT,
            Json(ApiResponse::error(
                "Registration failed".to_string(),
                vec!["Email sudah digunakan".to_string()],
            )),
        ));
    }

    // Hash password
    let password_hash = match PasswordService::hash_password(&request.password) {
        Ok(hash) => hash,
        Err(_) => {
            return Err((
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(ApiResponse::error(
                    "Registration failed".to_string(),
                    vec!["Failed to process password".to_string()],
                )),
            ));
        }
    };

    // Create new user
    let new_user = crate::models::user::ActiveModel {
        username: Set(sanitized_username),
        email: Set(sanitized_email),
        password_hash: Set(password_hash),
        full_name: Set(sanitized_full_name),
        is_active: Set(true),
        ..Default::default()
    };

    match new_user.insert(&db).await {
        Ok(user) => {
            let user_response = UserResponse::from(user);
            Ok(Json(ApiResponse::success(
                "User registered successfully".to_string(),
                user_response,
            )))
        }
        Err(err) => {
            eprintln!("Database error during registration: {}", err);
            Err((
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(ApiResponse::error(
                    "Registration failed".to_string(),
                    vec!["Failed to create user".to_string()],
                )),
            ))
        }
    }
}

pub async fn login(
    State(db): State<DatabaseConnection>,
    Json(request): Json<LoginRequest>,
) -> Result<Json<ApiResponse<LoginResponse>>, (StatusCode, Json<ApiResponse<()>>)> {
    // Validate request
    if let Err(errors) = request.validate() {
        let error_messages: Vec<String> = errors
            .field_errors()
            .iter()
            .flat_map(|(_, field_errors)| {
                field_errors.iter().map(|error| {
                    error.message.clone().unwrap_or_else(|| "Validation error".into()).to_string()
                })
            })
            .collect();

        return Err((
            StatusCode::BAD_REQUEST,
            Json(ApiResponse::error(
                "Validation failed".to_string(),
                error_messages,
            )),
        ));
    }

    // Find user by username or email
    let user = UserEntity::find()
        .filter(
            crate::models::user::Column::Username
                .eq(&request.username_or_email)
                .or(crate::models::user::Column::Email.eq(&request.username_or_email)),
        )
        .one(&db)
        .await;

    let user = match user {
        Ok(Some(user)) => user,
        Ok(None) => {
            return Err((
                StatusCode::UNAUTHORIZED,
                Json(ApiResponse::error(
                    "Login failed".to_string(),
                    vec!["Username/email atau password salah".to_string()],
                )),
            ));
        }
        Err(err) => {
            eprintln!("Database error during login: {}", err);
            return Err((
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(ApiResponse::error(
                    "Login failed".to_string(),
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
                "Login failed".to_string(),
                vec!["Account is not active".to_string()],
            )),
        ));
    }

    // Verify password
    match PasswordService::verify_password(&request.password, &user.password_hash) {
        Ok(true) => {
            // Generate JWT token
            let jwt_service = match JwtService::new() {
                Ok(service) => service,
                Err(_) => {
                    return Err((
                        StatusCode::INTERNAL_SERVER_ERROR,
                        Json(ApiResponse::error(
                            "Login failed".to_string(),
                            vec!["Token generation error".to_string()],
                        )),
                    ));
                }
            };

            let token = match jwt_service.generate_token(user.id, &user.username, &user.email) {
                Ok(token) => token,
                Err(_) => {
                    return Err((
                        StatusCode::INTERNAL_SERVER_ERROR,
                        Json(ApiResponse::error(
                            "Login failed".to_string(),
                            vec!["Token generation failed".to_string()],
                        )),
                    ));
                }
            };

            let user_response = UserResponse::from(user);
            let expires_in = JwtService::get_token_expiry_hours() * 3600; // Convert to seconds

            let login_response = LoginResponse {
                user: user_response,
                token,
                expires_in,
            };

            Ok(Json(ApiResponse::success(
                "Login successful".to_string(),
                login_response,
            )))
        }
        Ok(false) => Err((
            StatusCode::UNAUTHORIZED,
            Json(ApiResponse::error(
                "Login failed".to_string(),
                vec!["Username/email atau password salah".to_string()],
            )),
        )),
        Err(_) => Err((
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ApiResponse::error(
                "Login failed".to_string(),
                vec!["Password verification failed".to_string()],
            )),
        )),
    }
}

pub async fn me(
    State(db): State<DatabaseConnection>,
    request: Request,
) -> Result<Json<ApiResponse<UserResponse>>, (StatusCode, Json<ApiResponse<()>>)> {
    // Extract authorization header
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

    let user_response = UserResponse::from(user);
    Ok(Json(ApiResponse::success(
        "User profile retrieved successfully".to_string(),
        user_response,
    )))
}