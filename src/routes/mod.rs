pub mod karyawan;
pub mod kantor;
pub mod auth;

pub use karyawan::create_karyawan_routes;
pub use kantor::create_kantor_routes;
pub use auth::{auth_routes, public_auth_routes};