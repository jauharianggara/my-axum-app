# Project Organization Guide

## Directory Structure

This document describes the organized structure of the My Axum App project after cleanup and reorganization.

### Root Directory
```
my-axum-app/
├── src/                     # Main application source code
├── migration/               # Database migration files
├── tests/                   # Organized test framework
├── docs/                    # Documentation and guides
├── scripts/                 # Automation scripts
├── legacy-tests/           # Old/legacy test files
├── uploads/                # File upload storage
├── target/                 # Rust build artifacts
└── [config files]          # Cargo.toml, docker-compose.yml, etc.
```

### Detailed Structure

#### `src/` - Application Source Code
- `main.rs` - Application entry point
- `database.rs` - Database connection and configuration
- `handlers/` - HTTP request handlers (health, kantor, karyawan)
- `models/` - Data models and structures
- `routes/` - Route definitions and middleware
- `services/` - Business logic services (file upload, etc.)
- `validators/` - Data validation functions

#### `tests/` - Organized Test Framework
- `api/` - API endpoint tests
  - `basic_api_test.py` - Basic API functionality
  - `kantor_crud_test.py` - Kantor CRUD operations
  - `karyawan_crud_test.py` - Karyawan CRUD operations
- `photo/` - Photo upload functionality tests
  - `photo_upload_test.py` - Photo upload validation
  - `photo_validation_test.py` - Photo format validation
  - `photo_security_test.py` - Security validation
  - `photo_performance_test.py` - Performance testing
- `html/` - Interactive test forms
  - `test_photo_form.html` - Manual photo upload testing
- `scripts/` - Test automation scripts
  - `quick_test.ps1` - Quick test runner
  - `simple_test.ps1` - Simple API tests
- `utils/` - Test utilities and helpers
  - `test_utils.py` - Common test functions

#### `docs/` - Documentation
- `summaries/` - Project documentation summaries
  - `20251029_IMPLEMENTATION_SUMMARY.md` - Overall implementation details
  - `20251029_KANTOR_VALIDATION_SUMMARY.md` - Kantor validation features
  - `20251029_KANTOR_REQUIRED_SUMMARY.md` - Mandatory kantor requirements
  - `20251029_TEST_ORGANIZATION_SUMMARY.md` - Test organization details
  - `20251029_FOTO_FEATURE_DOCUMENTATION.md` - Photo feature documentation
- `test-results/` - Test execution results
  - `api_test_results.md` - API test results
  - `FINAL_TEST_RESULTS.md` - Final test outcomes
- `DATABASE_SETUP.md` - Database setup instructions
- `DOCKER_README.md` - Docker configuration guide
- `SCHEMATHESIS_GUIDE.md` - API testing with Schemathesis
- `TESTING_GUIDE.md` - General testing guidelines

#### `scripts/` - Automation Scripts
- `debug_route.ps1` - Debug route functionality
- `docker_with_schemathesis.ps1` - Docker + Schemathesis automation
- `docker_with_schemathesis.sh` - Linux/Mac version
- `run_schemathesis_tests.ps1` - Schemathesis test runner
- `setup_database.ps1` - Database initialization
- `validate-docker.sh` - Docker validation script

#### `legacy-tests/` - Legacy Test Files
Contains older test files that have been superseded by the organized test framework:
- `comprehensive_api_test.py` - Old comprehensive test
- `run_tests.py` - Old test runner
- `schemathesis_test.py` - Old Schemathesis test
- `test_kantor_required.py` - Legacy kantor validation
- `test_kantor_validation.py` - Legacy validation test
- `test_photo_upload.py` - Legacy photo upload test

## Organization Benefits

### Before Cleanup
- Scattered test files in root directory
- Mixed documentation and code files
- Unclear project structure
- Difficult navigation and maintenance

### After Organization
- ✅ Clean separation of concerns
- ✅ Logical grouping of related files
- ✅ Easy navigation and discovery
- ✅ Professional project structure
- ✅ Clear documentation hierarchy
- ✅ Preserved legacy files for reference

## Navigation Guide

### For Developers
- Start with `README.md` for project overview
- Check `src/` for application code
- Use `tests/` for current testing framework
- Refer to `docs/` for detailed documentation

### For Testing
- Use `tests/scripts/quick_test.ps1` for rapid testing
- Check `tests/api/` for specific API tests
- Use `tests/html/test_photo_form.html` for manual testing
- Review `docs/test-results/` for test outcomes

### For Documentation
- Project summaries in `docs/summaries/`
- Setup guides in `docs/`
- Test documentation in `docs/TESTING_GUIDE.md`
- Legacy information preserved in `legacy-tests/`

## Maintenance

This organization should be maintained by:
1. Adding new tests to appropriate `tests/` subdirectories
2. Placing documentation in `docs/` with proper categorization
3. Using `scripts/` for automation tasks
4. Keeping root directory clean of scattered files
5. Updating this guide when structure changes

## File Location Quick Reference

| File Type | Location | Purpose |
|-----------|----------|---------|
| Source Code | `src/` | Application implementation |
| Current Tests | `tests/` | Active test framework |
| Documentation | `docs/` | Guides and summaries |
| Scripts | `scripts/` | Automation tools |
| Legacy Tests | `legacy-tests/` | Historical reference |
| Config Files | Root | Project configuration |
| Build Output | `target/` | Rust compilation artifacts |
| Uploads | `uploads/` | File storage |