use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .create_table(
                Table::create()
                    .table(Jabatan::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(Jabatan::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(Jabatan::NamaJabatan)
                            .string()
                            .string_len(100)
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(Jabatan::Deskripsi)
                            .text()
                            .null(),
                    )
                    .col(
                        ColumnDef::new(Jabatan::CreatedAt)
                            .timestamp_with_time_zone()
                            .not_null()
                            .default(Expr::current_timestamp()),
                    )
                    .col(
                        ColumnDef::new(Jabatan::UpdatedAt)
                            .timestamp_with_time_zone()
                            .not_null()
                            .default(Expr::current_timestamp()),
                    )
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .drop_table(Table::drop().table(Jabatan::Table).to_owned())
            .await
    }
}

#[derive(DeriveIden)]
enum Jabatan {
    Table,
    Id,
    NamaJabatan,
    Deskripsi,
    CreatedAt,
    UpdatedAt,
}
