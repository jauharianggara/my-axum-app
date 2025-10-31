use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Step 1: Add jabatan_id column as nullable first
        manager
            .alter_table(
                Table::alter()
                    .table(Karyawan::Table)
                    .add_column(
                        ColumnDef::new(Karyawan::JabatanId)
                            .integer()
                            .null()
                    )
                    .to_owned(),
            )
            .await?;

        // Step 2: Insert default jabatan if not exists
        let insert_default_jabatan = Query::insert()
            .into_table(Jabatan::Table)
            .columns([Jabatan::NamaJabatan, Jabatan::Deskripsi])
            .values_panic(["Staff".into(), "Jabatan Default".into()])
            .to_owned();
        
        manager.exec_stmt(insert_default_jabatan).await?;

        // Step 3: Update existing karyawan to reference the default jabatan (id = 1)
        let update_karyawan = Query::update()
            .table(Karyawan::Table)
            .value(Karyawan::JabatanId, 1)
            .and_where(Expr::col(Karyawan::JabatanId).is_null())
            .to_owned();
        
        manager.exec_stmt(update_karyawan).await?;

        // Step 4: Make jabatan_id NOT NULL
        manager
            .alter_table(
                Table::alter()
                    .table(Karyawan::Table)
                    .modify_column(
                        ColumnDef::new(Karyawan::JabatanId)
                            .integer()
                            .not_null()
                    )
                    .to_owned(),
            )
            .await?;

        // Step 5: Add foreign key constraint
        manager
            .create_foreign_key(
                ForeignKey::create()
                    .name("fk_karyawan_jabatan_id")
                    .from(Karyawan::Table, Karyawan::JabatanId)
                    .to(Jabatan::Table, Jabatan::Id)
                    .on_delete(ForeignKeyAction::Restrict)
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
                    .name("fk_karyawan_jabatan_id")
                    .table(Karyawan::Table)
                    .to_owned(),
            )
            .await?;

        // Drop jabatan_id column
        manager
            .alter_table(
                Table::alter()
                    .table(Karyawan::Table)
                    .drop_column(Karyawan::JabatanId)
                    .to_owned(),
            )
            .await
    }
}

#[derive(DeriveIden)]
enum Karyawan {
    Table,
    JabatanId,
}

#[derive(DeriveIden)]
enum Jabatan {
    Table,
    Id,
    NamaJabatan,
    Deskripsi,
}
