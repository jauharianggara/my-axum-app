use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Eq, Serialize, Deserialize)]
#[sea_orm(table_name = "jabatan")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i32,
    pub nama_jabatan: String,
    pub deskripsi: Option<String>,
    pub created_by: Option<i32>,
    pub updated_by: Option<i32>,
    pub created_at: DateTimeWithTimeZone,
    pub updated_at: DateTimeWithTimeZone,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {
    #[sea_orm(has_many = "super::karyawan::Entity")]
    Karyawan,
    #[sea_orm(
        belongs_to = "super::user::Entity",
        from = "Column::CreatedBy",
        to = "super::user::Column::Id"
    )]
    CreatedByUser,
    #[sea_orm(
        belongs_to = "super::user::Entity",
        from = "Column::UpdatedBy",
        to = "super::user::Column::Id"
    )]
    UpdatedByUser,
}

impl Related<super::karyawan::Entity> for Entity {
    fn to() -> RelationDef {
        Relation::Karyawan.def()
    }
}



impl ActiveModelBehavior for ActiveModel {}

#[derive(Serialize, Deserialize, Debug, Validate)]
pub struct CreateJabatanRequest {
    #[validate(length(
        min = 2,
        max = 100,
        message = "Nama jabatan harus antara 2-100 karakter"
    ))]
    pub nama_jabatan: String,

    #[validate(length(max = 500, message = "Deskripsi maksimal 500 karakter"))]
    pub deskripsi: Option<String>,
}

#[derive(Serialize, Deserialize, Debug, Validate)]
pub struct UpdateJabatanRequest {
    #[validate(length(
        min = 2,
        max = 100,
        message = "Nama jabatan harus antara 2-100 karakter"
    ))]
    pub nama_jabatan: String,

    #[validate(length(max = 500, message = "Deskripsi maksimal 500 karakter"))]
    pub deskripsi: Option<String>,
}
