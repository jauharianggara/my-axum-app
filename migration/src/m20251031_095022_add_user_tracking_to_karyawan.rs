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
                    .table(Karyawan::Table)
                    .add_column(
                        ColumnDef::new(Karyawan::CreatedBy)
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
                    .table(Karyawan::Table)
                    .add_column(
                        ColumnDef::new(Karyawan::UpdatedBy)
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
                    .name("fk_karyawan_created_by")
                    .from(Karyawan::Table, Karyawan::CreatedBy)
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
                    .name("fk_karyawan_updated_by")
                    .from(Karyawan::Table, Karyawan::UpdatedBy)
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
                    .name("fk_karyawan_updated_by")
                    .table(Karyawan::Table)
                    .to_owned(),
            )
            .await?;

        manager
            .drop_foreign_key(
                ForeignKey::drop()
                    .name("fk_karyawan_created_by")
                    .table(Karyawan::Table)
                    .to_owned(),
            )
            .await?;

        // Drop columns
        manager
            .alter_table(
                Table::alter()
                    .table(Karyawan::Table)
                    .drop_column(Karyawan::UpdatedBy)
                    .to_owned(),
            )
            .await?;

        manager
            .alter_table(
                Table::alter()
                    .table(Karyawan::Table)
                    .drop_column(Karyawan::CreatedBy)
                    .to_owned(),
            )
            .await
    }
}

#[derive(DeriveIden)]
enum Karyawan {
    Table,
    CreatedBy,
    UpdatedBy,
}

#[derive(DeriveIden)]
enum Users {
    Table,
    Id,
}
