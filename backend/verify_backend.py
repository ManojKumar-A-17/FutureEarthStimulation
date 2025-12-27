"""
Quick Backend Verification Test
Run this after starting the backend server to verify everything works
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

def test_regions():
    """Test regions endpoint"""
    print("\n🌍 Testing /regions endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/regions", timeout=5)
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Region count: {data.get('count')}")
        print(f"   Sample regions: {[r['name'] for r in data['regions'][:5]]}")
        return response.status_code == 200 and data.get('count', 0) > 50
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

def test_simulate():
    """Test simulation endpoint with test region"""
    print("\n🧪 Testing /simulate endpoint...")
    try:
        payload = {
            "region": "test",
            "year": 2035,
            "rainfall_delta": -15.0,
            "temperature_delta": 1.2,
            "urban_growth": 30.0
        }
        response = requests.post(
            f"{BASE_URL}/simulate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Scenario ID: {data.get('scenario_id')}")
            print(f"   Data source: {data.get('data_source')}")
            print(f"   Stress level: {data.get('stats', {}).get('overall_stress_level')}")
            print(f"   Computation time: {data.get('stats', {}).get('computation_time_seconds')}s")
            return True
        else:
            print(f"   ❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

def test_cors():
    """Test CORS headers"""
    print("\n🔒 Testing CORS headers...")
    try:
        response = requests.options(
            f"{BASE_URL}/simulate",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST"
            },
            timeout=5
        )
        cors_origin = response.headers.get('access-control-allow-origin')
        cors_methods = response.headers.get('access-control-allow-methods')
        
        print(f"   Status: {response.status_code}")
        print(f"   Allow-Origin: {cors_origin}")
        print(f"   Allow-Methods: {cors_methods}")
        
        return cors_origin is not None
    except Exception as e:
        print(f"   ⚠️  Warning: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 Backend Verification Test")
    print("=" * 60)
    print("\nMake sure the backend server is running:")
    print("  cd backend && python run.py")
    print("\nStarting tests...\n")
    
    results = {
        "Health Check": test_health(),
        "Regions API": test_regions(),
        "Simulation": test_simulate(),
        "CORS": test_cors()
    }
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Backend is ready for frontend connection.")
        print("\nNext steps:")
        print("  1. cd ../frontend")
        print("  2. npm run dev  (or bun run dev)")
        print("  3. Open http://localhost:5173")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("  - Make sure backend server is running")
        print("  - Check if port 8000 is accessible")
        print("  - Verify .env file has correct configuration")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
