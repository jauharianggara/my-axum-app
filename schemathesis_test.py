#!/usr/bin/env python3
"""
Schemathesis API Testing for Karyawan & Kantor Management API
Comprehensive property-based testing untuk semua endpoints

Requirements:
    pip install schemathesis requests hypothesis
"""

import schemathesis
import requests
import json
import time
import sys
from typing import Dict, Any
from hypothesis import settings, HealthCheck

# Configuration
API_BASE_URL = "http://localhost:8080"
MAX_EXAMPLES = 50
TIMEOUT_SECONDS = 30

# Custom hooks untuk Schemathesis
class APITestConfig:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.setup_data = {}
        
    def wait_for_api(self, max_attempts: int = 30) -> bool:
        """Wait for API to be ready"""
        print(f"🔄 Waiting for API at {self.base_url}...")
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{self.base_url}/health", timeout=5)
                if response.status_code == 200:
                    print(f"✅ API is ready! (attempt {attempt + 1})")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            print(f"⏳ Attempt {attempt + 1}/{max_attempts} - waiting 2s...")
            time.sleep(2)
        
        print(f"❌ API not ready after {max_attempts} attempts")
        return False
    
    def setup_test_data(self) -> Dict[str, Any]:
        """Setup initial test data"""
        print("🔧 Setting up test data...")
        
        # Create test kantor first (for foreign key)
        kantor_data = {
            "nama": "Kantor Test Schemathesis",
            "alamat": "Jl. Test Schemathesis No.1, Jakarta",
            "longitude": 106.827153,
            "latitude": -6.175110
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/kantors",
                json=kantor_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                kantor_result = response.json()
                if kantor_result.get("success") and kantor_result.get("data"):
                    kantor_id = kantor_result["data"]["id"]
                    self.setup_data["kantor_id"] = kantor_id
                    print(f"✅ Test kantor created with ID: {kantor_id}")
                    return self.setup_data
            
            print(f"⚠️  Failed to create test kantor: {response.status_code}")
            # Try to get existing kantor
            response = requests.get(f"{self.base_url}/api/kantors", timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("data") and len(result["data"]) > 0:
                    kantor_id = result["data"][0]["id"]
                    self.setup_data["kantor_id"] = kantor_id
                    print(f"✅ Using existing kantor with ID: {kantor_id}")
                    return self.setup_data
            
        except Exception as e:
            print(f"❌ Error setting up test data: {e}")
        
        # Fallback - assume kantor with ID 1 exists
        self.setup_data["kantor_id"] = 1
        print("⚠️  Using fallback kantor_id: 1")
        return self.setup_data


# Initialize test config
test_config = APITestConfig()

# Generate OpenAPI schema from running service
def generate_openapi_schema():
    """Generate OpenAPI schema from API endpoints"""
    print("📋 Generating OpenAPI schema...")
    
    schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "Karyawan & Kantor Management API",
            "version": "2.1.0",
            "description": "REST API untuk manajemen data karyawan dan kantor"
        },
        "servers": [
            {"url": API_BASE_URL}
        ],
        "paths": {
            "/": {
                "get": {
                    "summary": "Root endpoint",
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "text/plain": {
                                    "schema": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            },
            "/health": {
                "get": {
                    "summary": "Health check",
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/karyawans": {
                "get": {
                    "summary": "Get all karyawans",
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "message": {"type": "string"},
                                            "data": {
                                                "type": "array",
                                                "items": {"$ref": "#/components/schemas/Karyawan"}
                                            },
                                            "errors": {"type": "null"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": "Create karyawan",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/CreateKaryawan"}
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Success"},
                        "400": {"description": "Validation error"}
                    }
                }
            },
            "/api/karyawans/{id}": {
                "get": {
                    "summary": "Get karyawan by ID",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "string",
                                "pattern": "^[1-9][0-9]*$"
                            }
                        }
                    ],
                    "responses": {
                        "200": {"description": "Success"},
                        "404": {"description": "Not found"},
                        "400": {"description": "Invalid ID"}
                    }
                },
                "put": {
                    "summary": "Update karyawan",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "pattern": "^[1-9][0-9]*$"}
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/CreateKaryawan"}
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Success"},
                        "400": {"description": "Validation error"},
                        "404": {"description": "Not found"}
                    }
                },
                "delete": {
                    "summary": "Delete karyawan",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "pattern": "^[1-9][0-9]*$"}
                        }
                    ],
                    "responses": {
                        "200": {"description": "Success"},
                        "404": {"description": "Not found"},
                        "400": {"description": "Invalid ID"}
                    }
                }
            },
            "/api/kantors": {
                "get": {
                    "summary": "Get all kantors",
                    "responses": {
                        "200": {"description": "Success"}
                    }
                },
                "post": {
                    "summary": "Create kantor",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/CreateKantor"}
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Success"},
                        "400": {"description": "Validation error"}
                    }
                }
            },
            "/api/kantors/{id}": {
                "get": {
                    "summary": "Get kantor by ID",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "pattern": "^[1-9][0-9]*$"}
                        }
                    ],
                    "responses": {
                        "200": {"description": "Success"},
                        "404": {"description": "Not found"},
                        "400": {"description": "Invalid ID"}
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "Karyawan": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "nama": {"type": "string"},
                        "posisi": {"type": "string"},
                        "gaji": {"type": "integer"},
                        "kantor_id": {"type": "integer"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"}
                    }
                },
                "CreateKaryawan": {
                    "type": "object",
                    "required": ["nama", "posisi", "gaji", "kantor_id"],
                    "properties": {
                        "nama": {
                            "type": "string",
                            "minLength": 2,
                            "maxLength": 50,
                            "pattern": "^[a-zA-Z\\s]+$"
                        },
                        "posisi": {
                            "type": "string",
                            "minLength": 2,
                            "maxLength": 30,
                            "pattern": "^[a-zA-Z\\s]+$"
                        },
                        "gaji": {
                            "type": "string",
                            "pattern": "^(1000000|[1-9][0-9]{6,7}|100000000)$"
                        },
                        "kantor_id": {
                            "type": "string",
                            "pattern": "^[1-9][0-9]*$"
                        }
                    }
                },
                "CreateKantor": {
                    "type": "object",
                    "required": ["nama", "alamat", "longitude", "latitude"],
                    "properties": {
                        "nama": {
                            "type": "string",
                            "minLength": 2,
                            "maxLength": 100
                        },
                        "alamat": {
                            "type": "string",
                            "minLength": 5,
                            "maxLength": 200
                        },
                        "longitude": {
                            "type": "number",
                            "minimum": -180,
                            "maximum": 180
                        },
                        "latitude": {
                            "type": "number",
                            "minimum": -90,
                            "maximum": 90
                        }
                    }
                }
            }
        }
    }
    
    return schema


# Custom hooks for better test data
@schemathesis.hook
def before_generate_body(context, strategy):
    """Custom hook untuk generate valid test data"""
    if context.operation.path == "/api/karyawans" and context.operation.method.upper() == "POST":
        # Ensure kantor_id references existing kantor
        if hasattr(test_config, 'setup_data') and 'kantor_id' in test_config.setup_data:
            return strategy.filter(lambda x: x.get('kantor_id') == str(test_config.setup_data['kantor_id']))
    return strategy


def run_schemathesis_tests():
    """Run comprehensive Schemathesis tests"""
    print("\n🧪 Starting Schemathesis API Testing")
    print("=" * 50)
    
    # Wait for API to be ready
    if not test_config.wait_for_api():
        print("❌ API not available - skipping tests")
        return False
    
    # Setup test data
    test_config.setup_test_data()
    
    # Generate schema
    schema = generate_openapi_schema()
    
    # Save schema to file for debugging
    with open("api_schema.json", "w") as f:
        json.dump(schema, f, indent=2)
    print("📋 OpenAPI schema saved to api_schema.json")
    
    # Load schema with Schemathesis
    schema_obj = schemathesis.from_dict(schema)
    
    # Test results
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    print(f"\n🔍 Running property-based tests (max {MAX_EXAMPLES} examples per endpoint)...")
    
    # Configure Hypothesis settings
    settings_obj = settings(
        max_examples=MAX_EXAMPLES,
        deadline=30000,  # 30 seconds
        suppress_health_check=[HealthCheck.too_slow],
        verbosity=1
    )
    
    # Run tests for each endpoint
    for endpoint in schema_obj:
        try:
            print(f"\n📍 Testing {endpoint.method.upper()} {endpoint.path}")
            
            @settings_obj
            @schemathesis.parametrize(schema=schema_obj, endpoint=endpoint)
            def test_endpoint(case):
                # Custom request modifications
                if case.operation.path == "/api/karyawans" and case.operation.method.upper() == "POST":
                    if case.body and isinstance(case.body, dict):
                        # Ensure valid kantor_id
                        if 'kantor_id' in case.body:
                            case.body['kantor_id'] = str(test_config.setup_data.get('kantor_id', 1))
                
                # Execute request
                response = case.call(timeout=TIMEOUT_SECONDS)
                
                # Basic checks
                case.validate_response(response)
                
                # Custom validations
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, dict):
                            # Check API response format
                            if 'success' in data:
                                assert isinstance(data['success'], bool)
                            if 'message' in data:
                                assert isinstance(data['message'], str)
                    except:
                        pass  # Non-JSON responses are OK for some endpoints
                
                return response
            
            # Run the test
            try:
                test_endpoint()
                results["passed"] += 1
                print(f"✅ {endpoint.method.upper()} {endpoint.path} - PASSED")
            except Exception as e:
                results["failed"] += 1
                error_msg = f"{endpoint.method.upper()} {endpoint.path} - FAILED: {str(e)}"
                results["errors"].append(error_msg)
                print(f"❌ {error_msg}")
            
            results["total"] += 1
            
        except Exception as e:
            results["failed"] += 1
            error_msg = f"Setup failed for {endpoint.method.upper()} {endpoint.path}: {str(e)}"
            results["errors"].append(error_msg)
            print(f"💥 {error_msg}")
    
    # Print summary
    print(f"\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Total endpoints: {results['total']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Success rate: {(results['passed']/results['total']*100):.1f}%" if results['total'] > 0 else "0%")
    
    if results['errors']:
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"  - {error}")
    
    success = results['failed'] == 0
    print(f"\n{'✅ All tests passed!' if success else '❌ Some tests failed!'}")
    
    return success


def run_manual_api_tests():
    """Run additional manual API tests"""
    print("\n🔧 Running manual API validation tests...")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Health check
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check - PASSED")
            tests_passed += 1
        else:
            print(f"❌ Health check - FAILED (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Health check - ERROR: {e}")
    
    # Test 2: Root endpoint
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        if response.status_code == 200 and "Hello" in response.text:
            print("✅ Root endpoint - PASSED")
            tests_passed += 1
        else:
            print(f"❌ Root endpoint - FAILED (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Root endpoint - ERROR: {e}")
    
    # Test 3: Get karyawans list
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/karyawans", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and isinstance(data.get("data"), list):
                print("✅ Karyawans list - PASSED")
                tests_passed += 1
            else:
                print(f"❌ Karyawans list - FAILED (invalid response format)")
        else:
            print(f"❌ Karyawans list - FAILED (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Karyawans list - ERROR: {e}")
    
    # Test 4: Get kantors list
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/kantors", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and isinstance(data.get("data"), list):
                print("✅ Kantors list - PASSED")
                tests_passed += 1
            else:
                print(f"❌ Kantors list - FAILED (invalid response format)")
        else:
            print(f"❌ Kantors list - FAILED (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Kantors list - ERROR: {e}")
    
    # Test 5: Invalid ID handling
    tests_total += 1
    try:
        response = requests.get(f"{API_BASE_URL}/api/karyawans/invalid", timeout=10)
        if response.status_code == 400:
            print("✅ Invalid ID handling - PASSED")
            tests_passed += 1
        else:
            print(f"❌ Invalid ID handling - FAILED (expected 400, got {response.status_code})")
    except Exception as e:
        print(f"❌ Invalid ID handling - ERROR: {e}")
    
    print(f"\n📊 Manual Tests: {tests_passed}/{tests_total} passed ({tests_passed/tests_total*100:.1f}%)")
    return tests_passed == tests_total


if __name__ == "__main__":
    print("🧪 Karyawan & Kantor API - Schemathesis Testing Suite")
    print("=" * 60)
    
    # Run manual tests first
    manual_success = run_manual_api_tests()
    
    # Run Schemathesis tests
    schema_success = run_schemathesis_tests()
    
    # Final result
    overall_success = manual_success and schema_success
    
    print(f"\n🏁 Final Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    # Exit with appropriate code
    sys.exit(0 if overall_success else 1)