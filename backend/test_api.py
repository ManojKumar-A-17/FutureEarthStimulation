"""
Test script for production /simulate endpoint
"""
import requests
import json


def test_simulate_endpoint():
    """Test POST /simulate endpoint"""
    
    url = "http://127.0.0.1:8000/simulate"
    
    # Test scenario
    payload = {
        "region": "test",
        "year": 2035,
        "rainfall_delta": -20.0,
        "temperature_delta": 1.5,
        "urban_growth": 40.0
    }
    
    print("=" * 70)
    print("TESTING POST /simulate")
    print("=" * 70)
    print("\nRequest:")
    print(json.dumps(payload, indent=2))
    print("\nSending request...")
    
    try:
        response = requests.post(url, json=payload)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS!")
            result = response.json()
            print("\nResponse:")
            print(json.dumps(result, indent=2))
            
            print("\n" + "=" * 70)
            print("KEY RESULTS:")
            print("=" * 70)
            print(f"Scenario ID: {result['scenario_id']}")
            print(f"Tile URL: {result['tile_url']}")
            print(f"Data Source: {result['data_source']}")
            print("\nStatistics:")
            for key, value in result['stats'].items():
                print(f"  - {key}: {value}")
        else:
            print("\n❌ FAILED!")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server")
        print("Make sure the server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


def test_cache_stats():
    """Test cache statistics endpoint"""
    print("\n" + "=" * 70)
    print("TESTING GET /cache/stats")
    print("=" * 70)
    
    try:
        response = requests.get("http://127.0.0.1:8000/cache/stats")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS!")
            result = response.json()
            print("\nCache Stats:")
            print(json.dumps(result, indent=2))
        else:
            print("\n❌ FAILED!")
            print(response.text)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


if __name__ == "__main__":
    print("\n🚀 TESTING PRODUCTION /simulate ENDPOINT\n")
    
    test_simulate_endpoint()
    test_cache_stats()
    
    print("\n" + "=" * 70)
    print("✅ TESTS COMPLETED")
    print("=" * 70)
    print("\nYou can also test the API interactively at:")
    print("👉 http://127.0.0.1:8000/docs")
    print()
