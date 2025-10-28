use validator::ValidationError;

pub fn validate_id(id_str: &str) -> Result<u32, String> {
    match id_str.parse::<u32>() {
        Ok(id) => Ok(id),
        Err(_) => Err("ID harus berupa angka positif yang valid".to_string()),
    }
}

pub fn validate_longitude(longitude: f64) -> Result<(), validator::ValidationError> {
    if longitude >= -180.0 && longitude <= 180.0 {
        Ok(())
    } else {
        let mut error = ValidationError::new("range");
        error.message = Some("Longitude harus antara -180 hingga 180".into());
        Err(error)
    }
}

pub fn validate_latitude(latitude: f64) -> Result<(), validator::ValidationError> {
    if latitude >= -90.0 && latitude <= 90.0 {
        Ok(())
    } else {
        let mut error = ValidationError::new("range");
        error.message = Some("Latitude harus antara -90 hingga 90".into());
        Err(error)
    }
}

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
