use crate::models::{
    kantor::Entity as KantorEntity,
    karyawan::{
        ActiveModel as KaryawanActiveModel, CreateKaryawanRequest, Entity as KaryawanEntity,
        Model as Karyawan, UpdateKaryawanRequest,
    },
    user::{Model as User, Entity as UserEntity, ActiveModel as UserActiveModel},
    ApiResponse,
};
use crate::validators::karyawan::{handle_validation_errors, validate_id, validate_kantor_id_exists};
use crate::services::file_upload::{FileUploadService, UploadedFile};
use crate::services::auth::PasswordService;
use axum::{
    extract::{State, Json as ExtractJson, Path, Multipart},
    Extension,
    response::Json,
};
use sea_orm::{
    prelude::DateTimeWithTimeZone, ActiveModelTrait, DatabaseConnection, EntityTrait, LoaderTrait,
    ModelTrait, Set, QueryFilter, ColumnTrait,
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
    pub foto_path: Option<String>,
    pub foto_original_name: Option<String>,
    pub foto_size: Option<i64>,
    pub foto_mime_type: Option<String>,
    pub user_id: Option<i32>,
    pub created_by: Option<i32>,
    pub updated_by: Option<i32>,
    pub created_at: DateTimeWithTimeZone,
    pub updated_at: DateTimeWithTimeZone,
}

pub async fn get_all_karyawan_with_kantor(
    State(db): State<DatabaseConnection>,
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
                            foto_path: karyawan.foto_path,
                            foto_original_name: karyawan.foto_original_name,
                            foto_size: karyawan.foto_size,
                            foto_mime_type: karyawan.foto_mime_type,
                            user_id: karyawan.user_id,
                            created_by: karyawan.created_by,
                            updated_by: karyawan.updated_by,
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
    State(db): State<DatabaseConnection>,
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
    State(db): State<DatabaseConnection>,
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
                foto_path: karyawan.foto_path,
                foto_original_name: karyawan.foto_original_name,
                foto_size: karyawan.foto_size,
                foto_mime_type: karyawan.foto_mime_type,
                user_id: karyawan.user_id,
                created_by: karyawan.created_by,
                updated_by: karyawan.updated_by,
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
    State(db): State<DatabaseConnection>,
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
    State(db): State<DatabaseConnection>,
    Extension(user): Extension<User>,
    ExtractJson(payload): ExtractJson<CreateKaryawanRequest>,
) -> Json<ApiResponse<Karyawan>> {
    // Validate the payload
    if let Err(validation_errors) = payload.validate() {
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            handle_validation_errors(validation_errors),
        ));
    }

    let kantor_id = match payload.kantor_id.parse::<i32>() {
        Ok(kantor_id) => kantor_id,
        Err(_) => {
            return Json(ApiResponse::error(
                "Invalid kantor_id format".to_string(),
                vec![
                    "kantor_id wajib diisi dan harus berupa angka positif yang valid"
                        .to_string(),
                ],
            ));
        }
    };

    // Validasi apakah kantor_id ada di database
    if let Err(error_msg) = validate_kantor_id_exists(kantor_id, &db).await {
        return Json(ApiResponse::error(
            "Invalid kantor_id".to_string(),
            vec![error_msg],
        ));
    }

    let gaji = match payload.gaji.parse::<i32>() {
        Ok(gaji) => gaji,
        Err(_) => {
            return Json(ApiResponse::error(
                "Invalid gaji format".to_string(),
                vec!["Gaji harus berupa angka yang valid".to_string()],
            ));
        }
    };

    // Parse user_id if provided
    let mut user_id = match payload.user_id {
        Some(ref uid) => match uid.parse::<i32>() {
            Ok(id) => Some(id),
            Err(_) => {
                return Json(ApiResponse::error(
                    "Invalid user_id format".to_string(),
                    vec!["user_id harus berupa angka yang valid".to_string()],
                ));
            }
        },
        None => None,
    };

    // Auto-create user if user_id is not provided
    if user_id.is_none() {
        // Generate username from nama (lowercase, remove spaces)
        let username = payload.nama.to_lowercase().replace(" ", "");
        
        // Generate email from username
        let email = format!("{}@karyawan.local", username);
        
        // Check if username already exists
        let existing_user = UserEntity::find()
            .filter(crate::models::user::Column::Username.eq(&username))
            .one(&db)
            .await;
        
        match existing_user {
            Ok(None) => {
                // User doesn't exist, create new user
                let default_password = "12345678";
                let password_hash = match PasswordService::hash_password(default_password) {
                    Ok(hash) => hash,
                    Err(e) => {
                        return Json(ApiResponse::error(
                            "Failed to hash password".to_string(),
                            vec![format!("Error: {}", e)],
                        ));
                    }
                };
                
                let new_user = UserActiveModel {
                    username: Set(username.clone()),
                    email: Set(email),
                    password_hash: Set(password_hash),
                    full_name: Set(Some(payload.nama.clone())),
                    is_active: Set(true),
                    ..Default::default()
                };
                
                match new_user.insert(&db).await {
                    Ok(created_user) => {
                        user_id = Some(created_user.id);
                    }
                    Err(e) => {
                        return Json(ApiResponse::error(
                            "Failed to create user account".to_string(),
                            vec![format!("Database error: {}", e)],
                        ));
                    }
                }
            }
            Ok(Some(existing)) => {
                // User already exists, use existing user_id
                user_id = Some(existing.id);
            }
            Err(e) => {
                return Json(ApiResponse::error(
                    "Failed to check existing user".to_string(),
                    vec![format!("Database error: {}", e)],
                ));
            }
        }
    }

    let new_karyawan = KaryawanActiveModel {
        nama: Set(payload.nama),
        posisi: Set(payload.posisi),
        gaji: Set(gaji),
        kantor_id: Set(kantor_id),
        user_id: Set(user_id),
        created_by: Set(Some(user.id)),
        updated_by: Set(Some(user.id)),
        foto_path: Set(None),
        foto_original_name: Set(None),
        foto_size: Set(None),
        foto_mime_type: Set(None),
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
    State(db): State<DatabaseConnection>,
    Extension(user): Extension<User>,
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

    let kantor_id = match payload.kantor_id.parse::<i32>() {
        Ok(kantor_id) => kantor_id,
        Err(_) => {
            return Json(ApiResponse::error(
                "Invalid kantor_id format".to_string(),
                vec![
                    "kantor_id wajib diisi dan harus berupa angka positif yang valid"
                        .to_string(),
                ],
            ));
        }
    };

    // Validasi apakah kantor_id ada di database
    if let Err(error_msg) = validate_kantor_id_exists(kantor_id, &db).await {
        return Json(ApiResponse::error(
            "Invalid kantor_id".to_string(),
            vec![error_msg],
        ));
    }

    let gaji = match payload.gaji.parse::<i32>() {
        Ok(gaji) => gaji,
        Err(_) => {
            return Json(ApiResponse::error(
                "Invalid gaji format".to_string(),
                vec!["Gaji harus berupa angka yang valid".to_string()],
            ));
        }
    };

    // Parse user_id if provided
    let user_id = match payload.user_id {
        Some(ref uid) => match uid.parse::<i32>() {
            Ok(id) => Some(id),
            Err(_) => {
                return Json(ApiResponse::error(
                    "Invalid user_id format".to_string(),
                    vec!["user_id harus berupa angka yang valid".to_string()],
                ));
            }
        },
        None => None,
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
    updated_karyawan.user_id = Set(user_id);
    updated_karyawan.updated_by = Set(Some(user.id));

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
    State(db): State<DatabaseConnection>,
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

    // Delete the physical photo file if it exists
    if let Some(foto_path) = &existing_karyawan.foto_path {
        let _ = FileUploadService::delete_karyawan_photo(foto_path).await;
    }

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

pub async fn create_karyawan_with_photo(
    State(db): State<DatabaseConnection>,
    Extension(user): Extension<User>,
    mut multipart: Multipart,
) -> Json<ApiResponse<Karyawan>> {
    let mut karyawan_data: Option<CreateKaryawanRequest> = None;
    let mut uploaded_file: Option<UploadedFile> = None;

    // Process multipart form data
    while let Some(field) = multipart.next_field().await.unwrap_or(None) {
        let name = field.name().unwrap_or("").to_string();

        match name.as_str() {
            "nama" | "posisi" | "gaji" | "kantor_id" | "user_id" => {
                let value = field.text().await.unwrap_or_default();
                
                // Build the karyawan data incrementally
                if karyawan_data.is_none() {
                    karyawan_data = Some(CreateKaryawanRequest {
                        nama: String::new(),
                        posisi: String::new(),
                        gaji: String::new(),
                        kantor_id: String::new(),
                        user_id: None,
                    });
                }

                if let Some(ref mut data) = karyawan_data {
                    match name.as_str() {
                        "nama" => data.nama = value,
                        "posisi" => data.posisi = value,
                        "gaji" => data.gaji = value,
                        "kantor_id" => data.kantor_id = value,
                        "user_id" => data.user_id = if value.is_empty() { None } else { Some(value) },
                        _ => {}
                    }
                }
            }
            "foto" => {
                match FileUploadService::save_karyawan_photo(field, None).await {
                    Ok(file) => uploaded_file = Some(file),
                    Err(err) => {
                        return Json(ApiResponse::error(
                            "Failed to upload photo".to_string(),
                            vec![err.to_string()],
                        ));
                    }
                }
            }
            _ => {} // Ignore unknown fields
        }
    }

    let payload = match karyawan_data {
        Some(data) => data,
        None => {
            return Json(ApiResponse::error(
                "Missing karyawan data".to_string(),
                vec!["Nama, posisi, gaji, dan kantor_id diperlukan".to_string()],
            ));
        }
    };

    // Validate the payload
    if let Err(validation_errors) = payload.validate() {
        // Clean up uploaded file if validation fails
        if let Some(file) = uploaded_file {
            let _ = FileUploadService::delete_karyawan_photo(&file.file_path).await;
        }
        
        return Json(ApiResponse::error(
            "Validation failed".to_string(),
            handle_validation_errors(validation_errors),
        ));
    }

    let kantor_id = match payload.kantor_id.parse::<i32>() {
        Ok(kantor_id) => kantor_id,
        Err(_) => {
            // Clean up uploaded file if parsing fails
            if let Some(file) = uploaded_file {
                let _ = FileUploadService::delete_karyawan_photo(&file.file_path).await;
            }
            
            return Json(ApiResponse::error(
                "Invalid kantor_id format".to_string(),
                vec![
                    "kantor_id wajib diisi dan harus berupa angka positif yang valid"
                        .to_string(),
                ],
            ));
        }
    };

    // Validasi apakah kantor_id ada di database
    if let Err(error_msg) = validate_kantor_id_exists(kantor_id, &db).await {
        // Clean up uploaded file if validation fails
        if let Some(file) = uploaded_file {
            let _ = FileUploadService::delete_karyawan_photo(&file.file_path).await;
        }
        
        return Json(ApiResponse::error(
            "Invalid kantor_id".to_string(),
            vec![error_msg],
        ));
    }

    let gaji = match payload.gaji.parse::<i32>() {
        Ok(gaji) => gaji,
        Err(_) => {
            // Clean up uploaded file if parsing fails
            if let Some(file) = uploaded_file {
                let _ = FileUploadService::delete_karyawan_photo(&file.file_path).await;
            }
            
            return Json(ApiResponse::error(
                "Invalid gaji format".to_string(),
                vec!["Gaji harus berupa angka yang valid".to_string()],
            ));
        }
    };

    // Parse user_id if provided
    let mut user_id = match payload.user_id {
        Some(ref uid) => match uid.parse::<i32>() {
            Ok(id) => Some(id),
            Err(_) => {
                // Clean up uploaded file if parsing fails
                if let Some(file) = &uploaded_file {
                    let _ = FileUploadService::delete_karyawan_photo(&file.file_path).await;
                }
                
                return Json(ApiResponse::error(
                    "Invalid user_id format".to_string(),
                    vec!["user_id harus berupa angka yang valid".to_string()],
                ));
            }
        },
        None => None,
    };

    // Auto-create user if user_id is not provided
    if user_id.is_none() {
        // Generate username from nama (lowercase, remove spaces)
        let username = payload.nama.to_lowercase().replace(" ", "");
        
        // Generate email from username
        let email = format!("{}@karyawan.local", username);
        
        // Check if username already exists
        let existing_user = UserEntity::find()
            .filter(crate::models::user::Column::Username.eq(&username))
            .one(&db)
            .await;
        
        match existing_user {
            Ok(None) => {
                // User doesn't exist, create new user
                let default_password = "12345678";
                let password_hash = match PasswordService::hash_password(default_password) {
                    Ok(hash) => hash,
                    Err(e) => {
                        // Clean up uploaded file if password hashing fails
                        if let Some(file) = &uploaded_file {
                            let _ = FileUploadService::delete_karyawan_photo(&file.file_path).await;
                        }
                        
                        return Json(ApiResponse::error(
                            "Failed to hash password".to_string(),
                            vec![format!("Error: {}", e)],
                        ));
                    }
                };
                
                let new_user = UserActiveModel {
                    username: Set(username.clone()),
                    email: Set(email),
                    password_hash: Set(password_hash),
                    full_name: Set(Some(payload.nama.clone())),
                    is_active: Set(true),
                    ..Default::default()
                };
                
                match new_user.insert(&db).await {
                    Ok(created_user) => {
                        user_id = Some(created_user.id);
                    }
                    Err(e) => {
                        // Clean up uploaded file if user creation fails
                        if let Some(file) = &uploaded_file {
                            let _ = FileUploadService::delete_karyawan_photo(&file.file_path).await;
                        }
                        
                        return Json(ApiResponse::error(
                            "Failed to create user account".to_string(),
                            vec![format!("Database error: {}", e)],
                        ));
                    }
                }
            }
            Ok(Some(existing)) => {
                // User already exists, use existing user_id
                user_id = Some(existing.id);
            }
            Err(e) => {
                // Clean up uploaded file if database check fails
                if let Some(file) = &uploaded_file {
                    let _ = FileUploadService::delete_karyawan_photo(&file.file_path).await;
                }
                
                return Json(ApiResponse::error(
                    "Failed to check existing user".to_string(),
                    vec![format!("Database error: {}", e)],
                ));
            }
        }
    }

    let new_karyawan = KaryawanActiveModel {
        nama: Set(payload.nama),
        posisi: Set(payload.posisi),
        gaji: Set(gaji),
        kantor_id: Set(kantor_id),
        user_id: Set(user_id),
        created_by: Set(Some(user.id)),
        updated_by: Set(Some(user.id)),
        foto_path: Set(uploaded_file.as_ref().map(|f| f.file_path.clone())),
        foto_original_name: Set(uploaded_file.as_ref().map(|f| f.original_name.clone())),
        foto_size: Set(uploaded_file.as_ref().map(|f| f.size)),
        foto_mime_type: Set(uploaded_file.as_ref().map(|f| f.mime_type.clone())),
        ..Default::default()
    };

    match new_karyawan.insert(&db).await {
        Ok(karyawan) => Json(ApiResponse::success(
            "Karyawan created successfully with photo".to_string(),
            karyawan,
        )),
        Err(err) => {
            // Clean up uploaded file if database insertion fails
            if let Some(file) = uploaded_file {
                let _ = FileUploadService::delete_karyawan_photo(&file.file_path).await;
            }
            
            Json(ApiResponse::error(
                "Failed to create karyawan".to_string(),
                vec![format!("Database error: {}", err)],
            ))
        }
    }
}

pub async fn upload_karyawan_photo(
    Path(id_str): Path<String>,
    State(db): State<DatabaseConnection>,
    Extension(user): Extension<User>,
    mut multipart: Multipart,
) -> Json<ApiResponse<Karyawan>> {
    // Validasi ID
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

    // Process multipart form data to get the photo
    let mut uploaded_file: Option<UploadedFile> = None;
    
    while let Some(field) = multipart.next_field().await.unwrap_or(None) {
        let name = field.name().unwrap_or("").to_string();
        
        if name == "foto" {
            match FileUploadService::update_karyawan_photo(
                field, 
                id, 
                existing_karyawan.foto_path.as_deref()
            ).await {
                Ok(file) => uploaded_file = Some(file),
                Err(err) => {
                    return Json(ApiResponse::error(
                        "Failed to upload photo".to_string(),
                        vec![err.to_string()],
                    ));
                }
            }
            break;
        }
    }

    let uploaded_file = match uploaded_file {
        Some(file) => file,
        None => {
            return Json(ApiResponse::error(
                "No photo file provided".to_string(),
                vec!["Field 'foto' diperlukan untuk upload foto".to_string()],
            ));
        }
    };

    // Update database with new photo info
    let mut updated_karyawan: KaryawanActiveModel = existing_karyawan.into();
    updated_karyawan.foto_path = Set(Some(uploaded_file.file_path));
    updated_karyawan.foto_original_name = Set(Some(uploaded_file.original_name));
    updated_karyawan.foto_size = Set(Some(uploaded_file.size));
    updated_karyawan.foto_mime_type = Set(Some(uploaded_file.mime_type));
    updated_karyawan.updated_by = Set(Some(user.id));

    match updated_karyawan.update(&db).await {
        Ok(karyawan) => Json(ApiResponse::success(
            format!("Photo uploaded successfully for karyawan ID {}", id),
            karyawan,
        )),
        Err(err) => Json(ApiResponse::error(
            "Failed to update karyawan with photo info".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}

pub async fn delete_karyawan_photo(
    Path(id_str): Path<String>,
    State(db): State<DatabaseConnection>,
    Extension(user): Extension<User>,
) -> Json<ApiResponse<Karyawan>> {
    // Validasi ID
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

    // Delete the physical file if it exists
    if let Some(foto_path) = &existing_karyawan.foto_path {
        let _ = FileUploadService::delete_karyawan_photo(foto_path).await;
    }

    // Update database to remove photo info
    let mut updated_karyawan: KaryawanActiveModel = existing_karyawan.into();
    updated_karyawan.foto_path = Set(None);
    updated_karyawan.foto_original_name = Set(None);
    updated_karyawan.foto_size = Set(None);
    updated_karyawan.foto_mime_type = Set(None);
    updated_karyawan.updated_by = Set(Some(user.id));

    match updated_karyawan.update(&db).await {
        Ok(karyawan) => Json(ApiResponse::success(
            format!("Photo deleted successfully for karyawan ID {}", id),
            karyawan,
        )),
        Err(err) => Json(ApiResponse::error(
            "Failed to update karyawan after photo deletion".to_string(),
            vec![format!("Database error: {}", err)],
        )),
    }
}
