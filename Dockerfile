# ===== Build stage =====
FROM rust:1.82 as builder
WORKDIR /app

# Pre-cache deps
COPY Cargo.toml Cargo.lock ./
# tambahkan stub agar cache deps efektif
RUN mkdir -p src && echo "fn main(){}" > src/main.rs && cargo build --release && rm -rf src

# Copy sumber asli & build release
COPY . .
# build app (ganti nama paket kalau berbeda)
RUN cargo build --release && \
    strip target/release/my-axum-app || true

# (opsional) jika ada crate "migration", ikut build
# RUN cargo build --release -p migration && strip target/release/migration || true

# ===== Runtime stage =====
FROM debian:bookworm-slim
WORKDIR /app
RUN useradd -m -u 10001 appuser && \
    apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

# copy binary
COPY --from=builder /app/target/release/my-axum-app /usr/local/bin/app
# COPY --from=builder /app/target/release/migration /usr/local/bin/migration

ENV RUST_LOG=info \
    APP_PORT=8080
USER appuser
EXPOSE 8080

# (opsional) jalankan migrasi sebelum start
# ENTRYPOINT ["sh","-lc","migration -- migrate up && exec /usr/local/bin/app"]
ENTRYPOINT ["/usr/local/bin/app"]
