use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Eq, Serialize, Deserialize)]
#[sea_orm(table_name = "karyawan")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i32,
    pub nama: String,
    pub posisi: String,
    pub gaji: i32,
    pub kantor_id:  i32,
    pub created_at: DateTimeWithTimeZone,
    pub updated_at: DateTimeWithTimeZone,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {
    #[sea_orm(
        belongs_to = "super::kantor::Entity",
        from = "Column::KantorId",
        to = "super::kantor::Column::Id"
    )]
    Kantor,
}

impl ActiveModelBehavior for ActiveModel {}

impl Related<super::kantor::Entity> for Entity {
    fn to() -> RelationDef {
        Relation::Kantor.def()
    }
}

// Type alias for backward compatibility
//pub type Karyawan = Model;

#[derive(Serialize, Deserialize, Debug, Validate)]
pub struct CreateKaryawanRequest {
    #[validate(length(min = 2, max = 50, message = "Nama harus antara 2-50 karakter"))]
    pub nama: String,

    #[validate(length(min = 2, max = 30, message = "Posisi harus antara 2-30 karakter"))]
    pub posisi: String,

    #[validate(custom(function = "crate::validators::karyawan::validate_gaji"))]
    pub gaji: String,

    #[validate(custom(function = "crate::validators::karyawan::validate_kantor_id"))]
    pub kantor_id: String,
}

#[derive(Serialize, Deserialize, Debug, Validate)]
pub struct UpdateKaryawanRequest {
    #[validate(length(min = 2, max = 50, message = "Nama harus antara 2-50 karakter"))]
    pub nama: String,

    #[validate(length(min = 2, max = 30, message = "Posisi harus antara 2-30 karakter"))]
    pub posisi: String,

    #[validate(custom(function = "crate::validators::karyawan::validate_gaji"))]
    pub gaji: String,

    #[validate(custom(function = "crate::validators::karyawan::validate_kantor_id"))]
    pub kantor_id: String,
}
