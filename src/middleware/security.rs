use axum::{
    body::Body,
    http::{header, HeaderMap, Request, Response, StatusCode},
    middleware::Next,
    response::IntoResponse,
    Json,
};
use std::time::Duration;
use tower::limit::RateLimitLayer;

/// Rate limiting configuration
pub fn rate_limit_layer() -> RateLimitLayer {
    // Allow 100 requests per minute
    RateLimitLayer::new(100, Duration::from_secs(60))
}

/// Security headers middleware
pub async fn security_headers(
    request: Request<Body>,
    next: Next,
) -> impl IntoResponse {
    let response = next.run(request).await;
    
    let (mut parts, body) = response.into_parts();
    
    // Add security headers
    parts.headers.insert(
        "X-Content-Type-Options",
        "nosniff".parse().unwrap(),
    );
    parts.headers.insert(
        "X-Frame-Options", 
        "DENY".parse().unwrap(),
    );
    parts.headers.insert(
        "X-XSS-Protection",
        "1; mode=block".parse().unwrap(),
    );
    parts.headers.insert(
        "Referrer-Policy",
        "strict-origin-when-cross-origin".parse().unwrap(),
    );
    parts.headers.insert(
        "Permissions-Policy",
        "camera=(), microphone=(), geolocation=()".parse().unwrap(),
    );
    // Content Security Policy
    parts.headers.insert(
        "Content-Security-Policy",
        "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'".parse().unwrap(),
    );
    
    // Add HSTS header for HTTPS (only in production)
    if let Ok(env) = std::env::var("ENVIRONMENT") {
        if env == "production" {
            parts.headers.insert(
                "Strict-Transport-Security",
                "max-age=31536000; includeSubDomains; preload".parse().unwrap(),
            );
        }
    }
    
    Response::from_parts(parts, body)
}

/// Input sanitization utilities
pub mod sanitization {
    use ammonia::Builder;
    use regex::Regex;
    use htmlescape;
    
    /// Clean HTML input to prevent XSS
    pub fn sanitize_html(input: &str) -> String {
        Builder::default()
            .clean(input)
            .to_string()
    }
    
    /// Escape HTML entities
    pub fn escape_html(input: &str) -> String {
        htmlescape::encode_minimal(input)
    }
    
    /// Basic SQL injection pattern detection (additional layer)
    pub fn contains_sql_injection_patterns(input: &str) -> bool {
        let patterns = [
            r"(?i)(union\s+select|or\s+1\s*=\s*1|and\s+1\s*=\s*1)",
            r"(?i)(drop\s+table|delete\s+from|insert\s+into)",
            r"(?i)(exec\s*\(|execute\s*\(|sp_|xp_)",
            r"(?i)(script\s*>|javascript:|vbscript:)",
            r"--\s*$",  // SQL comment patterns
        ];
        
        for pattern in &patterns {
            if let Ok(regex) = Regex::new(pattern) {
                if regex.is_match(input) {
                    return true;
                }
            }
        }
        false
    }
    
    /// Basic NoSQL injection pattern detection
    pub fn contains_nosql_injection_patterns(input: &str) -> bool {
        let patterns = [
            r"\$where|\$regex|\$gt|\$lt|\$ne|\$in|\$nin",
            r"(?i)(this\.|function\s*\()",
            r"(?i)(sleep\s*\(|benchmark\s*\()",
        ];
        
        for pattern in &patterns {
            if let Ok(regex) = Regex::new(pattern) {
                if regex.is_match(input) {
                    return true;
                }
            }
        }
        false
    }
    
    /// Validate email format
    pub fn is_valid_email(email: &str) -> bool {
        let email_regex = Regex::new(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        ).unwrap();
        email_regex.is_match(email)
    }
    
    /// Sanitize username (alphanumeric + underscore only)
    pub fn sanitize_username(input: &str) -> String {
        let username_regex = Regex::new(r"[^a-zA-Z0-9_]").unwrap();
        username_regex.replace_all(input, "").to_string()
    }
}

/// Input validation middleware for JSON payloads
pub async fn validate_json_input(
    request: Request<Body>,
    next: Next,
) -> impl IntoResponse {
    // Check content type for JSON endpoints
    if let Some(content_type) = request.headers().get(header::CONTENT_TYPE) {
        if let Ok(ct_str) = content_type.to_str() {
            if ct_str.contains("application/json") {
                // Additional validation could be added here
                // For now, we'll let the request proceed
            }
        }
    }
    
    next.run(request).await
}

/// CSRF protection middleware
pub async fn csrf_protection(
    headers: HeaderMap,
    request: Request<Body>,
    next: Next,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    let method = request.method().clone();
    
    // Only check CSRF for state-changing methods
    if matches!(method.as_str(), "POST" | "PUT" | "DELETE" | "PATCH") {
        // Allow requests with proper referer/origin for API calls
        let has_valid_origin = headers.get("origin")
            .or_else(|| headers.get("referer"))
            .map(|h| h.to_str().unwrap_or(""))
            .map(|origin| {
                // Check if origin matches allowed domains
                origin.starts_with("http://localhost:") || 
                origin.starts_with("https://yourdomain.com")
            })
            .unwrap_or(false);
        
        if !has_valid_origin {
            return Err((
                StatusCode::FORBIDDEN,
                Json(serde_json::json!({
                    "success": false,
                    "message": "CSRF protection triggered",
                    "data": null,
                    "errors": ["Invalid origin or missing CSRF token"]
                }))
            ));
        }
    }
    
    Ok(next.run(request).await)
}

#[cfg(test)]
mod tests {
    use super::sanitization::*;
    
    #[test]
    fn test_sql_injection_detection() {
        assert!(contains_sql_injection_patterns("1' OR 1=1 --"));
        assert!(contains_sql_injection_patterns("'; DROP TABLE users; --"));
        assert!(!contains_sql_injection_patterns("normal input"));
    }
    
    #[test]
    fn test_nosql_injection_detection() {
        assert!(contains_nosql_injection_patterns("$where: function() { return true; }"));
        assert!(contains_nosql_injection_patterns("{$gt: ''}"));
        assert!(!contains_nosql_injection_patterns("normal input"));
    }
    
    #[test]
    fn test_html_sanitization() {
        let malicious = r#"<script>alert('xss')</script>Hello"#;
        let clean = sanitize_html(malicious);
        assert!(!clean.contains("<script>"));
        assert!(clean.contains("Hello"));
    }
    
    #[test]
    fn test_email_validation() {
        assert!(is_valid_email("test@example.com"));
        assert!(!is_valid_email("invalid-email"));
        assert!(!is_valid_email("test@"));
    }
}