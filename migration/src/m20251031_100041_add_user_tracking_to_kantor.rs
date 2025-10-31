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
                    .table(Kantor::Table)
                    .add_column(
                        ColumnDef::new(Kantor::CreatedBy)
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
                    .table(Kantor::Table)
                    .add_column(
                        ColumnDef::new(Kantor::UpdatedBy)
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
                    .name("fk_kantor_created_by")
                    .from(Kantor::Table, Kantor::CreatedBy)
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
                    .name("fk_kantor_updated_by")
                    .from(Kantor::Table, Kantor::UpdatedBy)
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
                    .name("fk_kantor_updated_by")
                    .table(Kantor::Table)
                    .to_owned(),
            )
            .await?;

        manager
            .drop_foreign_key(
                ForeignKey::drop()
                    .name("fk_kantor_created_by")
                    .table(Kantor::Table)
                    .to_owned(),
            )
            .await?;

        // Drop columns
        manager
            .alter_table(
                Table::alter()
                    .table(Kantor::Table)
                    .drop_column(Kantor::UpdatedBy)
                    .to_owned(),
            )
            .await?;

        manager
            .alter_table(
                Table::alter()
                    .table(Kantor::Table)
                    .drop_column(Kantor::CreatedBy)
                    .to_owned(),
            )
            .await
    }
}

#[derive(DeriveIden)]
enum Kantor {
    Table,
    CreatedBy,
    UpdatedBy,
}

#[derive(DeriveIden)]
enum Users {
    Table,
    Id,
}
