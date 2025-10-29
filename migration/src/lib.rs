pub use sea_orm_migration::prelude::*;

mod m20241028_000001_create_karyawan_table;
mod m20241028_000002_create_kantor_table;
mod m20251028_090641_add_kantor_id_to_karyawan;
mod m20241029_000003_add_foto_column_to_karyawan;
mod m20251029_101303_make_kantor_id_required;


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
        ]
    }
}