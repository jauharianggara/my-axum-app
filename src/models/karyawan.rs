use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Karyawan {
    pub id: Option<u32>,
    pub nama: String,
    pub posisi: String,
    pub gaji: u32,
}

#[derive(Serialize, Deserialize, Debug, Validate)]
pub struct CreateKaryawanRequest {
    #[validate(length(min = 2, max = 50, message = "Nama harus antara 2-50 karakter"))]
    pub nama: String,
    
    #[validate(length(min = 2, max = 30, message = "Posisi harus antara 2-30 karakter"))]
    pub posisi: String,
    
    #[validate(custom(function = "crate::validators::karyawan::validate_gaji"))]
    pub gaji: String,
}

#[derive(Serialize, Deserialize, Debug, Validate)]
pub struct UpdateKaryawanRequest {
    #[validate(length(min = 2, max = 50, message = "Nama harus antara 2-50 karakter"))]
    pub nama: String,
    
    #[validate(length(min = 2, max = 30, message = "Posisi harus antara 2-30 karakter"))]
    pub posisi: String,
    
    #[validate(custom(function = "crate::validators::karyawan::validate_gaji"))]
    pub gaji: String,
}