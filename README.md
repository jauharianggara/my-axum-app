# My Axum App - Employee Management API

A robust REST API built with Rust and Axum for employee (karyawan) management with comprehensive validation.

## 🏗️ Project Structure

```
my-axum-app/
├── src/
│   ├── main.rs           # Application entry point and routing
│   ├── models/           # Data structures and schemas
│   │   └── mod.rs        # Karyawan, CreateKaryawanRequest, ApiResponse
│   ├── handlers/         # HTTP request handlers
│   │   └── mod.rs        # CRUD operations for karyawan
│   └── validators/       # Validation logic
│       └── mod.rs        # Custom validation functions
├── Cargo.toml           # Dependencies and project metadata
├── test_validation.ps1  # PowerShell test script
└── README.md           # This file
```

## 🚀 Features

- **Complete CRUD Operations** for Employee management
- **Comprehensive Validation**:
  - Name: 2-50 characters
  - Position: 2-30 characters  
  - Salary: 1,000,000 - 100,000,000 (accepts string or number)
  - ID: Must be positive integer
- **Robust Error Handling** with consistent JSON responses
- **Modular Architecture** following Rust best practices
- **Type-Safe** request/response handling

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/karyawans` | List all employees |
| GET | `/karyawans/{id}` | Get employee by ID |
| POST | `/karyawans` | Create new employee |
| PUT | `/karyawans/{id}` | Update employee |
| DELETE | `/karyawans/{id}` | Delete employee |

## 🔧 Usage

### Start the server:
```bash
cargo run
```

### Example requests:

**Create Employee:**
```bash
curl -X POST http://localhost:3000/karyawans \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "John Doe",
    "posisi": "Software Engineer", 
    "gaji": "8000000"
  }'
```

**Response Format:**
```json
{
  "success": true,
  "message": "Karyawan created successfully",
  "data": {
    "id": 3,
    "nama": "John Doe",
    "posisi": "Software Engineer",
    "gaji": 8000000
  },
  "errors": null
}
```

**Validation Error Example:**
```json
{
  "success": false,
  "message": "Validation failed",
  "data": null,
  "errors": [
    "nama: Nama harus antara 2-50 karakter",
    "gaji: Gaji harus berupa angka yang valid"
  ]
}
```

## 🧪 Testing

Run the validation tests:
```powershell
.\test_validation.ps1
```

## 🛠️ Dependencies

- **axum**: Modern web framework
- **tokio**: Async runtime
- **serde**: Serialization/deserialization
- **validator**: Data validation
- **sea-orm**: ORM for database operations

## 🎯 Architecture Benefits

- **Separation of Concerns**: Models, handlers, and validators in separate modules
- **Reusability**: Validation functions used across multiple handlers
- **Maintainability**: Clean, organized code structure
- **Testability**: Each module can be tested independently
- **Scalability**: Easy to add new features and endpoints