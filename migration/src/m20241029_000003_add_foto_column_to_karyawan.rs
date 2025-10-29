use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Karyawan::Table)
                    .add_column(
                        ColumnDef::new(Karyawan::FotoPath)
                            .string()
                            .null()
                    )
                    .add_column(
                        ColumnDef::new(Karyawan::FotoOriginalName)
                            .string()
                            .null()
                    )
                    .add_column(
                        ColumnDef::new(Karyawan::FotoSize)
                            .big_integer()
                            .null()
                    )
                    .add_column(
                        ColumnDef::new(Karyawan::FotoMimeType)
                            .string()
                            .null()
                    )
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Karyawan::Table)
                    .drop_column(Karyawan::FotoPath)
                    .drop_column(Karyawan::FotoOriginalName)
                    .drop_column(Karyawan::FotoSize)
                    .drop_column(Karyawan::FotoMimeType)
                    .to_owned(),
            )
            .await
    }
}

#[derive(DeriveIden)]
enum Karyawan {
    Table,
    FotoPath,
    FotoOriginalName,
    FotoSize,
    FotoMimeType,
}