use std::{i32, u32};

use validator::ValidationError;

// Custom validation function untuk gaji
pub fn validate_gaji(gaji: &str) -> Result<(), ValidationError> {
    match gaji.parse::<u32>() {
        Ok(value) => {
            if value >= 1000000 && value <= 100000000 {
                Ok(())
            } else {
                let mut error = ValidationError::new("range");
                error.message = Some("Gaji harus antara 1,000,000 - 100,000,000".into());
                Err(error)
            }
        }
        Err(_) => {
            let mut error = ValidationError::new("invalid_number");
            error.message = Some("Gaji harus berupa angka yang valid".into());
            Err(error)
        }
    }
}

// Function untuk validasi ID
pub fn validate_id(id_str: &str) -> Result<i32, String> {
    match id_str.parse::<i32>() {
        Ok(id) if id > 0 => Ok(id),
        Ok(_) => Err("ID harus berupa angka positif yang valid".to_string()),
        Err(_) => Err("ID harus berupa angka positif yang valid".to_string())
    }
}

// Function untuk validasi kantor_id (optional)
pub fn validate_kantor_id(kantor_id: &str) -> Result<(), ValidationError> {
    // Allow empty string or "null" for optional kantor_id
    if kantor_id.is_empty() || kantor_id.trim().to_lowercase() == "null" {
        return Ok(());
    }
    
    match kantor_id.parse::<i32>() {
        Ok(id) if id > 0 => Ok(()),
        Ok(_) => {
            let mut error = ValidationError::new("invalid_kantor_id");
            error.message = Some("kantor_id harus berupa angka positif yang valid atau kosong untuk freelancer".into());
            Err(error)
        }
        Err(_) => {
            let mut error = ValidationError::new("invalid_kantor_id");
            error.message = Some("kantor_id harus berupa angka positif yang valid atau kosong untuk freelancer".into());
            Err(error)
        }
    }
}

// Function untuk menghandle validation errors
pub fn handle_validation_errors(validation_errors: validator::ValidationErrors) -> Vec<String> {
    validation_errors
        .field_errors()
        .iter()
        .flat_map(|(field, errors)| {
            errors.iter().map(move |error| {
                let message = if let Some(msg) = &error.message {
                    msg.to_string()
                } else {
                    "Invalid value".to_string()
                };
                format!("{}: {}", field, message)
            })
        })
        .collect()
}