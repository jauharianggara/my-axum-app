use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Add user_id column
        manager
            .alter_table(
                Table::alter()
                    .table(Karyawan::Table)
                    .add_column(
                        ColumnDef::new(Karyawan::UserId)
                            .integer()
                            .null()
                            .unique_key()
                    )
                    .to_owned(),
            )
            .await?;

        // Add foreign key constraint for user_id
        manager
            .create_foreign_key(
                ForeignKey::create()
                    .name("fk_karyawan_user_id")
                    .from(Karyawan::Table, Karyawan::UserId)
                    .to(Users::Table, Users::Id)
                    .on_delete(ForeignKeyAction::SetNull)
                    .on_update(ForeignKeyAction::Cascade)
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Drop foreign key constraint
        manager
            .drop_foreign_key(
                ForeignKey::drop()
                    .name("fk_karyawan_user_id")
                    .table(Karyawan::Table)
                    .to_owned(),
            )
            .await?;

        // Drop user_id column
        manager
            .alter_table(
                Table::alter()
                    .table(Karyawan::Table)
                    .drop_column(Karyawan::UserId)
                    .to_owned(),
            )
            .await
    }
}

#[derive(DeriveIden)]
enum Karyawan {
    Table,
    UserId,
}

#[derive(DeriveIden)]
enum Users {
    Table,
    Id,
}
