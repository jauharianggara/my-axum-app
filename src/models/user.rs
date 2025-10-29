use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Eq, Serialize, Deserialize)]
#[sea_orm(table_name = "users")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i32,
    #[sea_orm(unique)]
    pub username: String,
    #[sea_orm(unique)]
    pub email: String,
    pub password_hash: String,
    pub full_name: Option<String>,
    pub is_active: bool,
    pub created_at: DateTime,
    pub updated_at: DateTime,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}

// Request/Response DTOs
#[derive(Debug, Deserialize, Validate)]
pub struct RegisterRequest {
    #[validate(length(min = 3, max = 50, message = "Username harus antara 3-50 karakter"))]
    pub username: String,
    
    #[validate(email(message = "Format email tidak valid"))]
    pub email: String,
    
    #[validate(length(min = 6, message = "Password minimal 6 karakter"))]
    pub password: String,
    
    #[validate(length(min = 2, max = 100, message = "Nama lengkap harus antara 2-100 karakter"))]
    pub full_name: Option<String>,
}

#[derive(Debug, Deserialize, Validate)]
pub struct LoginRequest {
    #[validate(length(min = 1, message = "Username/email tidak boleh kosong"))]
    pub username_or_email: String,
    
    #[validate(length(min = 1, message = "Password tidak boleh kosong"))]
    pub password: String,
}

#[derive(Debug, Serialize)]
pub struct UserResponse {
    pub id: i32,
    pub username: String,
    pub email: String,
    pub full_name: Option<String>,
    pub is_active: bool,
    pub created_at: DateTime,
}

#[derive(Debug, Serialize)]
pub struct LoginResponse {
    pub user: UserResponse,
    pub token: String,
    pub expires_in: i64,
}

impl From<Model> for UserResponse {
    fn from(user: Model) -> Self {
        Self {
            id: user.id,
            username: user.username,
            email: user.email,
            full_name: user.full_name,
            is_active: user.is_active,
            created_at: user.created_at,
        }
    }
}