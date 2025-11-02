use axum::{
    extract::{ConnectInfo, Request},
    middleware::Next,
    response::Response,
};
use std::net::SocketAddr;
use std::time::Instant;

/// Request logging middleware
/// Logs all incoming requests with IP, timestamp, path, method, and response time
pub async fn request_logger(
    ConnectInfo(addr): ConnectInfo<SocketAddr>,
    request: Request,
    next: Next,
) -> Response {
    let start = Instant::now();
    
    // Extract request information
    let method = request.method().clone();
    let uri = request.uri().clone();
    let path = uri.path();
    let query = uri.query().unwrap_or("");
    let version = format!("{:?}", request.version());
    
    // Get headers
    let user_agent = request
        .headers()
        .get("user-agent")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("-");
    
    let referer = request
        .headers()
        .get("referer")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("-");
    
    let content_type = request
        .headers()
        .get("content-type")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("-");
    
    let origin = request
        .headers()
        .get("origin")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("-");
    
    // Get X-Forwarded-For or real IP
    let forwarded_for = request
        .headers()
        .get("x-forwarded-for")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("-");
    
    let client_ip = if forwarded_for != "-" {
        forwarded_for
    } else {
        &addr.ip().to_string()
    };
    
    // Current timestamp
    let timestamp = chrono::Local::now().format("%Y-%m-%d %H:%M:%S%.3f");
    
    // Log incoming request
    println!("╔═══════════════════════════════════════════════════════════════");
    println!("║ 📥 INCOMING REQUEST");
    println!("╠═══════════════════════════════════════════════════════════════");
    println!("║ ⏰ Time       : {}", timestamp);
    println!("║ 🌐 IP         : {} (Socket: {})", client_ip, addr);
    println!("║ 📍 Method     : {}", method);
    println!("║ 🔗 Path       : {}", path);
    if !query.is_empty() {
        println!("║ ❓ Query      : {}", query);
    }
    println!("║ 📡 Protocol   : {}", version);
    println!("║ 🔖 Origin     : {}", origin);
    println!("║ 📄 Content    : {}", content_type);
    println!("║ 🔍 User-Agent : {}", user_agent);
    if referer != "-" {
        println!("║ 🔗 Referer    : {}", referer);
    }
    
    // Execute the request
    let response = next.run(request).await;
    
    // Calculate response time
    let duration = start.elapsed();
    let duration_ms = duration.as_millis();
    
    // Get response status
    let status = response.status();
    let status_code = status.as_u16();
    
    // Determine color/emoji based on status
    let (status_emoji, status_color) = match status_code {
        200..=299 => ("✅", "SUCCESS"),
        300..=399 => ("🔄", "REDIRECT"),
        400..=499 => ("⚠️ ", "CLIENT ERROR"),
        500..=599 => ("❌", "SERVER ERROR"),
        _ => ("ℹ️ ", "INFO"),
    };
    
    // Log response
    println!("╠═══════════════════════════════════════════════════════════════");
    println!("║ 📤 RESPONSE");
    println!("╠═══════════════════════════════════════════════════════════════");
    println!("║ {} Status     : {} {} ({})", status_emoji, status_code, status.canonical_reason().unwrap_or("Unknown"), status_color);
    println!("║ ⏱️  Duration   : {} ms", duration_ms);
    println!("╚═══════════════════════════════════════════════════════════════");
    println!();
    
    response
}

/// Simplified request logger (single line format)
pub async fn simple_request_logger(
    ConnectInfo(addr): ConnectInfo<SocketAddr>,
    request: Request,
    next: Next,
) -> Response {
    let start = Instant::now();
    
    let method = request.method().clone();
    let uri = request.uri().clone();
    let path = uri.path();
    
    let forwarded_for = request
        .headers()
        .get("x-forwarded-for")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("-");
    
    let client_ip = if forwarded_for != "-" {
        forwarded_for.to_string()
    } else {
        addr.ip().to_string()
    };
    
    let timestamp = chrono::Local::now().format("%Y-%m-%d %H:%M:%S");
    
    // Execute request
    let response = next.run(request).await;
    
    let duration = start.elapsed();
    let status = response.status();
    
    // Single line log format (similar to Apache access log)
    let status_emoji = match status.as_u16() {
        200..=299 => "✅",
        300..=399 => "🔄",
        400..=499 => "⚠️",
        500..=599 => "❌",
        _ => "ℹ️",
    };
    
    println!(
        "{} [{}] {} {} {} - {} ({} ms)",
        status_emoji,
        timestamp,
        client_ip,
        method,
        path,
        status.as_u16(),
        duration.as_millis()
    );
    
    response
}

/// Error request logger (only logs errors)
pub async fn error_request_logger(
    ConnectInfo(addr): ConnectInfo<SocketAddr>,
    request: Request,
    next: Next,
) -> Response {
    let method = request.method().clone();
    let uri = request.uri().clone();
    let path = uri.path().to_string();
    
    let forwarded_for = request
        .headers()
        .get("x-forwarded-for")
        .and_then(|v| v.to_str().ok())
        .map(|s| s.to_string());
    
    let client_ip = forwarded_for.unwrap_or_else(|| addr.ip().to_string());
    
    let timestamp = chrono::Local::now().format("%Y-%m-%d %H:%M:%S");
    
    let response = next.run(request).await;
    let status = response.status();
    
    // Only log errors (4xx and 5xx)
    if status.is_client_error() || status.is_server_error() {
        eprintln!(
            "❌ ERROR [{}] {} {} {} - {}",
            timestamp,
            client_ip,
            method,
            path,
            status.as_u16()
        );
    }
    
    response
}
