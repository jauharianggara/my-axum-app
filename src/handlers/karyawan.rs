use axum::{
    extract::{Path, Json as ExtractJson},
    response::Json,
};
use crate::models::{ApiResponse, Karyawan, CreateKaryawanRequest, UpdateKaryawanRequest};
use crate::validators::karyawan::{validate_id, handle_validation_errors};
use validator::Validate;

pub async fn get_all_karyawan() -> Json<ApiResponse<Vec<Karyawan>>> {
    let karyawans = vec![
        Karyawan {
            id: Some(1),
            nama: "Budi Santoso".to_string(),
            posisi: "Software Engineer".to_string(),
            gaji: 8000000,
        },
        Karyawan {
            id: Some(2),
            nama: "Siti Nurhaliza".to_string(),
            posisi: "Product Manager".to_string(),
            gaji: 12000000,
        },
    ];
    
    Json(ApiResponse::success(
        "List of karyawans retrieved successfully".to_string(),
        karyawans
    ))
}

pub async fn get_karyawan_by_id(Path(id_str): Path<String>) -> Json<ApiResponse<Karyawan>> {
    // Validasi ID menggunakan function
    let id = match validate_id(&id_str) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg]
            ));
        }
    };
    
    // Simulasi pengecekan apakah karyawan dengan ID tersebut ada
    if id == 0 {
        return Json(ApiResponse::error(
            "Karyawan not found".to_string(),
            vec!["Karyawan dengan ID tersebut tidak ditemukan".to_string()]
        ));
    }
    
    let karyawan = Karyawan {
        id: Some(id),
        nama: "Budi Santoso".to_string(),
        posisi: "Software Engineer".to_string(),
        gaji: 8000000,
    };
    
    Json(ApiResponse::success(
        format!("Karyawan with ID {} retrieved successfully", id),
        karyawan
    ))
}

pub async fn create_karyawan(ExtractJson(payload): ExtractJson<CreateKaryawanRequest>) -> Json<ApiResponse<Karyawan>> {
    // Validate the payload
    if let Err(validation_errors) = payload.validate() {
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            handle_validation_errors(validation_errors)
        ));
    }
    
    let new_karyawan = Karyawan {
        id: Some(3), // In real app, this would be auto-generated
        nama: payload.nama,
        posisi: payload.posisi,
        gaji: payload.gaji.parse::<u32>().unwrap(), // Safe to unwrap because validation passed
    };
    
    Json(ApiResponse::success(
        "Karyawan created successfully".to_string(),
        new_karyawan
    ))
}

pub async fn update_karyawan(Path(id_str): Path<String>, ExtractJson(payload): ExtractJson<UpdateKaryawanRequest>) -> Json<ApiResponse<Karyawan>> {
    // Validasi ID menggunakan function
    let id = match validate_id(&id_str) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg]
            ));
        }
    };
    
    // Validate the payload
    if let Err(validation_errors) = payload.validate() {
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            handle_validation_errors(validation_errors)
        ));
    }
    
    let updated_karyawan = Karyawan {
        id: Some(id),
        nama: payload.nama,
        posisi: payload.posisi,
        gaji: payload.gaji.parse::<u32>().unwrap(), // Safe to unwrap because validation passed
    };
    
    Json(ApiResponse::success(
        format!("Karyawan with ID {} updated successfully", id),
        updated_karyawan
    ))
}

pub async fn delete_karyawan(Path(id_str): Path<String>) -> Json<ApiResponse<()>> {
    // Validasi ID menggunakan function
    let id = match validate_id(&id_str) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg]
            ));
        }
    };
    
    Json(ApiResponse::success(
        format!("Karyawan with ID {} deleted successfully", id),
        ()
    ))
}