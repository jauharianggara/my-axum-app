use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Kantor {
    pub id: Option<u32>,
    pub nama: String,
    pub alamat: String,
    pub longitude: f64,
    pub latitude: f64,
}

#[derive(Serialize, Deserialize, Debug, Validate)]
pub struct CreateKantorRequest {
    #[validate(length(
        min = 2,
        max = 100,
        message = "Nama kantor harus antara 2-100 karakter"
    ))]
    pub nama: String,

    #[validate(length(
        min = 5,
        max = 200,
        message = "Alamat kantor harus antara 5-200 karakter"
    ))]
    pub alamat: String,

    #[validate(custom(function = "crate::validators::kantor::validate_longitude"))]
    pub longitude: f64,

    #[validate(custom(function = "crate::validators::kantor::validate_latitude"))]
    pub latitude: f64,
}

#[derive(Serialize, Deserialize, Debug, Validate)]
pub struct UpdateKantorRequest {
    #[validate(length(
        min = 2,
        max = 100,
        message = "Nama kantor harus antara 2-100 karakter"
    ))]
    pub nama: String,

    #[validate(length(
        min = 5,
        max = 200,
        message = "Alamat kantor harus antara 5-200 karakter"
    ))]
    pub alamat: String,

    #[validate(custom(function = "crate::validators::kantor::validate_longitude"))]
    pub longitude: f64,
    #[validate(custom(function = "crate::validators::kantor::validate_latitude"))]
    pub latitude: f64,
}
