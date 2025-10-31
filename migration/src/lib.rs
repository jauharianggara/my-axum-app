pub use sea_orm_migration::prelude::*;

mod m20241028_000001_create_karyawan_table;
mod m20241028_000002_create_kantor_table;
mod m20251028_090641_add_kantor_id_to_karyawan;
mod m20241029_000003_add_foto_column_to_karyawan;
mod m20251029_101303_make_kantor_id_required;
mod m20251029_120000_create_users_table;
mod m20251029_140819_change_timestamp_to_datetime;
mod m20251031_095022_add_user_tracking_to_karyawan;
mod m20251031_100041_add_user_tracking_to_kantor;
mod m20251031_102506_add_user_id_to_karyawan;
mod m20251031_110440_remove_user_id_unique_constraint;

pub struct Migrator;

#[async_trait::async_trait]
impl MigratorTrait for Migrator {
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![
            Box::new(m20241028_000001_create_karyawan_table::Migration),
            Box::new(m20241028_000002_create_kantor_table::Migration),
            Box::new(m20251028_090641_add_kantor_id_to_karyawan::Migration),
            Box::new(m20241029_000003_add_foto_column_to_karyawan::Migration),
            Box::new(m20251029_101303_make_kantor_id_required::Migration),
            Box::new(m20251029_120000_create_users_table::Migration),
            Box::new(m20251029_140819_change_timestamp_to_datetime::Migration),
            Box::new(m20251031_095022_add_user_tracking_to_karyawan::Migration),
            Box::new(m20251031_100041_add_user_tracking_to_kantor::Migration),
            Box::new(m20251031_102506_add_user_id_to_karyawan::Migration),
            Box::new(m20251031_110440_remove_user_id_unique_constraint::Migration),
        ]
    }
}