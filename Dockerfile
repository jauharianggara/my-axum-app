# ===== Build stage =====
FROM rustlang/rust:nightly-slim AS builder
WORKDIR /app

# Install required build dependencies
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    libssl-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy all source files and build
COPY . .

# Build the application
RUN cargo build --release && \
    ls -la target/release/ && \
    strip target/release/my-axum-app || true

# ===== Runtime stage =====
FROM debian:bookworm-slim
WORKDIR /app

# Create non-root user and install runtime dependencies
RUN useradd -m -u 10001 appuser && \
    apt-get update && \
    apt-get install -y \
    ca-certificates \
    libssl3 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy binaries from builder stage
COPY --from=builder /app/target/release/my-axum-app /usr/local/bin/app

# Create simple startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting application..."\n\
exec /usr/local/bin/app' > /usr/local/bin/start.sh && \
    chmod +x /usr/local/bin/start.sh

# Set ownership
RUN chown appuser:appuser /usr/local/bin/app /usr/local/bin/start.sh

# Environment variables
ENV RUST_LOG=info \
    PORT=8080 \
    HOST=0.0.0.0 \
    DATABASE_URL=""

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["/usr/local/bin/start.sh"]
