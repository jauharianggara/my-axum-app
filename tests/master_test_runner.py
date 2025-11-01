#!/usr/bin/env python3
"""
Master Test Runner for Axum API
===============================

This script orchestrates all test suites:
- Security Testing
- Authentication & Authorization Testing  
- Functional Testing (Photo uploads, etc.)
- Performance Testing

Usage:
    python master_test_runner.py                    # Run all tests
    python master_test_runner.py --suites security  # Run specific suite
    python master_test_runner.py --verbose          # Verbose output
    python master_test_runner.py --list             # List available suites
"""

import subprocess
import sys
import time
import requests
import os
import argparse
from pathlib import Path

class MasterTestRunner:
    def __init__(self, base_url="http://localhost:8080", verbose=False):
        self.base_url = base_url
        self.verbose = verbose
        self.test_dir = Path(__file__).parent
        self.results = {}
        
        # Available test suites
        self.available_suites = {
            'security': {
                'script': 'security_tests.py',
                'description': 'Security vulnerability testing (CORS, CSRF, XSS, SQL injection)',
                'priority': 1
            },
            'auth': {
                'script': 'auth_tests.py', 
                'description': 'Authentication and authorization testing',
                'priority': 2
            },
            'functional': {
                'script': 'comprehensive_photo_tests.py',
                'description': 'Functional testing (Photo uploads, API endpoints)',
                'priority': 3
            },
            'performance': {
                'script': 'performance_photo_tests.py',
                'description': 'Performance and load testing',
                'priority': 4
            }
        }
    
    def check_dependencies(self):
        """Check if required dependencies are available"""
        print("🔍 Checking Dependencies...")
        
        # Check Python packages
        required_packages = ['requests', 'PIL']
        missing_packages = []
        
        for package in required_packages:
            try:
                if package == 'PIL':
                    import PIL
                else:
                    __import__(package)
                print(f"✅ {package} - Available")
            except ImportError:
                print(f"❌ {package} - Missing")
                missing_packages.append(package)
        
        if missing_packages:
            print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
            print("Install with: pip install requests pillow")
            return False
        
        # Check if test scripts exist
        missing_scripts = []
        for suite_name, suite_info in self.available_suites.items():
            script_path = self.test_dir / suite_info['script']
            if script_path.exists():
                print(f"✅ {suite_info['script']} - Found")
            else:
                print(f"❌ {suite_info['script']} - Missing")
                missing_scripts.append(suite_info['script'])
        
        if missing_scripts:
            print(f"\n❌ Missing test scripts: {', '.join(missing_scripts)}")
            return False
        
        return True
    
    def check_server_health(self):
        """Check if the API server is running and healthy"""
        print("🏥 Checking Server Health...")
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                print(f"✅ Server is running at {self.base_url}")
                return True
            else:
                print(f"❌ Server health check failed: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to server at {self.base_url}")
            print("   Make sure the server is running: cargo run")
            return False
        except requests.exceptions.Timeout:
            print(f"❌ Server health check timed out")
            return False
        except Exception as e:
            print(f"❌ Server health check failed: {e}")
            return False
    
    def run_test_suite(self, suite_name):
        """Run a specific test suite"""
        if suite_name not in self.available_suites:
            print(f"❌ Unknown test suite: {suite_name}")
            return False
        
        suite_info = self.available_suites[suite_name]
        script_path = self.test_dir / suite_info['script']
        
        print(f"\n🧪 Running {suite_name.upper()} Tests...")
        print(f"📝 {suite_info['description']}")
        print("─" * 60)
        
        start_time = time.time()
        
        try:
            # Build command
            cmd = [sys.executable, str(script_path), '--url', self.base_url]
            if self.verbose:
                cmd.append('--verbose')
            
            # Run the test script
            result = subprocess.run(
                cmd,
                capture_output=not self.verbose,
                text=True,
                cwd=self.test_dir
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Store results
            self.results[suite_name] = {
                'success': result.returncode == 0,
                'duration': duration,
                'output': result.stdout if not self.verbose else '',
                'errors': result.stderr if not self.verbose else ''
            }
            
            if result.returncode == 0:
                print(f"✅ {suite_name.upper()} tests completed successfully ({duration:.1f}s)")
                return True
            else:
                print(f"❌ {suite_name.upper()} tests failed ({duration:.1f}s)")
                if not self.verbose and result.stderr:
                    print(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to run {suite_name} tests: {e}")
            self.results[suite_name] = {
                'success': False,
                'duration': 0,
                'output': '',
                'errors': str(e)
            }
            return False
    
    def run_all_suites(self, selected_suites=None):
        """Run all or selected test suites"""
        if selected_suites is None:
            suites_to_run = list(self.available_suites.keys())
        else:
            suites_to_run = selected_suites
        
        # Sort by priority
        suites_to_run.sort(key=lambda x: self.available_suites[x]['priority'])
        
        print(f"\n🚀 Running Test Suites: {', '.join(suites_to_run)}")
        print("=" * 80)
        
        total_start_time = time.time()
        successful_suites = 0
        
        for suite_name in suites_to_run:
            if self.run_test_suite(suite_name):
                successful_suites += 1
            
            # Small delay between suites
            if suite_name != suites_to_run[-1]:
                time.sleep(1)
        
        total_duration = time.time() - total_start_time
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 Test Suite Summary")
        print("=" * 80)
        
        print(f"Total Suites: {len(suites_to_run)}")
        print(f"✅ Successful: {successful_suites}")
        print(f"❌ Failed: {len(suites_to_run) - successful_suites}")
        print(f"⏱️  Total Duration: {total_duration:.1f}s")
        print(f"📈 Success Rate: {(successful_suites/len(suites_to_run))*100:.1f}%")
        
        # Detailed results
        print("\n📋 Detailed Results:")
        for suite_name in suites_to_run:
            if suite_name in self.results:
                result = self.results[suite_name]
                status = "✅ PASS" if result['success'] else "❌ FAIL"
                duration = result['duration']
                print(f"  {status} {suite_name.upper():<12} ({duration:.1f}s)")
                
                if not result['success'] and result['errors']:
                    print(f"       Error: {result['errors']}")
        
        # Overall assessment
        print("\n🎯 Overall Assessment:")
        if successful_suites == len(suites_to_run):
            print("🟢 EXCELLENT: All test suites passed! API is ready for production.")
        elif successful_suites >= len(suites_to_run) * 0.8:
            print("🟡 GOOD: Most tests passed. Review failed tests before deployment.")
        elif successful_suites >= len(suites_to_run) * 0.5:
            print("🟠 WARNING: Several test suites failed. Significant issues need attention.")
        else:
            print("🔴 CRITICAL: Major test failures detected. API not ready for production.")
        
        return successful_suites == len(suites_to_run)
    
    def list_available_suites(self):
        """List all available test suites"""
        print("\n📋 Available Test Suites:")
        print("=" * 60)
        
        for suite_name, suite_info in self.available_suites.items():
            script_exists = (self.test_dir / suite_info['script']).exists()
            status = "✅" if script_exists else "❌"
            print(f"{status} {suite_name.upper():<12} - {suite_info['description']}")
            print(f"   Script: {suite_info['script']}")
            print(f"   Priority: {suite_info['priority']}")
            print()
    
    def start_server(self):
        """Start the Axum server if not running"""
        print("🚀 Attempting to start server...")
        
        # Check if server is already running
        if self.check_server_health():
            print("✅ Server is already running")
            return True
        
        # Try to start server
        try:
            # Change to project root directory
            project_root = self.test_dir.parent
            
            print("Starting server with 'cargo run'...")
            # Start server in background
            process = subprocess.Popen(
                ['cargo', 'run'],
                cwd=project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start (max 30 seconds)
            for attempt in range(30):
                time.sleep(1)
                if self.check_server_health():
                    print(f"✅ Server started successfully (attempt {attempt + 1})")
                    return True
                print(f"⏳ Waiting for server to start... ({attempt + 1}/30)")
            
            print("❌ Server failed to start within 30 seconds")
            process.terminate()
            return False
            
        except FileNotFoundError:
            print("❌ 'cargo' command not found. Make sure Rust is installed.")
            return False
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Master Test Runner for Axum API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python master_test_runner.py                    # Run all tests
    python master_test_runner.py --suites security auth  # Run specific suites
    python master_test_runner.py --list             # List available suites
    python master_test_runner.py --start-server     # Auto-start server
    python master_test_runner.py --verbose          # Verbose output
        """
    )
    
    parser.add_argument('--url', default='http://localhost:8080', help='Base URL of the API')
    parser.add_argument('--suites', nargs='+', help='Specific test suites to run')
    parser.add_argument('--list', action='store_true', help='List available test suites')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--start-server', action='store_true', help='Attempt to start server if not running')
    parser.add_argument('--skip-deps', action='store_true', help='Skip dependency checks')
    
    args = parser.parse_args()
    
    # Initialize test runner
    runner = MasterTestRunner(args.url, args.verbose)
    
    # Handle list command
    if args.list:
        runner.list_available_suites()
        return
    
    print("🧪 Axum API - Master Test Runner")
    print("=" * 60)
    print(f"🌐 Target URL: {args.url}")
    if args.suites:
        print(f"📋 Selected Suites: {', '.join(args.suites)}")
    print()
    
    # Check dependencies
    if not args.skip_deps:
        if not runner.check_dependencies():
            print("\n❌ Dependency check failed. Fix issues and try again.")
            sys.exit(1)
        print()
    
    # Start server if requested
    if args.start_server:
        if not runner.start_server():
            print("\n❌ Failed to start server. Please start manually with 'cargo run'")
            sys.exit(1)
        print()
    
    # Check server health
    if not runner.check_server_health():
        print("\n❌ Server health check failed.")
        if not args.start_server:
            print("   Try using --start-server flag or start manually with 'cargo run'")
        sys.exit(1)
    print()
    
    # Validate selected suites
    if args.suites:
        invalid_suites = [s for s in args.suites if s not in runner.available_suites]
        if invalid_suites:
            print(f"❌ Invalid test suites: {', '.join(invalid_suites)}")
            print("Use --list to see available suites")
            sys.exit(1)
    
    # Run tests
    success = runner.run_all_suites(args.suites)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()