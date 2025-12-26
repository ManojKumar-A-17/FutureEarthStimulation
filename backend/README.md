# Alternate Earth Futures - Backend

**AI-Generated Simulation System for Exploring Alternate Earth Futures**

>  **Important**: This system generates **SIMULATIONS**, not predictions. Results represent possible futures under specified conditions, not forecasts of actual outcomes.

---

##  Overview

This backend provides a production-quality API for simulating alternate Earth futures based on climate and development scenarios. It combines real satellite data from Google Earth Engine with explainable machine learning models to generate plausible future states.

### Key Features

✅ **Real Satellite Data** - Fetches land cover, rainfall, temperature, and vegetation data from Google Earth Engine  
✅ **Simulation Logic** - Rule-based models for climate stress and land transitions  
✅ **Production API** - Clean REST API with request validation and caching  
✅ **Deterministic** - Same input always produces same output  
✅ **Free-Tier Compatible** - Works on free hosting (Render, Railway)  
✅ **Frontend-Agnostic** - Returns structured JSON for any frontend  

---

##  Quick Start

### Prerequisites

- Python 3.10+
- Google Cloud Project with Earth Engine enabled
- Virtual environment (`.venv`)

### Installation

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with:
EARTH_ENGINE_PROJECT=your-gcp-project-id

# Authenticate with Earth Engine (one time)
earthengine authenticate

# Run the server
python run.py
```

Server runs at: **http://127.0.0.1:8000**

---

## 📡 API Endpoints

### Production Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| **`/simulate`** | **POST** | **Main simulation endpoint** |
| `/health` | GET | Health check and EE status |
| `/regions` | GET | List available regions |
| `/cache/stats` | GET | Get cache statistics |
| `/cache/clear` | POST | Clear cached scenarios |
| `/docs` | GET | Interactive API documentation |

### Debug Endpoints (Not for Production)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/data-test/{region}` | GET | Test GEE data fetching |
| `/simulation-test/{region}` | GET | Test simulation pipeline |
| `/ee-test` | GET | Test Earth Engine connectivity |

---

##  Main API: POST /simulate

### Request Body

```json
{
  "region": "Tamil Nadu",
  "year": 2035,
  "rainfall_delta": -15.0,
  "temperature_delta": 1.2,
  "urban_growth": 30.0
}
```

### Parameters

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `region` | string | - | Region name (Tamil Nadu, Karnataka, Kerala, India, test) |
| `year` | integer | 2025-2100 | Target year for simulation |
| `rainfall_delta` | float | -50 to +30 | Rainfall change (%) |
| `temperature_delta` | float | -2 to +5 | Temperature change (°C) |
| `urban_growth` | float | 0 to 100 | Urban area growth (%) |

### Response

```json
{
  "scenario_id": "abc123def456",
  "tile_url": "/tiles/abc123def456/{z}/{x}/{y}.png",
  "stats": {
    "urban_gain_pct": 12.4,
    "vegetation_loss_pct": 9.1,
    "crop_stress_index": 0.67,
    "trees_change_pct": -8.2,
    "crops_change_pct": -5.5,
    "overall_stress_level": "high"
  },
  "metadata": {
    "region": "Tamil Nadu",
    "baseline_year": 2020,
    "target_year": 2035,
    "generated_at": "2025-12-23T12:00:00Z"
  },
  "data_source": "mock"
}
```

### Example using cURL

```bash
curl -X POST http://127.0.0.1:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "region": "test",
    "year": 2035,
    "rainfall_delta": -20.0,
    "temperature_delta": 1.5,
    "urban_growth": 40.0
  }'
```

### Example using Python

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/simulate",
    json={
        "region": "Tamil Nadu",
        "year": 2040,
        "rainfall_delta": -25.0,
        "temperature_delta": 2.0,
        "urban_growth": 50.0
    }
)

result = response.json()
print(f"Scenario ID: {result['scenario_id']}")
print(f"Vegetation Loss: {result['stats']['vegetation_loss_pct']}%")
```

---

##  Architecture

```
backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration & validation rules
│   ├── api/
│   │   ├── models.py           # Pydantic request/response models
│   │   └── simulate.py         # /simulate endpoint logic
│   ├── gee/
│   │   └── data_loader.py      # Google Earth Engine integration
│   ├── ml/
│   │   ├── climate_stress.py   # Climate stress calculation
│   │   ├── land_transition.py  # Land cover transition model
│   │   └── simulation_engine.py # Simulation orchestrator
│   └── utils/
│       ├── cache.py            # In-memory caching
│       └── regions.py          # Region definitions
├── requirements.txt            # Python dependencies
├── run.py                      # Server launcher
└── .env                        # Environment variables
```

---

##  Testing

### Test Production Endpoint

```bash
cd backend
python test_api.py
```

### Test Simulation Logic

```bash
python test_simulation.py
```

### Verify Determinism

Run the same request twice - results should be identical (except timestamps):

```bash
# First request
curl -X POST http://127.0.0.1:8000/simulate -H "Content-Type: application/json" \
  -d '{"region": "test", "year": 2035, "rainfall_delta": -15, "temperature_delta": 1.2, "urban_growth": 30}'

# Second request (same parameters)
curl -X POST http://127.0.0.1:8000/simulate -H "Content-Type: application/json" \
  -d '{"region": "test", "year": 2035, "rainfall_delta": -15, "temperature_delta": 1.2, "urban_growth": 30}'

# scenario_id should be IDENTICAL
```

---

##  Simulation Methodology

### Data Sources (via Google Earth Engine)

- **Land Cover**: Dynamic World (Google/World Resources Institute)
- **Rainfall**: CHIRPS (Climate Hazards Group)
- **Temperature**: MODIS Land Surface Temperature
- **Vegetation**: MODIS NDVI

### Models

#### 1. Climate Stress Model
Calculates vegetation stress based on:
- Rainfall deficit/excess
- Temperature increase
- Baseline vegetation health (NDVI)

**Output**: Stress index (0-1) and crop stress level (low/moderate/high/severe)

#### 2. Land Transition Model
Simulates land cover changes:
- **Under stress**: Trees → Grass/Shrub, Crops → Bare/Grass
- **Urban growth**: Expansion into Crops → Grass → Trees (priority order)

**Output**: Future land cover distribution with transition details

#### 3. Simulation Engine
Orchestrates the complete workflow:
1. Fetch baseline data (2020)
2. Apply climate stress
3. Calculate land transitions
4. Generate statistics
5. Cache results

---

##  Configuration

### Validation Constraints

Defined in `app/config.py`:

```python
RAIN_DELTA_MIN = -50.0    # Max 50% decrease
RAIN_DELTA_MAX = 30.0     # Max 30% increase
TEMP_DELTA_MIN = -2.0     # Cooling scenario
TEMP_DELTA_MAX = 5.0      # Extreme warming
URBAN_GROWTH_MIN = 0.0    # No growth
URBAN_GROWTH_MAX = 100.0  # 100% expansion
```

### Cache Settings

```python
CACHE_MAX_SIZE = 100      # Max cached scenarios
CACHE_TTL_HOURS = 24      # Cache lifetime
```

---

## 🌍 Available Regions

| Region | Bounding Box | Description |
|--------|--------------|-------------|
| `Tamil Nadu` | [77.0, 8.0, 80.5, 13.5] | Tamil Nadu state, India |
| `Karnataka` | [74.0, 11.5, 78.5, 18.5] | Karnataka state, India |
| `Kerala` | [74.8, 8.2, 77.4, 12.8] | Kerala state, India |
| `India` | [68.0, 6.0, 97.0, 36.0] | Full country |
| `test` | [78.46, 20.09, 79.46, 21.09] | Test region (~100km²) |

---

##  Error Handling

### Common Errors

| Status | Error | Solution |
|--------|-------|----------|
| 400 | Invalid parameters | Check parameter ranges in API docs |
| 404 | Region not found | Use `/regions` to see available regions |
| 500 | Earth Engine error | System falls back to mock data automatically |

### Earth Engine Not Registered

If GEE project isn't registered, the system automatically:
1. Falls back to mock baseline data
2. Still runs full simulation
3. Returns `"data_source": "mock"` in response

This ensures **zero downtime** even without GEE access.

---

##  Performance

- **First request**: ~5-10 seconds (fetches real data)
- **Cached requests**: <100ms
- **Memory usage**: <200MB
- **Cold start**: ~3 seconds

---

##  Academic Context

### This is NOT a Prediction System

This backend demonstrates:
✅ Cloud-based geospatial processing  
✅ Simulation-based modeling  
✅ Ethical ML system design  
✅ Production-ready architecture  

It explicitly **does not claim** to:
❌ Predict actual future outcomes  
❌ Replace climate models  
❌ Provide actionable forecasts  

### Suitable For

- Final year projects
- Research prototypes
- Portfolio demonstrations
- Technical interviews

---



**Built with**: FastAPI, Google Earth Engine, NumPy, scikit-learn
