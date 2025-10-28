use sea_orm_migration::cli::run_cli;

#[async_std::main]
async fn main() {
    run_cli(migration::Migrator).await;
}