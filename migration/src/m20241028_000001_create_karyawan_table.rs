use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .create_table(
                Table::create()
                    .table(Karyawan::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(Karyawan::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(Karyawan::Nama)
                            .string_len(50)
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(Karyawan::Posisi)
                            .string_len(30)
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(Karyawan::Gaji)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(Karyawan::CreatedAt)
                            .timestamp()
                            .default(Expr::current_timestamp())
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(Karyawan::UpdatedAt)
                            .timestamp()
                            .default(Expr::current_timestamp())
                            .extra("ON UPDATE CURRENT_TIMESTAMP".to_string())
                            .not_null(),
                    )
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .drop_table(Table::drop().table(Karyawan::Table).to_owned())
            .await
    }
}

#[derive(DeriveIden)]
enum Karyawan {
    Table,
    Id,
    Nama,
    Posisi,
    Gaji,
    CreatedAt,
    UpdatedAt,
}