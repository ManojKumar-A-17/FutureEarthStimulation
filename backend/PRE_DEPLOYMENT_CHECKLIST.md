# Pre-Deployment Checklist ✅

## Critical Fixes Applied

### 1. ✅ CORS Configuration
- **Issue**: Frontend couldn't connect due to CORS blocking
- **Fix**: Added `CORSMiddleware` in `main.py`
- **Allows**: `http://localhost:5173` and `http://127.0.0.1:5173` (Vite dev server)

### 2. ✅ Region Validation
- **Issue**: Hardcoded region list (only 5 regions) in `models.py`
- **Fix**: Removed hardcoded list, now validates against all 80+ regions dynamically
- **Regions**: Now supports all Indian states, US states, Chinese provinces, Brazilian states, Australian states, European countries, and more

### 3. ✅ Environment Variables
- **Frontend**: Added `VITE_BACKEND_URL` in `.env`
- **Backend**: Uses `EARTH_ENGINE_PROJECT` from `.env`

### 4. ✅ Region Name Normalization
- **Frontend sends**: `"tamilnadu"` (lowercase, no spaces)
- **Backend maps**: `tamilnadu` → `Tamil Nadu` → lookups in REGIONS dict
- **Works for**: All 80+ regions with proper name matching

---

## Verification Steps Before Connecting Frontend

### Step 1: Start Backend Server
```powershell
cd D:\Google-Earth\idea1\FutureEarthStimulation\backend
python run.py
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 2: Test Health Endpoint
```powershell
curl http://127.0.0.1:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "earth_engine": "initialized" // or "error: ..." if GEE not setup
}
```

### Step 3: Test Regions Endpoint
```powershell
curl http://127.0.0.1:8000/regions
```

**Expected Response:**
```json
{
  "regions": [
    {
      "id": "andhrapradesh",
      "name": "Andhra Pradesh",
      "bbox": [76.8, 12.6, 84.8, 19.9],
      "description": "Andhra Pradesh state, India"
    },
    // ... 80+ more regions
  ],
  "count": 81
}
```

### Step 4: Test Simulation Endpoint (Mock Data)
```powershell
curl -X POST http://127.0.0.1:8000/simulate `
  -H "Content-Type: application/json" `
  -d '{
    "region": "tamilnadu",
    "year": 2035,
    "rainfall_delta": -15.0,
    "temperature_delta": 1.2,
    "urban_growth": 30.0
  }'
```

**Expected Response:**
```json
{
  "scenario_id": "a8f3c92b1e4d",
  "data_source": "mock", // or "real" if GEE is setup
  "stats": {
    "urban_gain_pct": 30.5,
    "vegetation_loss_pct": 12.3,
    "crop_stress_index": 0.67,
    "trees_change_pct": -8.1,
    "overall_stress_level": "high",
    "cached": false,
    "computation_time_seconds": 0.15
  },
  "metadata": {
    "region": "tamilnadu",
    "baseline_year": 2020,
    "target_year": 2035
  },
  // ... more fields
}
```

### Step 5: Test CORS (from browser)
Open browser console on `http://localhost:5173` and run:
```javascript
fetch('http://127.0.0.1:8000/health')
  .then(r => r.json())
  .then(d => console.log('✅ CORS working:', d))
  .catch(e => console.error('❌ CORS failed:', e));
```

**Expected**: No CORS errors, health data logged

---

## Known Issues & Solutions

### Issue: "Project not registered for Earth Engine API"
**Status**: Expected for new projects
**Impact**: Simulation will use mock data instead
**Solution**: 
1. Register project: https://console.cloud.google.com/earth-engine
2. Update `.env` with your project ID
3. Restart backend

**Workaround**: Mock data is fully functional for testing

### Issue: Frontend region names don't match
**Status**: ✅ Fixed
**Solution**: Frontend sends lowercase IDs like `"tamilnadu"`, backend normalizes to `"Tamil Nadu"`

### Issue: Simulation takes 5+ seconds
**Status**: Normal for first request per region
**Explanation**: 
- First request: Fetches real GEE data (~3-5s)
- Subsequent requests: Cached (~0.1s)

---

## API Endpoints Summary

| Endpoint | Method | Purpose | Frontend Uses |
|----------|--------|---------|---------------|
| `/health` | GET | Server health check | Connection status |
| `/regions` | GET | List all regions | Region selector |
| `/simulate` | POST | Run simulation | Main functionality |
| `/cache/stats` | GET | Cache statistics | Optional monitoring |
| `/cache/clear` | POST | Clear cache | Optional admin |

---

## Frontend-Backend Contract

### Request Format
```typescript
interface SimulationRequest {
  region: string;          // "tamilnadu", "california", etc.
  year: number;            // 2025-2100
  rainfall_delta: number;  // -50 to 30 (%)
  temperature_delta: number; // -2 to 5 (°C)
  urban_growth: number;    // 0 to 100 (%)
}
```

### Response Format
```typescript
interface SimulationResponse {
  scenario_id: string;
  data_source: "real" | "mock";
  metadata: {
    region: string;
    baseline_year: number;
    target_year: number;
    generated_at: string;
  };
  stats: {
    urban_gain_pct: number;
    vegetation_loss_pct: number;
    crop_stress_index: number;
    trees_change_pct: number;
    crops_change_pct: number;
    overall_stress_level: "low" | "medium" | "high" | "severe";
    cached: boolean;
    computation_time_seconds: number;
  };
  results: {
    climate_stress: {
      combined_stress_index: number;    // 0-1
      rainfall_stress: number;          // 0-1
      temperature_stress: number;       // 0-1
      vegetation_stress: number;        // 0-1
    };
    land_transitions: {
      degraded_area_km2: number;
      urbanized_area_km2: number;
      forest_to_urban_pct: number;
      crops_to_urban_pct: number;
    };
  };
  tile_url: string;
}
```

---

## Deployment Readiness Status

| Component | Status | Notes |
|-----------|--------|-------|
| CORS Setup | ✅ Ready | Configured for Vite |
| Region System | ✅ Ready | 80+ regions working |
| Validation | ✅ Ready | Dynamic validation |
| Error Handling | ✅ Ready | Graceful fallbacks |
| Mock Data | ✅ Ready | Testing without GEE |
| Cache System | ✅ Ready | In-memory caching |
| API Documentation | ✅ Ready | OpenAPI/Swagger |
| Environment Config | ✅ Ready | `.env` files set |

---

## Final Checks Before Frontend Connection

1. ✅ Backend server running on port 8000
2. ✅ `/health` returns healthy status
3. ✅ `/regions` returns 80+ regions
4. ✅ CORS headers present in responses
5. ✅ Test simulation completes successfully
6. ✅ Frontend `.env` has correct backend URL

---

## Start Frontend

```powershell
cd D:\Google-Earth\idea1\FutureEarthStimulation\frontend
npm run dev
# or
bun run dev
```

**Expected**: Frontend opens at `http://localhost:5173` and connects to backend

---

## Troubleshooting

### Frontend shows "Connection Failed"
- Check backend is running: `curl http://127.0.0.1:8000/health`
- Check CORS: Look for CORS errors in browser console
- Check firewall: Ensure port 8000 is accessible

### Simulation returns 400 "Invalid region"
- Check region ID format: Must be lowercase, no spaces
- Test region: `curl http://127.0.0.1:8000/regions | jq '.regions[].id'`

### Simulation is slow
- First request per region: Expected (3-5s)
- Subsequent requests: Should be fast (<0.2s) due to cache
- Check cache: `curl http://127.0.0.1:8000/cache/stats`

---

**System is ready for frontend connection! 🚀**
