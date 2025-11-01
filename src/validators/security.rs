use crate::middleware::security::sanitization::{
    contains_sql_injection_patterns, 
    contains_nosql_injection_patterns,
    is_valid_email,
    sanitize_html,
    escape_html
};
use validator::ValidationError;

/// Custom validator for SQL injection prevention
pub fn validate_no_sql_injection(value: &str) -> Result<(), ValidationError> {
    if contains_sql_injection_patterns(value) {
        return Err(ValidationError::new("sql_injection_detected"));
    }
    Ok(())
}

/// Custom validator for NoSQL injection prevention
pub fn validate_no_nosql_injection(value: &str) -> Result<(), ValidationError> {
    if contains_nosql_injection_patterns(value) {
        return Err(ValidationError::new("nosql_injection_detected"));
    }
    Ok(())
}

/// Custom validator for email format
pub fn validate_email_format(email: &str) -> Result<(), ValidationError> {
    if !is_valid_email(email) {
        return Err(ValidationError::new("invalid_email_format"));
    }
    Ok(())
}

/// Custom validator for safe HTML content
pub fn validate_safe_html(content: &str) -> Result<(), ValidationError> {
    let sanitized = sanitize_html(content);
    if sanitized != content {
        return Err(ValidationError::new("unsafe_html_content"));
    }
    Ok(())
}

/// Custom validator for username format (alphanumeric + underscore only)
pub fn validate_username_format(username: &str) -> Result<(), ValidationError> {
    let valid_chars = username.chars().all(|c| c.is_alphanumeric() || c == '_');
    if !valid_chars || username.is_empty() || username.len() > 50 {
        return Err(ValidationError::new("invalid_username_format"));
    }
    Ok(())
}

/// Custom validator for password strength
pub fn validate_password_strength(password: &str) -> Result<(), ValidationError> {
    if password.len() < 8 {
        return Err(ValidationError::new("password_too_short"));
    }
    
    let has_lowercase = password.chars().any(|c| c.is_lowercase());
    let has_uppercase = password.chars().any(|c| c.is_uppercase());
    let has_digit = password.chars().any(|c| c.is_numeric());
    
    if !has_lowercase || !has_uppercase || !has_digit {
        return Err(ValidationError::new("password_too_weak"));
    }
    
    Ok(())
}

/// Comprehensive input sanitization
pub struct SecurityValidator;

impl SecurityValidator {
    /// Sanitize and validate a string input
    pub fn sanitize_string(input: &str) -> Result<String, ValidationError> {
        // Check for injection patterns
        validate_no_sql_injection(input)?;
        validate_no_nosql_injection(input)?;
        
        // Escape HTML entities
        let escaped = escape_html(input);
        Ok(escaped)
    }
    
    /// Sanitize HTML content
    pub fn sanitize_html_content(input: &str) -> String {
        sanitize_html(input)
    }
    
    /// Validate and sanitize email
    pub fn validate_email(email: &str) -> Result<String, ValidationError> {
        let trimmed = email.trim().to_lowercase();
        validate_email_format(&trimmed)?;
        validate_no_sql_injection(&trimmed)?;
        Ok(trimmed)
    }
    
    /// Validate and sanitize username
    pub fn validate_username(username: &str) -> Result<String, ValidationError> {
        let trimmed = username.trim().to_lowercase();
        validate_username_format(&trimmed)?;
        validate_no_sql_injection(&trimmed)?;
        Ok(trimmed)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_sql_injection_validation() {
        assert!(validate_no_sql_injection("normal text").is_ok());
        assert!(validate_no_sql_injection("1' OR 1=1 --").is_err());
        assert!(validate_no_sql_injection("'; DROP TABLE users; --").is_err());
    }
    
    #[test]
    fn test_nosql_injection_validation() {
        assert!(validate_no_nosql_injection("normal text").is_ok());
        assert!(validate_no_nosql_injection("$where: function() { return true; }").is_err());
        assert!(validate_no_nosql_injection("{$gt: ''}").is_err());
    }
    
    #[test]
    fn test_email_validation() {
        assert!(validate_email_format("test@example.com").is_ok());
        assert!(validate_email_format("invalid-email").is_err());
        assert!(validate_email_format("test@").is_err());
    }
    
    #[test]
    fn test_username_validation() {
        assert!(validate_username_format("valid_user123").is_ok());
        assert!(validate_username_format("invalid-user!").is_err());
        assert!(validate_username_format("").is_err());
    }
    
    #[test]
    fn test_password_strength() {
        assert!(validate_password_strength("StrongPass123").is_ok());
        assert!(validate_password_strength("weak").is_err());
        assert!(validate_password_strength("nouppercase123").is_err());
        assert!(validate_password_strength("NOLOWERCASE123").is_err());
        assert!(validate_password_strength("NoDigits").is_err());
    }
    
    #[test]
    fn test_security_validator() {
        assert!(SecurityValidator::sanitize_string("normal text").is_ok());
        assert!(SecurityValidator::sanitize_string("1' OR 1=1 --").is_err());
        
        let email = SecurityValidator::validate_email("  TEST@Example.COM  ");
        assert!(email.is_ok());
        assert_eq!(email.unwrap(), "test@example.com");
        
        let username = SecurityValidator::validate_username("  TestUser123  ");
        assert!(username.is_ok());
        assert_eq!(username.unwrap(), "testuser123");
    }
}