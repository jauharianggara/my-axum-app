#!/usr/bin/env python3
"""
Master Test Runner for Karyawan Photo Upload API
Orchestrates all testing suites: functional, performance, and security
"""

import sys
import os
import subprocess
import time
import requests
import json
from datetime import datetime
import argparse

# Test suite configurations
TEST_SUITES = {
    'functional': {
        'script': 'comprehensive_photo_tests.py',
        'description': '🧪 Functional Testing Suite',
        'duration': 'Medium (~2-5 minutes)',
        'priority': 1
    },
    'performance': {
        'script': 'performance_photo_tests.py', 
        'description': '🚀 Performance Testing Suite',
        'duration': 'Long (~5-10 minutes)',
        'priority': 2
    },
    'security': {
        'script': 'security_photo_tests.py',
        'description': '🛡️  Security Testing Suite', 
        'duration': 'Medium (~3-7 minutes)',
        'priority': 3
    }
}

BASE_URL = "http://localhost:8080"
API_BASE = f"{BASE_URL}/api"

class TestOrchestrator:
    """Main test orchestrator class"""
    
    def __init__(self):
        self.results = {}
        self.start_time = None
        self.end_time = None
        self.server_process = None
        
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        required_packages = ['requests', 'pillow']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"   ✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"   ❌ {package}")
        
        if missing_packages:
            print(f"\n⚠️  Missing dependencies: {', '.join(missing_packages)}")
            print("Please install them with:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False
        
        print("✅ All dependencies satisfied\n")
        return True
    
    def check_server_status(self):
        """Check if the server is running and responsive"""
        print("🌐 Checking server status...")
        
        try:
            response = requests.get(f"{API_BASE}/karyawans", timeout=5)
            if response.status_code in [200, 401, 403]:  # Server responding
                print(f"✅ Server is running at {BASE_URL}")
                return True
            else:
                print(f"⚠️  Server responding but returned status {response.status_code}")
                return True  # Still responsive
        except requests.exceptions.ConnectionError:
            print(f"❌ Server not running at {BASE_URL}")
            return False
        except requests.exceptions.Timeout:
            print(f"⏱️  Server timeout at {BASE_URL}")
            return False
        except Exception as e:
            print(f"❌ Server check failed: {str(e)}")
            return False
    
    def start_server_if_needed(self):
        """Attempt to start the server if it's not running"""
        if self.check_server_status():
            return True
        
        print("\n🚀 Attempting to start server...")
        
        # Check if Cargo.toml exists
        if not os.path.exists("Cargo.toml"):
            print("❌ Cargo.toml not found. Make sure you're in the project directory.")
            return False
        
        try:
            # Start server in background
            print("   Starting Rust/Axum server...")
            
            if os.name == 'nt':  # Windows
                self.server_process = subprocess.Popen(
                    ["cargo", "run"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:  # Unix-like
                self.server_process = subprocess.Popen(
                    ["cargo", "run"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            # Wait for server to start
            print("   Waiting for server to start...")
            for i in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                if self.check_server_status():
                    print(f"✅ Server started successfully!")
                    time.sleep(2)  # Give it a moment to fully initialize
                    return True
                
                if i % 5 == 4:  # Every 5 seconds
                    print(f"   Still waiting... ({i+1}/30 seconds)")
            
            print("❌ Server failed to start within 30 seconds")
            return False
            
        except FileNotFoundError:
            print("❌ Cargo not found. Make sure Rust is installed.")
            return False
        except Exception as e:
            print(f"❌ Failed to start server: {str(e)}")
            return False
    
    def run_test_suite(self, suite_name: str, verbose: bool = False):
        """Run a specific test suite"""
        if suite_name not in TEST_SUITES:
            print(f"❌ Unknown test suite: {suite_name}")
            return False
        
        suite = TEST_SUITES[suite_name]
        script_path = suite['script']
        
        if not os.path.exists(script_path):
            print(f"❌ Test script not found: {script_path}")
            return False
        
        print(f"\n{'='*80}")
        print(f"{suite['description']}")
        print(f"Duration: {suite['duration']}")
        print(f"{'='*80}")
        
        try:
            start_time = time.time()
            
            # Run the test script
            if verbose:
                result = subprocess.run([sys.executable, script_path], 
                                      capture_output=False, text=True)
            else:
                result = subprocess.run([sys.executable, script_path], 
                                      capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print("STDERR:", result.stderr)
            
            end_time = time.time()
            duration = end_time - start_time
            
            success = result.returncode == 0
            
            self.results[suite_name] = {
                'success': success,
                'duration': duration,
                'returncode': result.returncode
            }
            
            if success:
                print(f"\n✅ {suite['description']} PASSED ({duration:.1f}s)")
            else:
                print(f"\n❌ {suite['description']} FAILED ({duration:.1f}s)")
                print(f"   Return code: {result.returncode}")
            
            return success
            
        except Exception as e:
            print(f"❌ Failed to run {suite_name}: {str(e)}")
            self.results[suite_name] = {
                'success': False,
                'duration': 0,
                'error': str(e)
            }
            return False
    
    def run_all_tests(self, selected_suites: list = None, verbose: bool = False):
        """Run all or selected test suites"""
        self.start_time = datetime.now()
        
        print(f"\n{'='*80}")
        print("🧪 COMPREHENSIVE API TESTING SUITE")
        print(f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        # Determine which suites to run
        if selected_suites:
            suites_to_run = {k: v for k, v in TEST_SUITES.items() if k in selected_suites}
        else:
            suites_to_run = TEST_SUITES
        
        # Sort by priority
        sorted_suites = sorted(suites_to_run.items(), key=lambda x: x[1]['priority'])
        
        print(f"📋 Test Plan:")
        for name, suite in sorted_suites:
            print(f"   {suite['priority']}. {suite['description']} - {suite['duration']}")
        
        success_count = 0
        total_count = len(sorted_suites)
        
        # Run each test suite
        for suite_name, suite_config in sorted_suites:
            success = self.run_test_suite(suite_name, verbose)
            if success:
                success_count += 1
        
        self.end_time = datetime.now()
        total_duration = (self.end_time - self.start_time).total_seconds()
        
        # Print final summary
        self.print_final_summary(success_count, total_count, total_duration)
        
        return success_count == total_count
    
    def print_final_summary(self, success_count: int, total_count: int, duration: float):
        """Print comprehensive test summary"""
        print(f"\n{'='*80}")
        print("📊 FINAL TEST SUMMARY")
        print(f"{'='*80}")
        print(f"Total Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
        print(f"Test Suites:    {success_count}/{total_count} passed")
        print(f"Success Rate:   {(success_count/total_count)*100:.1f}%")
        
        print(f"\n📈 Individual Results:")
        for suite_name, result in self.results.items():
            status = "✅ PASSED" if result['success'] else "❌ FAILED"
            duration = result.get('duration', 0)
            print(f"   {TEST_SUITES[suite_name]['description']}: {status} ({duration:.1f}s)")
            
            if not result['success'] and 'error' in result:
                print(f"      Error: {result['error']}")
        
        # Overall assessment
        if success_count == total_count:
            print(f"\n🏆 ALL TESTS PASSED!")
            print("   Your photo upload API is ready for production!")
        elif success_count >= total_count * 0.8:
            print(f"\n✅ MOSTLY SUCCESSFUL!")
            print("   Most tests passed. Review failed tests before deployment.")
        elif success_count >= total_count * 0.5:
            print(f"\n⚠️  PARTIAL SUCCESS")
            print("   Some critical issues detected. Fix before deployment.")
        else:
            print(f"\n❌ MULTIPLE FAILURES")
            print("   Significant issues detected. Requires investigation.")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if 'functional' in self.results and not self.results['functional']['success']:
            print("   • Fix functional issues before proceeding with other tests")
        if 'security' in self.results and not self.results['security']['success']:
            print("   • Address security vulnerabilities immediately")
        if 'performance' in self.results and not self.results['performance']['success']:
            print("   • Optimize performance for production load")
        
        if success_count == total_count:
            print("   • API is ready for production deployment!")
            print("   • Consider setting up CI/CD with these tests")
            print("   • Monitor performance and security in production")
    
    def cleanup(self):
        """Cleanup resources"""
        if self.server_process:
            print("\n🧹 Stopping test server...")
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                print("✅ Server stopped")
            except:
                try:
                    self.server_process.kill()
                    print("✅ Server killed")
                except:
                    print("⚠️  Could not stop server process")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Comprehensive API Testing Suite')
    parser.add_argument('--suites', nargs='+', choices=list(TEST_SUITES.keys()),
                       help='Specific test suites to run (default: all)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output (show all test details)')
    parser.add_argument('--no-server-start', action='store_true',
                       help='Skip automatic server startup')
    parser.add_argument('--list', action='store_true',
                       help='List available test suites')
    
    args = parser.parse_args()
    
    if args.list:
        print("Available test suites:")
        for name, suite in sorted(TEST_SUITES.items(), key=lambda x: x[1]['priority']):
            print(f"  {name:12} - {suite['description']} ({suite['duration']})")
        return 0
    
    orchestrator = TestOrchestrator()
    
    try:
        # Check dependencies
        if not orchestrator.check_dependencies():
            return 1
        
        # Start server if needed
        if not args.no_server_start:
            if not orchestrator.start_server_if_needed():
                print("\n❌ Cannot proceed without a running server")
                print("   Start the server manually and use --no-server-start flag")
                return 1
        else:
            if not orchestrator.check_server_status():
                print("\n❌ Server is not running")
                print("   Start the server manually or remove --no-server-start flag")
                return 1
        
        # Run tests
        success = orchestrator.run_all_tests(args.suites, args.verbose)
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Testing failed: {str(e)}")
        return 1
    finally:
        orchestrator.cleanup()

if __name__ == "__main__":
    exit(main())