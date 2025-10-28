use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct ApiResponse<T> {
    pub success: bool,
    pub message: String,
    pub data: Option<T>,
    pub errors: Option<Vec<String>>,
}

impl<T> ApiResponse<T> {
    pub fn success(message: String, data: T) -> Self {
        Self {
            success: true,
            message,
            data: Some(data),
            errors: None,
        }
    }
    
    pub fn error(message: String, errors: Vec<String>) -> Self {
        Self {
            success: false,
            message,
            data: None,
            errors: Some(errors),
        }
    }
}