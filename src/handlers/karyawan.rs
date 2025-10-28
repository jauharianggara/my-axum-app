use crate::models::{
    ApiResponse,
    kantor::Entity as KantorEntity,
    karyawan::{
        ActiveModel as KaryawanActiveModel, CreateKaryawanRequest, Entity as KaryawanEntity,
        Model as Karyawan, UpdateKaryawanRequest,
    },
};
use crate::validators::karyawan::{handle_validation_errors, validate_id};
use axum::{
    extract::{Extension, Json as ExtractJson, Path},
    response::Json,
};
use sea_orm::{
    ActiveModelTrait, DatabaseConnection, EntityTrait, LoaderTrait, ModelTrait, Set,
    prelude::DateTimeWithTimeZone,
};
use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Serialize, Deserialize, Debug)]
pub struct KaryawanWithKantor {
    pub id: i32,
    pub nama: String,
    pub posisi: String,
    pub gaji: i32,
    pub kantor_id: i32,
    pub kantor_nama: Option<String>,
    pub created_at: DateTimeWithTimeZone,
    pub updated_at: DateTimeWithTimeZone,
}

pub async fn get_all_karyawan_with_kantor(
    Extension(db): Extension<DatabaseConnection>,
) -> Json<ApiResponse<Vec<KaryawanWithKantor>>> {
    match KaryawanEntity::find().all(&db).await {
        Ok(karyawans) => {
            // Load related kantor data using Sea-ORM loader
            match karyawans.load_one(KantorEntity, &db).await {
                Ok(kantors) => {
                    let karyawan_with_kantor: Vec<KaryawanWithKantor> = karyawans
                        .into_iter()
                        .zip(kantors.into_iter())
                        .map(|(karyawan, kantor)| KaryawanWithKantor {
                            id: karyawan.id,
                            nama: karyawan.nama,
                            posisi: karyawan.posisi,
                            gaji: karyawan.gaji,
                            kantor_id: karyawan.kantor_id,
                            kantor_nama: kantor.map(|k| k.nama),
                            created_at: karyawan.created_at,
                            updated_at: karyawan.updated_at,
                        })
                        .collect();

                    Json(ApiResponse::success(
                        "List of karyawans with kantor retrieved successfully".to_string(),
                        karyawan_with_kantor,
                    ))
                }
                Err(err) => Json(ApiResponse::error(
                    "Failed to load kantor data".to_string(),
                    vec![format!("Database error: {}", err)],
                )),
            }
        }
        Err(err) => Json(ApiResponse::error(
            "Failed to retrieve karyawans".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}

pub async fn get_all_karyawan(
    Extension(db): Extension<DatabaseConnection>,
) -> Json<ApiResponse<Vec<Karyawan>>> {
    match KaryawanEntity::find().all(&db).await {
        Ok(karyawans) => Json(ApiResponse::success(
            "List of karyawans retrieved successfully".to_string(),
            karyawans,
        )),
        Err(err) => Json(ApiResponse::error(
            "Failed to retrieve karyawans".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}

pub async fn get_karyawan_with_kantor_by_id(
    Path(id_str): Path<String>,
    Extension(db): Extension<DatabaseConnection>,
) -> Json<ApiResponse<KaryawanWithKantor>> {
    // Validasi ID menggunakan function
    let id = match validate_id(&id_str) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg],
            ));
        }
    };

    match KaryawanEntity::find_by_id(id).one(&db).await {
        Ok(Some(karyawan)) => {
            // Load related kantor data
            let kantor_nama = match karyawan.find_related(KantorEntity).one(&db).await {
                Ok(kantor) => kantor.map(|k| k.nama),
                Err(_) => None,
            };

            let karyawan_with_kantor = KaryawanWithKantor {
                id: karyawan.id,
                nama: karyawan.nama,
                posisi: karyawan.posisi,
                gaji: karyawan.gaji,
                kantor_id: karyawan.kantor_id,
                kantor_nama,
                created_at: karyawan.created_at,
                updated_at: karyawan.updated_at,
            };

            Json(ApiResponse::success(
                format!(
                    "Karyawan with ID {} and kantor info retrieved successfully",
                    id
                ),
                karyawan_with_kantor,
            ))
        }
        Ok(None) => Json(ApiResponse::error(
            "Karyawan not found".to_string(),
            vec!["Karyawan dengan ID tersebut tidak ditemukan".to_string()],
        )),
        Err(err) => Json(ApiResponse::error(
            "Failed to retrieve karyawan".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}

pub async fn get_karyawan_by_id(
    Path(id_str): Path<String>,
    Extension(db): Extension<DatabaseConnection>,
) -> Json<ApiResponse<Karyawan>> {
    // Validasi ID menggunakan function
    let id = match validate_id(&id_str) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg],
            ));
        }
    };

    match KaryawanEntity::find_by_id(id).one(&db).await {
        Ok(Some(karyawan)) => Json(ApiResponse::success(
            format!("Karyawan with ID {} retrieved successfully", id),
            karyawan,
        )),
        Ok(None) => Json(ApiResponse::error(
            "Karyawan not found".to_string(),
            vec!["Karyawan dengan ID tersebut tidak ditemukan".to_string()],
        )),
        Err(err) => Json(ApiResponse::error(
            "Failed to retrieve karyawan".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}

pub async fn create_karyawan(
    Extension(db): Extension<DatabaseConnection>,
    ExtractJson(payload): ExtractJson<CreateKaryawanRequest>,
) -> Json<ApiResponse<Karyawan>> {
    // Validate the payload
    if let Err(validation_errors) = payload.validate() {
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            handle_validation_errors(validation_errors),
        ));
    }

    // Parse kantor_id - allow empty/null for freelancers
    let kantor_id = match payload.kantor_id.parse::<i32>() {
        Ok(kantor_id) => kantor_id,
        Err(_) => {
            return Json(ApiResponse::error(
                "Invalid kantor_id format".to_string(),
                vec!["kantor_id harus berupa angka positif yang valid atau kosong untuk freelancer".to_string()],
            ));
        }
    }; 

    let gaji = match payload.gaji.parse::<i32>() {
        Ok(gaji) => gaji,
        Err(_) => {
            return Json(ApiResponse::error(
                "Invalid gaji format".to_string(),
                vec!["Gaji harus berupa angka yang valid".to_string()],
            ));
        }
    };

    let new_karyawan = KaryawanActiveModel {
        nama: Set(payload.nama),
        posisi: Set(payload.posisi),
        gaji: Set(gaji),
        kantor_id: Set(kantor_id),
        ..Default::default()
    };

    match new_karyawan.insert(&db).await {
        Ok(karyawan) => Json(ApiResponse::success(
            "Karyawan created successfully".to_string(),
            karyawan,
        )),
        Err(err) => Json(ApiResponse::error(
            "Failed to create karyawan".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}

pub async fn update_karyawan(
    Path(id_str): Path<String>,
    Extension(db): Extension<DatabaseConnection>,
    ExtractJson(payload): ExtractJson<UpdateKaryawanRequest>,
) -> Json<ApiResponse<Karyawan>> {
    // Validasi ID menggunakan function
    let id = match validate_id(&id_str) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg],
            ));
        }
    };

    // Validate the payload
    if let Err(validation_errors) = payload.validate() {
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            handle_validation_errors(validation_errors),
        ));
    }

    // Parse kantor_id - allow empty/null for freelancers
    let kantor_id = match payload.kantor_id.parse::<i32>() {
        Ok(kantor_id) => kantor_id,
        Err(_) => {
            return Json(ApiResponse::error(
                "Invalid kantor_id format".to_string(),
                vec!["kantor_id harus berupa angka positif yang valid atau kosong untuk freelancer".to_string()],
            ));
        }
    };

    let gaji = match payload.gaji.parse::<i32>() {
        Ok(gaji) => gaji,
        Err(_) => {
            return Json(ApiResponse::error(
                "Invalid gaji format".to_string(),
                vec!["Gaji harus berupa angka yang valid".to_string()],
            ));
        }
    };

    // Check if karyawan exists
    let existing_karyawan = match KaryawanEntity::find_by_id(id).one(&db).await {
        Ok(Some(karyawan)) => karyawan,
        Ok(None) => {
            return Json(ApiResponse::error(
                "Karyawan not found".to_string(),
                vec!["Karyawan dengan ID tersebut tidak ditemukan".to_string()],
            ));
        }
        Err(err) => {
            return Json(ApiResponse::error(
                "Failed to find karyawan".to_string(),
                vec![format!("Database error: {}", err)],
            ));
        }
    };

    let mut updated_karyawan: KaryawanActiveModel = existing_karyawan.into();
    updated_karyawan.nama = Set(payload.nama);
    updated_karyawan.posisi = Set(payload.posisi);
    updated_karyawan.gaji = Set(gaji);
    updated_karyawan.kantor_id = Set(kantor_id);

    match updated_karyawan.update(&db).await {
        Ok(karyawan) => Json(ApiResponse::success(
            format!("Karyawan with ID {} updated successfully", id),
            karyawan,
        )),
        Err(err) => Json(ApiResponse::error(
            "Failed to update karyawan".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}

pub async fn delete_karyawan(
    Path(id_str): Path<String>,
    Extension(db): Extension<DatabaseConnection>,
) -> Json<ApiResponse<()>> {
    // Validasi ID menggunakan function
    let id = match validate_id(&id_str) {
        Ok(id) => id,
        Err(error_msg) => {
            return Json(ApiResponse::error(
                "Invalid ID format".to_string(),
                vec![error_msg],
            ));
        }
    };

    // Check if karyawan exists
    let existing_karyawan = match KaryawanEntity::find_by_id(id).one(&db).await {
        Ok(Some(karyawan)) => karyawan,
        Ok(None) => {
            return Json(ApiResponse::error(
                "Karyawan not found".to_string(),
                vec!["Karyawan dengan ID tersebut tidak ditemukan".to_string()],
            ));
        }
        Err(err) => {
            return Json(ApiResponse::error(
                "Failed to find karyawan".to_string(),
                vec![format!("Database error: {}", err)],
            ));
        }
    };

    match existing_karyawan.delete(&db).await {
        Ok(_) => Json(ApiResponse::success(
            format!("Karyawan with ID {} deleted successfully", id),
            (),
        )),
        Err(err) => Json(ApiResponse::error(
            "Failed to delete karyawan".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}
