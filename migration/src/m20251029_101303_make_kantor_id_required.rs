use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Update existing NULL kantor_id records to point to a default kantor
        // First, let's find the first available kantor ID
        manager
            .get_connection()
            .execute_unprepared(
                "UPDATE karyawan SET kantor_id = (SELECT MIN(id) FROM kantor) WHERE kantor_id IS NULL"
            )
            .await?;

        // Drop the existing foreign key constraint
        manager
            .drop_foreign_key(
                ForeignKey::drop()
                    .name("fk_karyawan_kantor_id")
                    .table(Karyawan::Table)
                    .to_owned(),
            )
            .await?;

        // Make the column NOT NULL
        manager
            .alter_table(
                Table::alter()
                    .table(Karyawan::Table)
                    .modify_column(
                        ColumnDef::new(Karyawan::KantorId)
                            .integer()
                            .not_null()
                    )
                    .to_owned(),
            )
            .await?;

        // Recreate foreign key constraint with CASCADE instead of SET NULL
        manager
            .create_foreign_key(
                ForeignKey::create()
                    .name("fk_karyawan_kantor_id")
                    .from(Karyawan::Table, Karyawan::KantorId)
                    .to(Kantor::Table, Kantor::Id)
                    .on_delete(ForeignKeyAction::Restrict) // Prevent deletion of kantor if karyawan exists
                    .on_update(ForeignKeyAction::Cascade)
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Drop the foreign key constraint
        manager
            .drop_foreign_key(
                ForeignKey::drop()
                    .name("fk_karyawan_kantor_id")
                    .table(Karyawan::Table)
                    .to_owned(),
            )
            .await?;

        // Make the column nullable again
        manager
            .alter_table(
                Table::alter()
                    .table(Karyawan::Table)
                    .modify_column(
                        ColumnDef::new(Karyawan::KantorId)
                            .integer()
                            .null()
                    )
                    .to_owned(),
            )
            .await?;

        // Recreate original foreign key constraint with SET NULL
        manager
            .create_foreign_key(
                ForeignKey::create()
                    .name("fk_karyawan_kantor_id")
                    .from(Karyawan::Table, Karyawan::KantorId)
                    .to(Kantor::Table, Kantor::Id)
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
    KantorId,
}

#[derive(DeriveIden)]
enum Kantor {
    Table,
    Id,
}
