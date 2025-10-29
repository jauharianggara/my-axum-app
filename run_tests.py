#!/usr/bin/env python3
"""
Main Test Runner for Karyawan API
Centralized testing framework for all API functionality
"""

import sys
import os
import subprocess
import time
import requests
import argparse
from datetime import datetime

# Add tests directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

BASE_URL = "http://localhost:8080"
API_BASE = f"{BASE_URL}/api"

class TestSuiteRunner:
    """Main test suite runner"""
    
    def __init__(self):
        self.results = {}
        self.start_time = None
        self.end_time = None
        
    def check_server(self):
        """Check if server is running"""
        try:
            response = requests.get(f"{API_BASE}/karyawans", timeout=5)
            return response.status_code in [200, 401, 403]
        except:
            return False
    
    def run_test_module(self, module_path: str, description: str):
        """Run a specific test module"""
        print(f"\n{'='*60}")
        print(f"🧪 {description}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            result = subprocess.run([sys.executable, module_path], 
                                  capture_output=True, text=True, timeout=300)
            
            end_time = time.time()
            duration = end_time - start_time
            
            success = result.returncode == 0
            
            if success:
                print(f"✅ PASSED ({duration:.1f}s)")
                if result.stdout:
                    # Show only summary lines
                    lines = result.stdout.split('\n')
                    summary_lines = [line for line in lines if any(keyword in line.lower() 
                                   for keyword in ['pass', 'fail', 'success', 'error', 'summary'])]
                    if summary_lines:
                        print("📊 Summary:")
                        for line in summary_lines[-5:]:  # Last 5 summary lines
                            if line.strip():
                                print(f"   {line}")
            else:
                print(f"❌ FAILED ({duration:.1f}s)")
                if result.stderr:
                    print(f"Error: {result.stderr[:200]}...")
                if result.stdout:
                    print(f"Output: {result.stdout[:200]}...")
            
            self.results[description] = {
                'success': success,
                'duration': duration,
                'returncode': result.returncode
            }
            
            return success
            
        except subprocess.TimeoutExpired:
            print(f"❌ TIMEOUT (>300s)")
            self.results[description] = {'success': False, 'duration': 300, 'error': 'timeout'}
            return False
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            self.results[description] = {'success': False, 'duration': 0, 'error': str(e)}
            return False
    
    def print_final_summary(self):
        """Print final test summary"""
        if not self.results:
            return
            
        total_duration = (self.end_time - self.start_time).total_seconds()
        success_count = sum(1 for r in self.results.values() if r['success'])
        total_count = len(self.results)
        
        print(f"\n{'='*80}")
        print(f"📊 FINAL TEST SUMMARY")
        print(f"{'='*80}")
        print(f"Total Duration: {total_duration:.1f}s")
        print(f"Test Suites: {success_count}/{total_count} passed")
        print(f"Success Rate: {(success_count/total_count)*100:.1f}%")
        
        print(f"\n📈 Individual Results:")
        for name, result in self.results.items():
            status = "✅ PASSED" if result['success'] else "❌ FAILED"
            duration = result.get('duration', 0)
            print(f"   {name}: {status} ({duration:.1f}s)")
        
        if success_count == total_count:
            print(f"\n🏆 ALL TESTS PASSED!")
        elif success_count >= total_count * 0.8:
            print(f"\n✅ MOSTLY SUCCESSFUL!")
        else:
            print(f"\n⚠️  SOME ISSUES DETECTED")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Karyawan API Test Suite')
    parser.add_argument('--suite', choices=['api', 'photo', 'all'], default='all',
                       help='Test suite to run')
    parser.add_argument('--quick', action='store_true',
                       help='Run only essential tests')
    parser.add_argument('--no-server-check', action='store_true',
                       help='Skip server connectivity check')
    
    args = parser.parse_args()
    
    runner = TestSuiteRunner()
    
    print(f"🚀 KARYAWAN API TEST SUITE")
    print(f"{'='*50}")
    
    # Check server
    if not args.no_server_check:
        print("🌐 Checking server connectivity...")
        if not runner.check_server():
            print("❌ Server not available at http://localhost:8080")
            print("   Please start the server first: cargo run")
            return 1
        print("✅ Server is running")
    
    runner.start_time = datetime.now()
    
    try:
        success_count = 0
        total_count = 0
        
        # Define test suites
        test_suites = []
        
        if args.suite in ['api', 'all']:
            test_suites.extend([
                ('tests/api/basic_api_test.py', 'Basic API Functionality'),
                ('tests/api/karyawan_crud_test.py', 'Karyawan CRUD Operations'),
                ('tests/api/kantor_crud_test.py', 'Kantor CRUD Operations'),
            ])
        
        if args.suite in ['photo', 'all']:
            test_suites.extend([
                ('tests/photo/photo_upload_test.py', 'Photo Upload Functionality'),
                ('tests/photo/photo_validation_test.py', 'Photo Validation'),
            ])
            
            if not args.quick:
                test_suites.extend([
                    ('tests/photo/photo_performance_test.py', 'Photo Performance'),
                    ('tests/photo/photo_security_test.py', 'Photo Security'),
                ])
        
        # Run each test suite
        for test_path, description in test_suites:
            if os.path.exists(test_path):
                success = runner.run_test_module(test_path, description)
                if success:
                    success_count += 1
                total_count += 1
            else:
                print(f"⚠️  Test file not found: {test_path}")
        
        runner.end_time = datetime.now()
        runner.print_final_summary()
        
        return 0 if success_count == total_count else 1
        
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Test suite failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())