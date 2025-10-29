use anyhow::{Context, Result};
use axum::extract::multipart::Field;
use std::path::Path;
use tokio::fs;
use tokio::io::AsyncWriteExt;
use uuid::Uuid;

pub struct FileUploadService;

#[derive(Debug, Clone)]
pub struct UploadedFile {
    pub file_path: String,
    pub original_name: String,
    pub size: i64,
    pub mime_type: String,
}

impl FileUploadService {
    pub async fn save_karyawan_photo(
        field: Field<'_>,
        karyawan_id: Option<i32>,
    ) -> Result<UploadedFile> {
        let content_type = field.content_type().unwrap_or("").to_string();
        let original_name = field.file_name().unwrap_or("unknown").to_string();

        // Validate file type
        Self::validate_image_type(&content_type)?;

        // Create uploads directory if it doesn't exist
        let upload_dir = "uploads/karyawan/photos";
        fs::create_dir_all(upload_dir).await
            .context("Failed to create upload directory")?;

        // Generate unique filename
        let file_extension = Self::get_file_extension(&original_name);
        let unique_filename = match karyawan_id {
            Some(id) => format!("karyawan_{}_{}.{}", id, Uuid::new_v4(), file_extension),
            None => format!("temp_karyawan_{}.{}", Uuid::new_v4(), file_extension),
        };

        let file_path = format!("{}/{}", upload_dir, unique_filename);

        // Save file
        let data = field.bytes().await
            .context("Failed to read file data")?;

        let file_size = data.len() as i64;

        // Validate file size (max 5MB)
        Self::validate_file_size(file_size)?;

        let mut file = fs::File::create(&file_path).await
            .context("Failed to create file")?;

        file.write_all(&data).await
            .context("Failed to write file data")?;

        Ok(UploadedFile {
            file_path,
            original_name,
            size: file_size,
            mime_type: content_type,
        })
    }

    pub async fn delete_karyawan_photo(file_path: &str) -> Result<()> {
        if Path::new(file_path).exists() {
            fs::remove_file(file_path).await
                .context("Failed to delete file")?;
        }
        Ok(())
    }

    fn validate_image_type(content_type: &str) -> Result<()> {
        let allowed_types = [
            "image/jpeg",
            "image/jpg", 
            "image/png",
            "image/webp"
        ];

        if !allowed_types.contains(&content_type) {
            return Err(anyhow::anyhow!(
                "Invalid file type. Only JPEG, PNG, and WebP images are allowed. Got: {}",
                content_type
            ));
        }

        Ok(())
    }

    fn validate_file_size(size: i64) -> Result<()> {
        const MAX_SIZE: i64 = 5 * 1024 * 1024; // 5MB

        if size > MAX_SIZE {
            return Err(anyhow::anyhow!(
                "File too large. Maximum size is 5MB, got: {} bytes",
                size
            ));
        }

        if size == 0 {
            return Err(anyhow::anyhow!("File is empty"));
        }

        Ok(())
    }

    fn get_file_extension(filename: &str) -> String {
        Path::new(filename)
            .extension()
            .and_then(|ext| ext.to_str())
            .unwrap_or("jpg")
            .to_string()
    }

    pub async fn update_karyawan_photo(
        field: Field<'_>,
        karyawan_id: i32,
        old_photo_path: Option<&str>,
    ) -> Result<UploadedFile> {
        // Delete old photo if exists
        if let Some(old_path) = old_photo_path {
            let _ = Self::delete_karyawan_photo(old_path).await;
        }

        // Save new photo
        Self::save_karyawan_photo(field, Some(karyawan_id)).await
    }
}