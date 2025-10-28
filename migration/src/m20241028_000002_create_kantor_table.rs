use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .create_table(
                Table::create()
                    .table(Kantor::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(Kantor::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(Kantor::Nama)
                            .string_len(100)
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(Kantor::Alamat)
                            .string_len(200)
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(Kantor::Longitude)
                            .decimal_len(10, 7)
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(Kantor::Latitude)
                            .decimal_len(10, 7)
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(Kantor::CreatedAt)
                            .timestamp()
                            .default(Expr::current_timestamp())
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(Kantor::UpdatedAt)
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
            .drop_table(Table::drop().table(Kantor::Table).to_owned())
            .await
    }
}

#[derive(DeriveIden)]
enum Kantor {
    Table,
    Id,
    Nama,
    Alamat,
    Longitude,
    Latitude,
    CreatedAt,
    UpdatedAt,
}