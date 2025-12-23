"""
Comprehensive endpoint testing for Alternate Earth Futures Simulator Backend
Tests all production endpoints before frontend integration
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test_header(test_name: str):
    print(f"\n{'=' * 70}")
    print(f"{Colors.BLUE}{test_name}{Colors.END}")
    print('=' * 70)

def print_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_error(message: str):
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_info(message: str):
    print(f"{Colors.YELLOW}ℹ{Colors.END} {message}")

# ============================================================================
# TEST 1: Health Check
# ============================================================================

def test_health():
    print_test_header("TEST 1: Health Check Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Status Code: {response.status_code}")
            print_success(f"Response: {json.dumps(data, indent=2)}")
            
            # Verify response structure
            if "status" in data and data["status"] == "healthy":
                print_success("Server is healthy")
                return True
            else:
                print_error("Unexpected response structure")
                return False
        else:
            print_error(f"Status Code: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Connection failed: {e}")
        return False

# ============================================================================
# TEST 2: Regions Endpoint
# ============================================================================

def test_regions():
    print_test_header("TEST 2: Available Regions Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/regions", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Status Code: {response.status_code}")
            
            regions = data.get("regions", [])
            print_success(f"Found {len(regions)} regions:")
            
            for region in regions:
                region_id = region.get("id", "unknown")
                name = region.get("name", "unknown")
                bbox = region.get("bbox", [])
                print(f"  • {region_id}: {name} (bbox: {bbox})")
            
            # Verify expected regions exist
            region_ids = [r.get("id") for r in regions]
            expected = ["tamilnadu", "karnataka", "kerala", "india", "test"]
            
            for exp in expected:
                if exp in region_ids:
                    print_success(f"Region '{exp}' found")
                else:
                    print_error(f"Region '{exp}' missing")
            
            return len(regions) >= 5
        else:
            print_error(f"Status Code: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {e}")
        return False

# ============================================================================
# TEST 3: Simulate Endpoint - Valid Request
# ============================================================================

def test_simulate_valid():
    print_test_header("TEST 3: Simulate Endpoint - Valid Request")
    
    payload = {
        "region": "test",
        "year": 2035,
        "rainfall_delta": -15,
        "temperature_delta": 1.2,
        "urban_growth": 30
    }
    
    print_info(f"Request payload:\n{json.dumps(payload, indent=2)}")
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/simulate", json=payload, timeout=30)
        elapsed = time.time() - start_time
        
        print_info(f"Response time: {elapsed:.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Status Code: {response.status_code}")
            
            # Verify response structure
            required_fields = ["scenario_id", "metadata", "results", "stats"]
            for field in required_fields:
                if field in data:
                    print_success(f"Field '{field}' present")
                else:
                    print_error(f"Field '{field}' missing")
                    return False
            
            # Show key results
            scenario_id = data.get("scenario_id", "N/A")
            print_info(f"Scenario ID: {scenario_id}")
            
            metadata = data.get("metadata", {})
            print_info(f"Region: {metadata.get('region')}")
            print_info(f"Year: {metadata.get('year')}")
            print_info(f"Generated at: {metadata.get('generated_at')}")
            
            results = data.get("results", {})
            stress = results.get("climate_stress", {})
            print_info(f"Climate stress index: {stress.get('combined_stress_index', 'N/A')}")
            
            transitions = results.get("land_transitions", {})
            print_info(f"Degraded area: {transitions.get('degraded_area_km2', 0):.2f} km²")
            print_info(f"Urbanized area: {transitions.get('urbanized_area_km2', 0):.2f} km²")
            
            stats = data.get("stats", {})
            print_info(f"Cached: {stats.get('cached', False)}")
            print_info(f"Computation time: {stats.get('computation_time_seconds', 0):.2f}s")
            
            return True
        else:
            print_error(f"Status Code: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error: {e}")
        return False

# ============================================================================
# TEST 4: Simulate Endpoint - Invalid Requests (Validation)
# ============================================================================

def test_simulate_validation():
    print_test_header("TEST 4: Simulate Endpoint - Validation Tests")
    
    invalid_payloads = [
        {
            "name": "Invalid region",
            "payload": {"region": "invalid_region", "year": 2035, "rainfall_delta": -15, "temperature_delta": 1.2, "urban_growth": 30},
            "expected_error": "region"
        },
        {
            "name": "Year too low",
            "payload": {"region": "test", "year": 2020, "rainfall_delta": -15, "temperature_delta": 1.2, "urban_growth": 30},
            "expected_error": "year"
        },
        {
            "name": "Year too high",
            "payload": {"region": "test", "year": 2150, "rainfall_delta": -15, "temperature_delta": 1.2, "urban_growth": 30},
            "expected_error": "year"
        },
        {
            "name": "Rainfall delta too low",
            "payload": {"region": "test", "year": 2035, "rainfall_delta": -100, "temperature_delta": 1.2, "urban_growth": 30},
            "expected_error": "rainfall"
        },
        {
            "name": "Temperature delta too high",
            "payload": {"region": "test", "year": 2035, "rainfall_delta": -15, "temperature_delta": 10, "urban_growth": 30},
            "expected_error": "temperature"
        },
        {
            "name": "Urban growth negative",
            "payload": {"region": "test", "year": 2035, "rainfall_delta": -15, "temperature_delta": 1.2, "urban_growth": -10},
            "expected_error": "urban"
        },
    ]
    
    passed = 0
    failed = 0
    
    for test_case in invalid_payloads:
        print(f"\n  Testing: {test_case['name']}")
        
        try:
            response = requests.post(f"{BASE_URL}/simulate", json=test_case["payload"], timeout=10)
            
            if response.status_code == 422:  # Validation error expected
                print_success(f"Correctly rejected with 422")
                passed += 1
            elif response.status_code == 400:  # Also acceptable
                print_success(f"Correctly rejected with 400")
                passed += 1
            else:
                print_error(f"Expected validation error, got {response.status_code}")
                failed += 1
                
        except Exception as e:
            print_error(f"Error: {e}")
            failed += 1
    
    print(f"\n  Validation tests: {passed} passed, {failed} failed")
    return failed == 0

# ============================================================================
# TEST 5: Determinism & Caching
# ============================================================================

def test_determinism_and_caching():
    print_test_header("TEST 5: Determinism & Caching")
    
    # Clear cache first
    print_info("Clearing cache...")
    try:
        requests.post(f"{BASE_URL}/cache/clear", timeout=5)
        print_success("Cache cleared")
    except:
        print_error("Failed to clear cache")
        return False
    
    # Test payload
    payload = {
        "region": "test",
        "year": 2040,
        "rainfall_delta": -20,
        "temperature_delta": 2.0,
        "urban_growth": 50
    }
    
    print_info("Making first request (should compute)...")
    try:
        start1 = time.time()
        response1 = requests.post(f"{BASE_URL}/simulate", json=payload, timeout=30)
        time1 = time.time() - start1
        
        if response1.status_code != 200:
            print_error(f"First request failed: {response1.status_code}")
            return False
        
        data1 = response1.json()
        scenario_id_1 = data1.get("scenario_id")
        cached_1 = data1.get("stats", {}).get("cached", False)
        
        print_success(f"First request: scenario_id={scenario_id_1}")
        print_info(f"Time: {time1:.2f}s, Cached: {cached_1}")
        
        # Second identical request
        print_info("Making second identical request (should be cached)...")
        start2 = time.time()
        response2 = requests.post(f"{BASE_URL}/simulate", json=payload, timeout=30)
        time2 = time.time() - start2
        
        if response2.status_code != 200:
            print_error(f"Second request failed: {response2.status_code}")
            return False
        
        data2 = response2.json()
        scenario_id_2 = data2.get("scenario_id")
        cached_2 = data2.get("stats", {}).get("cached", False)
        
        print_success(f"Second request: scenario_id={scenario_id_2}")
        print_info(f"Time: {time2:.2f}s, Cached: {cached_2}")
        
        # Verify determinism
        if scenario_id_1 == scenario_id_2:
            print_success("✓ DETERMINISM VERIFIED: Same inputs produce same scenario_id")
        else:
            print_error("✗ DETERMINISM FAILED: Different scenario_ids produced")
            return False
        
        # Verify caching
        if not cached_1 and cached_2:
            print_success("✓ CACHING WORKING: First computed, second cached")
            
            if time2 < time1:
                print_success(f"✓ CACHE SPEEDUP: {time1/time2:.1f}x faster")
        else:
            print_error(f"✗ CACHING ISSUE: cached_1={cached_1}, cached_2={cached_2}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Error: {e}")
        return False

# ============================================================================
# TEST 6: Cache Stats & Clear
# ============================================================================

def test_cache_management():
    print_test_header("TEST 6: Cache Management")
    
    # Get cache stats
    print_info("Checking cache stats...")
    try:
        response = requests.get(f"{BASE_URL}/cache/stats", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Cache stats retrieved:")
            print(f"  • Entries: {data.get('entries', 0)}")
            print(f"  • Max size: {data.get('max_size', 0)}")
            print(f"  • TTL: {data.get('ttl_hours', 0)} hours")
            
            scenarios = data.get("scenarios", [])
            if scenarios:
                print_info(f"Cached scenarios: {len(scenarios)}")
                for scenario in scenarios[:3]:  # Show first 3
                    print(f"    - {scenario.get('scenario_id', 'N/A')}")
        else:
            print_error(f"Failed to get cache stats: {response.status_code}")
            return False
        
        # Clear cache
        print_info("Clearing cache...")
        response = requests.post(f"{BASE_URL}/cache/clear", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Cache cleared: {data.get('message', 'N/A')}")
            print_info(f"Cleared {data.get('cleared_count', 0)} entries")
        else:
            print_error(f"Failed to clear cache: {response.status_code}")
            return False
        
        # Verify cache is empty
        response = requests.get(f"{BASE_URL}/cache/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            entries = data.get('entries', -1)
            if entries == 0:
                print_success("Cache successfully cleared")
                return True
            else:
                print_error(f"Cache still has {entries} entries")
                return False
        
    except Exception as e:
        print_error(f"Error: {e}")
        return False

# ============================================================================
# TEST 7: Load Test (Light)
# ============================================================================

def test_light_load():
    print_test_header("TEST 7: Light Load Test (5 concurrent scenarios)")
    
    payloads = [
        {"region": "test", "year": 2030, "rainfall_delta": -10, "temperature_delta": 1.0, "urban_growth": 20},
        {"region": "test", "year": 2035, "rainfall_delta": -15, "temperature_delta": 1.5, "urban_growth": 30},
        {"region": "test", "year": 2040, "rainfall_delta": -20, "temperature_delta": 2.0, "urban_growth": 40},
        {"region": "test", "year": 2050, "rainfall_delta": -25, "temperature_delta": 2.5, "urban_growth": 50},
        {"region": "test", "year": 2060, "rainfall_delta": 5, "temperature_delta": 0.5, "urban_growth": 25},
    ]
    
    print_info("Clearing cache first...")
    requests.post(f"{BASE_URL}/cache/clear")
    
    print_info(f"Sending {len(payloads)} simulation requests...")
    
    results = []
    for i, payload in enumerate(payloads, 1):
        try:
            start = time.time()
            response = requests.post(f"{BASE_URL}/simulate", json=payload, timeout=30)
            elapsed = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                scenario_id = data.get("scenario_id", "N/A")
                print_success(f"Request {i}: {scenario_id} ({elapsed:.2f}s)")
                results.append(True)
            else:
                print_error(f"Request {i} failed: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print_error(f"Request {i} error: {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print_info(f"Results: {passed}/{total} requests successful")
    
    return passed == total

# ============================================================================
# TEST 8: API Documentation
# ============================================================================

def test_documentation():
    print_test_header("TEST 8: API Documentation Endpoints")
    
    try:
        # Test /docs (Swagger UI)
        print_info("Checking /docs (Swagger UI)...")
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print_success("/docs is accessible")
        else:
            print_error(f"/docs returned {response.status_code}")
            return False
        
        # Test /openapi.json
        print_info("Checking /openapi.json...")
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
        if response.status_code == 200:
            openapi_spec = response.json()
            print_success(f"/openapi.json is accessible")
            print_info(f"API Title: {openapi_spec.get('info', {}).get('title', 'N/A')}")
            print_info(f"API Version: {openapi_spec.get('info', {}).get('version', 'N/A')}")
            
            paths = openapi_spec.get('paths', {})
            print_info(f"Documented endpoints: {len(paths)}")
            
            return True
        else:
            print_error(f"/openapi.json returned {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {e}")
        return False

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    print("\n" + "=" * 70)
    print(f"{Colors.BLUE}ALTERNATE EARTH FUTURES SIMULATOR - ENDPOINT TESTING{Colors.END}")
    print(f"{Colors.BLUE}Testing all endpoints before frontend integration{Colors.END}")
    print("=" * 70)
    
    # Check server availability first
    print_info(f"Target server: {BASE_URL}")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print_success("Server is reachable")
    except:
        print_error(f"Cannot connect to server at {BASE_URL}")
        print_info("Please start the server first: python run.py")
        return
    
    # Run all tests
    tests = [
        ("Health Check", test_health),
        ("Regions List", test_regions),
        ("Valid Simulation", test_simulate_valid),
        ("Validation Tests", test_simulate_validation),
        ("Determinism & Caching", test_determinism_and_caching),
        ("Cache Management", test_cache_management),
        ("Light Load Test", test_light_load),
        ("API Documentation", test_documentation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
        
        time.sleep(0.5)  # Small delay between tests
    
    # Final summary
    print("\n" + "=" * 70)
    print(f"{Colors.BLUE}TEST SUMMARY{Colors.END}")
    print("=" * 70)
    
    for test_name, passed in results:
        status = f"{Colors.GREEN}✓ PASSED{Colors.END}" if passed else f"{Colors.RED}✗ FAILED{Colors.END}"
        print(f"{status} - {test_name}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print("\n" + "=" * 70)
    if passed_count == total_count:
        print(f"{Colors.GREEN}🎉 ALL TESTS PASSED ({passed_count}/{total_count}){Colors.END}")
        print(f"{Colors.GREEN}Backend is ready for frontend integration!{Colors.END}")
    else:
        print(f"{Colors.YELLOW}⚠️  {passed_count}/{total_count} TESTS PASSED{Colors.END}")
        print(f"{Colors.YELLOW}Review failed tests above before proceeding to frontend{Colors.END}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
