pub mod karyawan;
pub mod kantor;
pub mod common;


pub use common::ApiResponse; 
pub use karyawan::{Karyawan, CreateKaryawanRequest, UpdateKaryawanRequest};
pub use kantor::{Kantor, CreateKantorRequest, UpdateKantorRequest};