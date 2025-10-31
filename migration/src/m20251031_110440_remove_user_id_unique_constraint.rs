use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Step 1: Drop the foreign key constraint
        manager
            .drop_foreign_key(
                ForeignKey::drop()
                    .name("fk_karyawan_user_id")
                    .table(Karyawan::Table)
                    .to_owned(),
            )
            .await?;

        // Step 2: Drop the unique constraint on user_id
        manager
            .drop_index(
                Index::drop()
                    .name("user_id")
                    .table(Karyawan::Table)
                    .to_owned(),
            )
            .await?;

        // Step 3: Recreate the foreign key WITHOUT unique constraint
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
        // Step 1: Drop the foreign key
        manager
            .drop_foreign_key(
                ForeignKey::drop()
                    .name("fk_karyawan_user_id")
                    .table(Karyawan::Table)
                    .to_owned(),
            )
            .await?;

        // Step 2: Recreate the unique constraint
        manager
            .create_index(
                Index::create()
                    .name("user_id")
                    .table(Karyawan::Table)
                    .col(Karyawan::UserId)
                    .unique()
                    .to_owned(),
            )
            .await?;

        // Step 3: Recreate the foreign key
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
