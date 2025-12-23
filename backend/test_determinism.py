"""
Test determinism - same inputs should produce same scenario_id
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_determinism():
    """Test that identical inputs produce identical scenario_id"""
    
    # Test payload
    payload = {
        "region": "test",
        "year": 2035,
        "rainfall_delta": -15,
        "temperature_delta": 1.2,
        "urban_growth": 30
    }
    
    print("=" * 60)
    print("DETERMINISM TEST")
    print("=" * 60)
    print(f"Request: {json.dumps(payload, indent=2)}")
    print()
    
    # First request
    print("Making first request...")
    response1 = requests.post(f"{BASE_URL}/simulate", json=payload)
    if response1.status_code != 200:
        print(f"❌ Request 1 failed: {response1.status_code}")
        print(response1.text)
        return False
    
    data1 = response1.json()
    scenario_id_1 = data1.get("scenario_id")
    print(f"✓ First scenario_id: {scenario_id_1}")
    print()
    
    # Second request (should hit cache if deterministic)
    print("Making second request...")
    response2 = requests.post(f"{BASE_URL}/simulate", json=payload)
    if response2.status_code != 200:
        print(f"❌ Request 2 failed: {response2.status_code}")
        print(response2.text)
        return False
    
    data2 = response2.json()
    scenario_id_2 = data2.get("scenario_id")
    print(f"✓ Second scenario_id: {scenario_id_2}")
    print()
    
    # Compare
    if scenario_id_1 == scenario_id_2:
        print("=" * 60)
        print("✅ DETERMINISM TEST PASSED")
        print("=" * 60)
        print(f"Both requests produced identical scenario_id: {scenario_id_1}")
        
        # Check if cached
        cached_1 = data1.get("stats", {}).get("cached", False)
        cached_2 = data2.get("stats", {}).get("cached", False)
        print(f"First request cached: {cached_1}")
        print(f"Second request cached: {cached_2}")
        
        if not cached_1 and cached_2:
            print("✓ Caching working correctly (first computed, second cached)")
        
        return True
    else:
        print("=" * 60)
        print("❌ DETERMINISM TEST FAILED")
        print("=" * 60)
        print(f"scenario_id mismatch:")
        print(f"  Request 1: {scenario_id_1}")
        print(f"  Request 2: {scenario_id_2}")
        return False

def test_different_inputs():
    """Test that different inputs produce different scenario_ids"""
    
    print("\n" + "=" * 60)
    print("UNIQUENESS TEST")
    print("=" * 60)
    
    payloads = [
        {"region": "test", "year": 2035, "rainfall_delta": -15, "temperature_delta": 1.2, "urban_growth": 30},
        {"region": "test", "year": 2035, "rainfall_delta": -10, "temperature_delta": 1.2, "urban_growth": 30},
        {"region": "test", "year": 2040, "rainfall_delta": -15, "temperature_delta": 1.2, "urban_growth": 30},
    ]
    
    scenario_ids = []
    
    for i, payload in enumerate(payloads, 1):
        response = requests.post(f"{BASE_URL}/simulate", json=payload)
        if response.status_code != 200:
            print(f"❌ Request {i} failed: {response.status_code}")
            continue
        
        data = response.json()
        scenario_id = data.get("scenario_id")
        scenario_ids.append(scenario_id)
        print(f"Request {i}: {scenario_id}")
    
    unique_ids = len(set(scenario_ids))
    total_ids = len(scenario_ids)
    
    print()
    if unique_ids == total_ids:
        print(f"✅ UNIQUENESS TEST PASSED: {unique_ids}/{total_ids} unique scenario_ids")
        return True
    else:
        print(f"❌ UNIQUENESS TEST FAILED: {unique_ids}/{total_ids} unique scenario_ids")
        return False

if __name__ == "__main__":
    try:
        # Clear cache first
        print("Clearing cache...")
        requests.post(f"{BASE_URL}/cache/clear")
        print("✓ Cache cleared\n")
        
        # Run tests
        determinism_passed = test_determinism()
        uniqueness_passed = test_different_inputs()
        
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Determinism test: {'✅ PASSED' if determinism_passed else '❌ FAILED'}")
        print(f"Uniqueness test: {'✅ PASSED' if uniqueness_passed else '❌ FAILED'}")
        
        if determinism_passed and uniqueness_passed:
            print("\n🎉 All tests passed! Backend is deterministic.")
        else:
            print("\n⚠️ Some tests failed. Review results above.")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server at http://127.0.0.1:8000")
        print("Make sure the server is running: python run.py")
    except Exception as e:
        print(f"❌ ERROR: {e}")
