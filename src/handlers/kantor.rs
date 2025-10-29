use crate::models::{ApiResponse, kantor::{Entity as KantorEntity, Model as Kantor, ActiveModel as KantorActiveModel, CreateKantorRequest, UpdateKantorRequest}};
use crate::validators::kantor::{
    handle_validation_errors, validate_id, validate_latitude, validate_longitude,
};
use axum::{
    extract::{Json as ExtractJson, Path, State},
    response::Json,
};
use sea_orm::{DatabaseConnection, EntityTrait, ActiveModelTrait, Set, ModelTrait};
use validator::Validate;
use rust_decimal::Decimal;
use std::str::FromStr;

pub async fn get_all_kantor(State(db): State<DatabaseConnection>) -> Json<ApiResponse<Vec<Kantor>>> {
    match KantorEntity::find().all(&db).await {
        Ok(kantors) => {
            Json(ApiResponse::success(
                "List of kantors retrieved successfully".to_string(),
                kantors,
            ))
        }
        Err(err) => {
            Json(ApiResponse::error(
                "Failed to retrieve kantors".to_string(),
                vec![format!("Database error: {}", err)]
            ))
        }
    }
}

pub async fn get_kantor_by_id(
    Path(id): Path<String>,
    State(db): State<DatabaseConnection>
) -> Json<ApiResponse<Kantor>> {
    // Validasi ID menggunakan function
    let id = match validate_id(&id) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg],
            ));
        }
    };

    match KantorEntity::find_by_id(id).one(&db).await {
        Ok(Some(kantor)) => {
            Json(ApiResponse::success(
                format!("Kantor with ID {} retrieved successfully", id),
                kantor,
            ))
        }
        Ok(None) => {
            Json(ApiResponse::error(
                "Kantor not found".to_string(),
                vec!["Kantor dengan ID tersebut tidak ditemukan".to_string()],
            ))
        }
        Err(err) => {
            Json(ApiResponse::error(
                "Failed to retrieve kantor".to_string(),
                vec![format!("Database error: {}", err)]
            ))
        }
    }
}

pub async fn create_kantor(
    State(db): State<DatabaseConnection>,
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

    let longitude = match Decimal::from_str(&payload.longitude.to_string()) {
        Ok(val) => val,
        Err(_) => {
            return Json(ApiResponse::error(
                "Invalid longitude format".to_string(),
                vec!["Longitude harus berupa angka desimal yang valid".to_string()]
            ));
        }
    };

    let latitude = match Decimal::from_str(&payload.latitude.to_string()) {
        Ok(val) => val,
        Err(_) => {
            return Json(ApiResponse::error(
                "Invalid latitude format".to_string(),
                vec!["Latitude harus berupa angka desimal yang valid".to_string()]
            ));
        }
    };

    let new_kantor = KantorActiveModel {
        nama: Set(payload.nama),
        alamat: Set(payload.alamat),
        longitude: Set(longitude),
        latitude: Set(latitude),
        ..Default::default()
    };

    match new_kantor.insert(&db).await {
        Ok(kantor) => {
            Json(ApiResponse::success(
                "Kantor created successfully".to_string(),
                kantor,
            ))
        }
        Err(err) => {
            Json(ApiResponse::error(
                "Failed to create kantor".to_string(),
                vec![format!("Database error: {}", err)]
            ))
        }
    }
}

pub async fn update_kantor(
    Path(id): Path<String>,
    State(db): State<DatabaseConnection>,
    ExtractJson(payload): ExtractJson<UpdateKantorRequest>,
) -> Json<ApiResponse<Kantor>> {
    // Validasi ID menggunakan function
    let id = match validate_id(&id) {
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

    // Check if kantor exists
    let existing_kantor = match KantorEntity::find_by_id(id).one(&db).await {
        Ok(Some(kantor)) => kantor,
        Ok(None) => {
            return Json(ApiResponse::error(
                "Kantor not found".to_string(),
                vec!["Kantor dengan ID tersebut tidak ditemukan".to_string()],
            ));
        }
        Err(err) => {
            return Json(ApiResponse::error(
                "Failed to find kantor".to_string(),
                vec![format!("Database error: {}", err)]
            ));
        }
    };

    let longitude = match Decimal::from_str(&payload.longitude.to_string()) {
        Ok(val) => val,
        Err(_) => {
            return Json(ApiResponse::error(
                "Invalid longitude format".to_string(),
                vec!["Longitude harus berupa angka desimal yang valid".to_string()]
            ));
        }
    };

    let latitude = match Decimal::from_str(&payload.latitude.to_string()) {
        Ok(val) => val,
        Err(_) => {
            return Json(ApiResponse::error(
                "Invalid latitude format".to_string(),
                vec!["Latitude harus berupa angka desimal yang valid".to_string()]
            ));
        }
    };

    let mut updated_kantor: KantorActiveModel = existing_kantor.into();
    updated_kantor.nama = Set(payload.nama);
    updated_kantor.alamat = Set(payload.alamat);
    updated_kantor.longitude = Set(longitude);
    updated_kantor.latitude = Set(latitude);

    match updated_kantor.update(&db).await {
        Ok(kantor) => {
            Json(ApiResponse::success(
                format!("Kantor with ID {} updated successfully", id),
                kantor,
            ))
        }
        Err(err) => {
            Json(ApiResponse::error(
                "Failed to update kantor".to_string(),
                vec![format!("Database error: {}", err)]
            ))
        }
    }
}

pub async fn delete_kantor(
    Path(id): Path<String>,
    State(db): State<DatabaseConnection>
) -> Json<ApiResponse<()>> {
    // Validasi ID menggunakan function
    let id = match validate_id(&id) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg],
            ));
        }
    };

    // Check if kantor exists
    let existing_kantor = match KantorEntity::find_by_id(id).one(&db).await {
        Ok(Some(kantor)) => kantor,
        Ok(None) => {
            return Json(ApiResponse::error(
                "Kantor not found".to_string(),
                vec!["Kantor dengan ID tersebut tidak ditemukan".to_string()],
            ));
        }
        Err(err) => {
            return Json(ApiResponse::error(
                "Failed to find kantor".to_string(),
                vec![format!("Database error: {}", err)]
            ));
        }
    };

    match existing_kantor.delete(&db).await {
        Ok(_) => {
            Json(ApiResponse::success(
                format!("Kantor with ID {} deleted successfully", id),
                (),
            ))
        }
        Err(err) => {
            Json(ApiResponse::error(
                "Failed to delete kantor".to_string(),
                vec![format!("Database error: {}", err)]
            ))
        }
    }
}