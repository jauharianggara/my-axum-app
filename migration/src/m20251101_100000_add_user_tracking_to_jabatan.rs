use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Add created_by column
        manager
            .alter_table(
                Table::alter()
                    .table(Jabatan::Table)
                    .add_column(
                        ColumnDef::new(Jabatan::CreatedBy)
                            .integer()
                            .null()
                    )
                    .to_owned(),
            )
            .await?;

        // Add updated_by column
        manager
            .alter_table(
                Table::alter()
                    .table(Jabatan::Table)
                    .add_column(
                        ColumnDef::new(Jabatan::UpdatedBy)
                            .integer()
                            .null()
                    )
                    .to_owned(),
            )
            .await?;

        // Add foreign key constraint for created_by
        manager
            .create_foreign_key(
                ForeignKey::create()
                    .name("fk_jabatan_created_by")
                    .from(Jabatan::Table, Jabatan::CreatedBy)
                    .to(Users::Table, Users::Id)
                    .on_delete(ForeignKeyAction::SetNull)
                    .on_update(ForeignKeyAction::Cascade)
                    .to_owned(),
            )
            .await?;

        // Add foreign key constraint for updated_by
        manager
            .create_foreign_key(
                ForeignKey::create()
                    .name("fk_jabatan_updated_by")
                    .from(Jabatan::Table, Jabatan::UpdatedBy)
                    .to(Users::Table, Users::Id)
                    .on_delete(ForeignKeyAction::SetNull)
                    .on_update(ForeignKeyAction::Cascade)
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Drop foreign key constraints
        manager
            .drop_foreign_key(
                ForeignKey::drop()
                    .name("fk_jabatan_updated_by")
                    .table(Jabatan::Table)
                    .to_owned(),
            )
            .await?;

        manager
            .drop_foreign_key(
                ForeignKey::drop()
                    .name("fk_jabatan_created_by")
                    .table(Jabatan::Table)
                    .to_owned(),
            )
            .await?;

        // Drop columns
        manager
            .alter_table(
                Table::alter()
                    .table(Jabatan::Table)
                    .drop_column(Jabatan::UpdatedBy)
                    .to_owned(),
            )
            .await?;

        manager
            .alter_table(
                Table::alter()
                    .table(Jabatan::Table)
                    .drop_column(Jabatan::CreatedBy)
                    .to_owned(),
            )
            .await
    }
}

#[derive(DeriveIden)]
enum Jabatan {
    Table,
    CreatedBy,
    UpdatedBy,
}

#[derive(DeriveIden)]
enum Users {
    Table,
    Id,
}