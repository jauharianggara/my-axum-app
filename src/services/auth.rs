use anyhow::Result;
use base64::{engine::general_purpose, Engine as _};
use bcrypt::{hash, verify, DEFAULT_COST};
use chrono::{Duration, Utc};
use hmac::{Hmac, Mac};
use serde::{Deserialize, Serialize};
use sha2::Sha256;
use std::env;

type HmacSha256 = Hmac<Sha256>;

#[derive(Debug, Serialize, Deserialize)]
pub struct JwtHeader {
    pub alg: String,
    pub typ: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Claims {
    pub sub: String,  // Subject (user id)
    pub username: String,
    pub email: String,
    pub exp: i64,     // Expiry timestamp
    pub iat: i64,     // Issued at timestamp
}

pub struct JwtService {
    secret: String,
}

impl JwtService {
    pub fn new() -> Result<Self> {
        let secret = env::var("JWT_SECRET").unwrap_or_else(|_| {
            "your-256-bit-secret-key-here-make-sure-it-is-long-enough-for-security".to_string()
        });

        Ok(Self { secret })
    }

    pub fn generate_token(&self, user_id: i32, username: &str, email: &str) -> Result<String> {
        let now = Utc::now();
        let expire_hours = env::var("JWT_EXPIRE_HOURS")
            .unwrap_or_else(|_| "24".to_string())
            .parse::<i64>()
            .unwrap_or(24);

        let header = JwtHeader {
            alg: "HS256".to_string(),
            typ: "JWT".to_string(),
        };

        let claims = Claims {
            sub: user_id.to_string(),
            username: username.to_string(),
            email: email.to_string(),
            exp: (now + Duration::hours(expire_hours)).timestamp(),
            iat: now.timestamp(),
        };

        let header_json = serde_json::to_string(&header)?;
        let claims_json = serde_json::to_string(&claims)?;

        let header_encoded = general_purpose::URL_SAFE_NO_PAD.encode(header_json.as_bytes());
        let claims_encoded = general_purpose::URL_SAFE_NO_PAD.encode(claims_json.as_bytes());

        let message = format!("{}.{}", header_encoded, claims_encoded);

        let mut mac = HmacSha256::new_from_slice(self.secret.as_bytes())
            .map_err(|e| anyhow::anyhow!("Invalid secret key: {}", e))?;
        mac.update(message.as_bytes());
        let signature = mac.finalize().into_bytes();
        let signature_encoded = general_purpose::URL_SAFE_NO_PAD.encode(&signature);

        Ok(format!("{}.{}", message, signature_encoded))
    }

    pub fn verify_token(&self, token: &str) -> Result<Claims> {
        let parts: Vec<&str> = token.split('.').collect();
        if parts.len() != 3 {
            return Err(anyhow::anyhow!("Invalid token format"));
        }

        let header_data = parts[0];
        let claims_data = parts[1];
        let signature_data = parts[2];

        // Verify signature
        let message = format!("{}.{}", header_data, claims_data);
        let mut mac = HmacSha256::new_from_slice(self.secret.as_bytes())
            .map_err(|e| anyhow::anyhow!("Invalid secret key: {}", e))?;
        mac.update(message.as_bytes());

        let expected_signature = mac.finalize().into_bytes();
        let provided_signature = general_purpose::URL_SAFE_NO_PAD
            .decode(signature_data)
            .map_err(|e| anyhow::anyhow!("Invalid signature encoding: {}", e))?;

        if expected_signature[..] != provided_signature[..] {
            return Err(anyhow::anyhow!("Invalid signature"));
        }

        // Decode claims
        let claims_bytes = general_purpose::URL_SAFE_NO_PAD
            .decode(claims_data)
            .map_err(|e| anyhow::anyhow!("Invalid claims encoding: {}", e))?;
        let claims_json = String::from_utf8(claims_bytes)
            .map_err(|e| anyhow::anyhow!("Invalid claims UTF-8: {}", e))?;
        let claims: Claims = serde_json::from_str(&claims_json)
            .map_err(|e| anyhow::anyhow!("Invalid claims JSON: {}", e))?;

        // Check expiration
        let now = Utc::now().timestamp();
        if claims.exp < now {
            return Err(anyhow::anyhow!("Token has expired"));
        }

        Ok(claims)
    }

    pub fn extract_user_id(&self, token: &str) -> Result<i32> {
        let claims = self.verify_token(token)?;
        claims.sub.parse::<i32>()
            .map_err(|e| anyhow::anyhow!("Invalid user ID in token: {}", e))
    }

    pub fn get_token_expiry_hours() -> i64 {
        env::var("JWT_EXPIRE_HOURS")
            .unwrap_or_else(|_| "24".to_string())
            .parse::<i64>()
            .unwrap_or(24)
    }
}

pub struct PasswordService;

impl PasswordService {
    pub fn hash_password(password: &str) -> Result<String> {
        hash(password, DEFAULT_COST)
            .map_err(|e| anyhow::anyhow!("Failed to hash password: {}", e))
    }

    pub fn verify_password(password: &str, hash: &str) -> Result<bool> {
        verify(password, hash)
            .map_err(|e| anyhow::anyhow!("Failed to verify password: {}", e))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_password_hashing() {
        let password = "test_password_123";
        let hash = PasswordService::hash_password(password).unwrap();
        
        assert!(PasswordService::verify_password(password, &hash).unwrap());
        assert!(!PasswordService::verify_password("wrong_password", &hash).unwrap());
    }

    #[test]
    fn test_jwt_token() {
        let jwt_service = JwtService::new().unwrap();
        let token = jwt_service.generate_token(1, "testuser", "test@example.com").unwrap();
        
        let claims = jwt_service.verify_token(&token).unwrap();
        assert_eq!(claims.sub, "1");
        assert_eq!(claims.username, "testuser");
        assert_eq!(claims.email, "test@example.com");
        
        let user_id = jwt_service.extract_user_id(&token).unwrap();
        assert_eq!(user_id, 1);
    }

    #[test]
    fn test_invalid_token() {
        let jwt_service = JwtService::new().unwrap();
        
        assert!(jwt_service.verify_token("invalid.token").is_err());
        assert!(jwt_service.verify_token("invalid.token.format").is_err());
    }
}