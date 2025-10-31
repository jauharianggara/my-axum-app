use crate::models::{
    jabatan::{
        ActiveModel as JabatanActiveModel, CreateJabatanRequest, Entity as JabatanEntity,
        Model as Jabatan, UpdateJabatanRequest,
    },
    user::Model as User,
    ApiResponse,
};
use axum::{
    extract::{Json as ExtractJson, Path, State},
    response::Json,
    Extension,
};
use sea_orm::{ActiveModelTrait, DatabaseConnection, EntityTrait, ModelTrait, Set};
use validator::Validate;

// Helper function for ID validation
fn validate_id(id_str: &str) -> Result<i32, String> {
    match id_str.parse::<i32>() {
        Ok(id) if id > 0 => Ok(id),
        Ok(_) => Err("ID harus berupa angka positif yang valid".to_string()),
        Err(_) => Err("ID harus berupa angka positif yang valid".to_string()),
    }
}

// Helper function for validation errors
fn handle_validation_errors(validation_errors: validator::ValidationErrors) -> Vec<String> {
    validation_errors
        .field_errors()
        .iter()
        .flat_map(|(field, errors)| {
            errors.iter().map(move |error| {
                let message = if let Some(msg) = &error.message {
                    msg.to_string()
                } else {
                    "Invalid value".to_string()
                };
                format!("{}: {}", field, message)
            })
        })
        .collect()
}

pub async fn get_all_jabatan(
    State(db): State<DatabaseConnection>,
) -> Json<ApiResponse<Vec<Jabatan>>> {
    match JabatanEntity::find().all(&db).await {
        Ok(jabatan_list) => Json(ApiResponse::success(
            "List of jabatan retrieved successfully".to_string(),
            jabatan_list,
        )),
        Err(err) => Json(ApiResponse::error(
            "Failed to retrieve jabatan".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}

pub async fn get_jabatan_by_id(
    Path(id_str): Path<String>,
    State(db): State<DatabaseConnection>,
) -> Json<ApiResponse<Jabatan>> {
    let id = match validate_id(&id_str) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg],
            ));
        }
    };

    match JabatanEntity::find_by_id(id).one(&db).await {
        Ok(Some(jabatan)) => Json(ApiResponse::success(
            format!("Jabatan with ID {} retrieved successfully", id),
            jabatan,
        )),
        Ok(None) => Json(ApiResponse::error(
            "Jabatan not found".to_string(),
            vec!["Jabatan dengan ID tersebut tidak ditemukan".to_string()],
        )),
        Err(err) => Json(ApiResponse::error(
            "Failed to retrieve jabatan".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}

pub async fn create_jabatan(
    State(db): State<DatabaseConnection>,
    Extension(user): Extension<User>,
    ExtractJson(payload): ExtractJson<CreateJabatanRequest>,
) -> Json<ApiResponse<Jabatan>> {
    if let Err(validation_errors) = payload.validate() {
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            handle_validation_errors(validation_errors),
        ));
    }

    let new_jabatan = JabatanActiveModel {
        nama_jabatan: Set(payload.nama_jabatan),
        deskripsi: Set(payload.deskripsi),
        created_by: Set(Some(user.id)),
        updated_by: Set(Some(user.id)),
        ..Default::default()
    };

    match new_jabatan.insert(&db).await {
        Ok(jabatan) => Json(ApiResponse::success(
            "Jabatan created successfully".to_string(),
            jabatan,
        )),
        Err(err) => Json(ApiResponse::error(
            "Failed to create jabatan".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}

pub async fn update_jabatan(
    Path(id_str): Path<String>,
    State(db): State<DatabaseConnection>,
    Extension(user): Extension<User>,
    ExtractJson(payload): ExtractJson<UpdateJabatanRequest>,
) -> Json<ApiResponse<Jabatan>> {
    let id = match validate_id(&id_str) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg],
            ));
        }
    };

    if let Err(validation_errors) = payload.validate() {
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            handle_validation_errors(validation_errors),
        ));
    }

    let existing_jabatan = match JabatanEntity::find_by_id(id).one(&db).await {
        Ok(Some(jabatan)) => jabatan,
        Ok(None) => {
            return Json(ApiResponse::error(
                "Jabatan not found".to_string(),
                vec!["Jabatan dengan ID tersebut tidak ditemukan".to_string()],
            ));
        }
        Err(err) => {
            return Json(ApiResponse::error(
                "Failed to find jabatan".to_string(),
                vec![format!("Database error: {}", err)],
            ));
        }
    };

    let mut updated_jabatan: JabatanActiveModel = existing_jabatan.into();
    updated_jabatan.nama_jabatan = Set(payload.nama_jabatan);
    updated_jabatan.deskripsi = Set(payload.deskripsi);
    updated_jabatan.updated_by = Set(Some(user.id));

    match updated_jabatan.update(&db).await {
        Ok(jabatan) => Json(ApiResponse::success(
            format!("Jabatan with ID {} updated successfully", id),
            jabatan,
        )),
        Err(err) => Json(ApiResponse::error(
            "Failed to update jabatan".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}

pub async fn delete_jabatan(
    Path(id_str): Path<String>,
    State(db): State<DatabaseConnection>,
) -> Json<ApiResponse<()>> {
    let id = match validate_id(&id_str) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg],
            ));
        }
    };

    let existing_jabatan = match JabatanEntity::find_by_id(id).one(&db).await {
        Ok(Some(jabatan)) => jabatan,
        Ok(None) => {
            return Json(ApiResponse::error(
                "Jabatan not found".to_string(),
                vec!["Jabatan dengan ID tersebut tidak ditemukan".to_string()],
            ));
        }
        Err(err) => {
            return Json(ApiResponse::error(
                "Failed to find jabatan".to_string(),
                vec![format!("Database error: {}", err)],
            ));
        }
    };

    match existing_jabatan.delete(&db).await {
        Ok(_) => Json(ApiResponse::success(
            format!("Jabatan with ID {} deleted successfully", id),
            (),
        )),
        Err(err) => Json(ApiResponse::error(
            "Failed to delete jabatan".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}
