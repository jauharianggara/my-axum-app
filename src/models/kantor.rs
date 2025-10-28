use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Serialize, Deserialize)]
#[sea_orm(table_name = "kantor")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i32,
    pub nama: String,
    pub alamat: String,
    pub longitude: Decimal,
    pub latitude: Decimal,
    pub created_at: DateTimeWithTimeZone,
    pub updated_at: DateTimeWithTimeZone,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {
    #[sea_orm(has_many = "super::karyawan::Entity")]
    Karyawan,
}

impl ActiveModelBehavior for ActiveModel {}

impl Related<super::karyawan::Entity> for Entity {
    fn to() -> RelationDef {
        Relation::Karyawan.def()
    }
}

// Type alias for backward compatibility
//pub type Kantor = Model;

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
