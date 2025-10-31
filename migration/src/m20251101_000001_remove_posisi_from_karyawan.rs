use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Drop posisi column from karyawan table
        manager
            .alter_table(
                Table::alter()
                    .table(Karyawan::Table)
                    .drop_column(Karyawan::Posisi)
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Re-add posisi column if rollback needed
        manager
            .alter_table(
                Table::alter()
                    .table(Karyawan::Table)
                    .add_column(
                        ColumnDef::new(Karyawan::Posisi)
                            .string()
                            .string_len(30)
                            .not_null()
                            .default("")
                    )
                    .to_owned(),
            )
            .await
    }
}

#[derive(DeriveIden)]
enum Karyawan {
    Table,
    Posisi,
}
