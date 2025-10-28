use crate::models::{ApiResponse, CreateKantorRequest, Kantor, UpdateKantorRequest};
use crate::validators::kantor::{
    handle_validation_errors, validate_id, validate_latitude, validate_longitude,
};
use axum::{
    extract::{Json as ExtractJson, Path},
    response::Json,
};
use validator::Validate;

pub async fn get_all_kantor() -> Json<ApiResponse<Vec<Kantor>>> {
    let kantors = vec![
        Kantor {
            id: Some(1),
            nama: "Kantor Pusat".to_string(),
            alamat: "Jl. Merdeka No.1, Jakarta".to_string(),
            longitude: 106.827153,
            latitude: -6.175110,
        },
        Kantor {
            id: Some(2),
            nama: "Kantor Cabang".to_string(),
            alamat: "Jl. Sudirman No.10, Bandung".to_string(),
            longitude: 107.609810,
            latitude: -6.917464,
        },
    ];

    Json(ApiResponse::success(
        "List of kantors retrieved successfully".to_string(),
        kantors,
    ))
}

pub async fn get_kantor_by_id(Path(id): Path<u32>) -> Json<ApiResponse<Kantor>> {
    // Validasi ID menggunakan function
    let id = match validate_id(&id.to_string()) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg],
            ));
        }
    };

    // Simulasi pengecekan apakah kantor dengan ID tersebut ada
    if id == 0 {
        return Json(ApiResponse::error(
            "Kantor not found".to_string(),
            vec!["Kantor dengan ID tersebut tidak ditemukan".to_string()],
        ));
    }

    let kantor = Kantor {
        id: Some(id),
        nama: "Kantor Pusat".to_string(),
        alamat: "Jl. Merdeka No.1, Jakarta".to_string(),
        longitude: 106.827153,
        latitude: -6.175110,
    };

    Json(ApiResponse::success(
        format!("Kantor with ID {} retrieved successfully", id),
        kantor,
    ))
}

pub async fn create_kantor(
    ExtractJson(payload): ExtractJson<CreateKantorRequest>,
) -> Json<ApiResponse<Kantor>> {
    // Validasi payload
    if let Err(errors) = payload.validate() {
        let error_messages = handle_validation_errors(errors);
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            error_messages,
        ));
    }

    if let Err(error) = validate_longitude(payload.longitude) {
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            vec![
                error
                    .message
                    .unwrap_or_else(|| "Invalid longitude".into())
                    .to_string(),
            ],
        ));
    }

    if let Err(error) = validate_latitude(payload.latitude) {
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            vec![
                error
                    .message
                    .unwrap_or_else(|| "Invalid latitude".into())
                    .to_string(),
            ],
        ));
    }

    let new_kantor = Kantor {
        id: Some(3), // In real app, this would be auto-generated
        nama: payload.nama,
        alamat: payload.alamat,
        longitude: payload.longitude,
        latitude: payload.latitude,
    };

    Json(ApiResponse::success(
        "Kantor created successfully".to_string(),
        new_kantor,
    ))
}

pub async fn update_kantor(
    Path(id): Path<u32>,
    ExtractJson(payload): ExtractJson<UpdateKantorRequest>,
) -> Json<ApiResponse<Kantor>> {
    // Validasi ID menggunakan function
    let id = match validate_id(&id.to_string()) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg],
            ));
        }
    };

    // Validasi payload
    if let Err(errors) = payload.validate() {
        let error_messages = handle_validation_errors(errors);
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            error_messages,
        ));
    }

    if let Err(error) = validate_longitude(payload.longitude) {
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            vec![
                error
                    .message
                    .unwrap_or_else(|| "Invalid longitude".into())
                    .to_string(),
            ],
        ));
    }

    if let Err(error) = validate_latitude(payload.latitude) {
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            vec![
                error
                    .message
                    .unwrap_or_else(|| "Invalid latitude".into())
                    .to_string(),
            ],
        ));
    }

    let updated_kantor = Kantor {
        id: Some(id),
        nama: payload.nama,
        alamat: payload.alamat,
        longitude: payload.longitude,
        latitude: payload.latitude,
    };

    Json(ApiResponse::success(
        format!("Kantor with ID {} updated successfully", id),
        updated_kantor,
    ))
}

pub async fn delete_kantor(Path(id): Path<u32>) -> Json<ApiResponse<()>> {
    // Validasi ID menggunakan function
    let id = match validate_id(&id.to_string()) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg],
            ));
        }
    };

    Json(ApiResponse::success(
        format!("Kantor with ID {} deleted successfully", id),
        (),
    ))
}