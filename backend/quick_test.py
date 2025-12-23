"""Quick endpoint test - run this while server is running"""
import requests

BASE = "http://127.0.0.1:8000"

print("Testing endpoints...")
print("=" * 60)

# 1. Health
print("\n1. GET /health")
r = requests.get(f"{BASE}/health")
print(f"   Status: {r.status_code}, Response: {r.json()}")

# 2. Regions
print("\n2. GET /regions")
r = requests.get(f"{BASE}/regions")
print(f"   Status: {r.status_code}")
data = r.json()
print(f"   Found {len(data['regions'])} regions")

# 3. Simulate (valid)
print("\n3. POST /simulate (valid)")
payload = {"region": "test", "year": 2035, "rainfall_delta": -15, "temperature_delta": 1.2, "urban_growth": 30}
r = requests.post(f"{BASE}/simulate", json=payload)
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"   Scenario ID: {data.get('scenario_id')}")
    print(f"   Has metadata: {'metadata' in data}")
    print(f"   Has results: {'results' in data}")
    print(f"   Has stats: {'stats' in data}")
    print(f"   Cached: {data.get('stats', {}).get('cached', False)}")
else:
    print(f"   Error: {r.text[:200]}")

# 4. Simulate (repeat - should be cached)
print("\n4. POST /simulate (repeat - should cache)")
r = requests.post(f"{BASE}/simulate", json=payload)
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"   Scenario ID: {data.get('scenario_id')}")
    print(f"   Cached: {data.get('stats', {}).get('cached', False)}")

# 5. Cache stats
print("\n5. GET /cache/stats")
r = requests.get(f"{BASE}/cache/stats")
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"   Entries: {data.get('entries', 0)}")
    print(f"   Max size: {data.get('max_size', 0)}")

# 6. Validation test
print("\n6. POST /simulate (invalid - should reject)")
bad_payload = {"region": "test", "year": 2020, "rainfall_delta": -15, "temperature_delta": 1.2, "urban_growth": 30}
r = requests.post(f"{BASE}/simulate", json=bad_payload)
print(f"   Status: {r.status_code} (expect 422)")

print("\n" + "=" * 60)
print("✓ Quick test complete. Start server first if errors.")
