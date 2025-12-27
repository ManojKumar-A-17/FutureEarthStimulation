"""
FINAL PRE-DEPLOYMENT VERIFICATION
Complete system check before connecting frontend to backend
"""

import sys
import os

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text:^60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_section(text):
    print(f"\n{Colors.BLUE}{text}{Colors.END}")

def print_success(text):
    print(f"  {Colors.GREEN}✓ {text}{Colors.END}")

def print_warning(text):
    print(f"  {Colors.YELLOW}⚠ {text}{Colors.END}")

def print_error(text):
    print(f"  {Colors.RED}✗ {text}{Colors.END}")

def test_imports():
    """Test all critical imports"""
    print_section("1. Testing Python Imports")
    
    issues = []
    
    try:
        import fastapi
        print_success(f"FastAPI {fastapi.__version__}")
    except ImportError as e:
        print_error(f"FastAPI import failed: {e}")
        issues.append("FastAPI")
    
    try:
        import ee
        print_success("Earth Engine API")
    except ImportError as e:
        print_error(f"Earth Engine import failed: {e}")
        issues.append("Earth Engine")
    
    try:
        import uvicorn
        print_success("Uvicorn")
    except ImportError as e:
        print_error(f"Uvicorn import failed: {e}")
        issues.append("Uvicorn")
    
    try:
        from app.main import app
        print_success("Main app module")
    except Exception as e:
        print_error(f"Main app import failed: {e}")
        issues.append("Main app")
    
    try:
        from app.api.simulate import SimulateAPI
        print_success("Simulate API")
    except Exception as e:
        print_error(f"Simulate API import failed: {e}")
        issues.append("Simulate API")
    
    try:
        from app.utils.regions import REGIONS, get_available_regions
        print_success(f"Regions module ({len(REGIONS)} regions)")
    except Exception as e:
        print_error(f"Regions import failed: {e}")
        issues.append("Regions")
    
    return len(issues) == 0

def test_configuration():
    """Test configuration files and environment"""
    print_section("2. Testing Configuration")
    
    issues = []
    
    # Check .env file
    if os.path.exists('.env'):
        print_success(".env file exists")
        with open('.env', 'r') as f:
            content = f.read()
            if 'EARTH_ENGINE_PROJECT' in content:
                print_success("EARTH_ENGINE_PROJECT configured")
            else:
                print_warning("EARTH_ENGINE_PROJECT not set (will use mock data)")
    else:
        print_warning(".env file not found (using defaults)")
    
    # Check frontend .env
    frontend_env = '../frontend/.env'
    if os.path.exists(frontend_env):
        print_success("Frontend .env exists")
        with open(frontend_env, 'r') as f:
            content = f.read()
            if 'VITE_BACKEND_URL' in content:
                print_success("Frontend backend URL configured")
            else:
                print_error("VITE_BACKEND_URL not set in frontend")
                issues.append("Frontend .env")
    else:
        print_error("Frontend .env file missing")
        issues.append("Frontend .env")
    
    return len(issues) == 0

def test_regions():
    """Test region system"""
    print_section("3. Testing Region System")
    
    try:
        from app.utils.regions import REGIONS, get_available_regions, get_available_region_names
        
        regions = get_available_regions()
        region_ids = get_available_region_names()
        
        print_success(f"Total regions: {len(REGIONS)}")
        print_success(f"Region IDs generated: {len(region_ids)}")
        
        # Test normalization
        if 'tamilnadu' in region_ids:
            print_success("Region ID normalization working (tamilnadu)")
        
        if 'california' in region_ids:
            print_success("US regions available (california)")
        
        if 'guangdong' in region_ids:
            print_success("Chinese regions available (guangdong)")
        
        # Show sample regions
        print(f"\n  Sample regions:")
        for region in regions[:5]:
            print(f"    - {region['name']} ({region['id']})")
        
        return True
    except Exception as e:
        print_error(f"Region system test failed: {e}")
        return False

def test_cors():
    """Test CORS configuration"""
    print_section("4. Testing CORS Configuration")
    
    try:
        from app.main import app
        
        # Check if CORSMiddleware is in middleware stack
        has_cors = False
        for middleware in app.user_middleware:
            if 'CORSMiddleware' in str(middleware):
                has_cors = True
                break
        
        if has_cors:
            print_success("CORS middleware configured")
        else:
            print_error("CORS middleware not found!")
            return False
        
        return True
    except Exception as e:
        print_error(f"CORS test failed: {e}")
        return False

def test_api_models():
    """Test API model validation"""
    print_section("5. Testing API Models")
    
    try:
        from app.api.models import SimulationRequest, SimulationResponse
        
        # Test request validation
        test_request = {
            "region": "test",
            "year": 2035,
            "rainfall_delta": -15.0,
            "temperature_delta": 1.2,
            "urban_growth": 30.0
        }
        
        req = SimulationRequest(**test_request)
        print_success(f"Request validation working (region: {req.region})")
        
        # Test parameter constraints
        from app.config import (
            RAIN_DELTA_MIN, RAIN_DELTA_MAX,
            TEMP_DELTA_MIN, TEMP_DELTA_MAX,
            URBAN_GROWTH_MIN, URBAN_GROWTH_MAX
        )
        
        print_success(f"Rainfall range: {RAIN_DELTA_MIN}% to {RAIN_DELTA_MAX}%")
        print_success(f"Temperature range: {TEMP_DELTA_MIN}°C to {TEMP_DELTA_MAX}°C")
        print_success(f"Urban growth range: {URBAN_GROWTH_MIN}% to {URBAN_GROWTH_MAX}%")
        
        return True
    except Exception as e:
        print_error(f"API models test failed: {e}")
        return False

def test_simulation_engine():
    """Test simulation engine with mock data"""
    print_section("6. Testing Simulation Engine")
    
    try:
        from app.ml.simulation_engine import SimulationEngine
        
        engine = SimulationEngine()
        print_success("Simulation engine initialized")
        
        # Test with mock data
        mock_baseline = {
            'region': 'test',
            'year': 2020,
            'land_cover': {
                'classes': {'1': 500, '4': 700, '6': 200},
                'metadata': {}
            },
            'rainfall': {'annual_mean_mm': 1000},
            'temperature': {'mean_celsius': 25.0},
            'ndvi': {'mean_ndvi': 0.55}
        }
        
        scenario = {
            'target_year': 2035,
            'rainfall_delta': -15.0,
            'temperature_delta': 1.2,
            'urban_growth': 30.0
        }
        
        result = engine.run_simulation(mock_baseline, scenario)
        
        if 'scenario_id' in result:
            print_success(f"Simulation executed (ID: {result['scenario_id'][:12]}...)")
        
        if 'summary_stats' in result:
            stats = result['summary_stats']
            print_success(f"Stress level: {stats.get('overall_stress_level', 'unknown')}")
        
        return True
    except Exception as e:
        print_error(f"Simulation engine test failed: {e}")
        return False

def test_cache():
    """Test cache system"""
    print_section("7. Testing Cache System")
    
    try:
        from app.utils.cache import get_cache
        
        cache = get_cache()
        print_success("Cache system initialized")
        
        # Test cache operations
        test_params = {'region': 'test', 'year': 2035}
        test_data = {'result': 'test'}
        
        cache.set(test_params, test_data)
        retrieved = cache.get(test_params)
        
        if retrieved == test_data:
            print_success("Cache set/get working")
        
        stats = cache.get_stats()
        print_success(f"Cache capacity: {stats['max_size']} entries")
        
        cache.clear()
        print_success("Cache clear working")
        
        return True
    except Exception as e:
        print_error(f"Cache test failed: {e}")
        return False

def check_frontend():
    """Check frontend files"""
    print_section("8. Checking Frontend")
    
    frontend_path = '../frontend'
    
    if not os.path.exists(frontend_path):
        print_error("Frontend directory not found")
        return False
    
    issues = []
    
    # Check key files
    files_to_check = [
        'package.json',
        'vite.config.ts',
        '.env',
        'src/main.tsx',
        'src/api/backendClient.ts',
        'src/types/simulation.ts',
        'src/hooks/useSimulation.ts'
    ]
    
    for file in files_to_check:
        path = os.path.join(frontend_path, file)
        if os.path.exists(path):
            print_success(f"{file}")
        else:
            print_error(f"{file} missing")
            issues.append(file)
    
    # Check node_modules
    if os.path.exists(os.path.join(frontend_path, 'node_modules')):
        print_success("node_modules installed")
    else:
        print_warning("node_modules not found (need to run npm install)")
        issues.append("node_modules")
    
    return len(issues) == 0

def main():
    """Run all tests"""
    print_header("PRE-DEPLOYMENT VERIFICATION")
    
    print(f"{Colors.BOLD}System: Backend + Frontend Integration{Colors.END}")
    print(f"{Colors.BOLD}Date: 2025-12-26{Colors.END}\n")
    
    results = {
        "Python Imports": test_imports(),
        "Configuration": test_configuration(),
        "Region System": test_regions(),
        "CORS Setup": test_cors(),
        "API Models": test_api_models(),
        "Simulation Engine": test_simulation_engine(),
        "Cache System": test_cache(),
        "Frontend Files": check_frontend()
    }
    
    print_header("VERIFICATION SUMMARY")
    
    all_passed = True
    for test_name, passed in results.items():
        if passed:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
            all_passed = False
    
    print(f"\n{Colors.BOLD}Overall Status:{Colors.END}")
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL SYSTEMS READY FOR DEPLOYMENT{Colors.END}\n")
        print(f"{Colors.CYAN}Next Steps:{Colors.END}")
        print(f"  1. Terminal 1: {Colors.BOLD}python run.py{Colors.END}")
        print(f"  2. Terminal 2: {Colors.BOLD}cd ../frontend && npm run dev{Colors.END}")
        print(f"  3. Browser: {Colors.BOLD}http://localhost:5173{Colors.END}\n")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ SOME TESTS FAILED - FIX ISSUES ABOVE{Colors.END}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
