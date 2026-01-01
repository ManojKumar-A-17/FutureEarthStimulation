import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import ee
from app.gee.data_loader import GEEDataLoader
from app.utils.regions import get_available_regions, get_region_info
from app.ml.simulation_engine import SimulationEngine
from app.api.models import SimulationRequest, SimulationResponse, ErrorResponse
from app.api.simulate import SimulateAPI
from app.utils.cache import get_cache

# Load env vars
load_dotenv()

# Initialize Earth Engine
print("Initializing Earth Engine...")
try:
    import json
    from google.oauth2.service_account import Credentials

    project = os.getenv("EARTH_ENGINE_PROJECT")
    service_account_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    
    if service_account_json:
        # Production: Use Service Account from JSON string in env var
        print("Using Service Account authentication (Production mode)")
        creds_dict = json.loads(service_account_json)
        creds = Credentials.from_service_account_info(creds_dict)
        ee.Initialize(credentials=creds, project=project)
    else:
        # Local: Use default browser login
        print(f"Using default authentication (Local mode). Project: {project}")
        ee.Initialize(project=project)
        
    print("Earth Engine initialized successfully.")
    EE_STATUS = "initialized"
except Exception as e:
    print(f"Earth Engine initialization failed: {e}")
    EE_STATUS = f"error: {e}"

app = FastAPI(
    title="Alternate Earth Futures Backend",
    description="AI-powered simulation system for exploring alternate Earth futures using real satellite data",
    version="1.0.0"
)

# Global Exception Handler to prevent crashes
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print(f"CRITICAL ERROR handling request {request.url}: {str(e)}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error", "detail": str(e)}
        )

# CRITICAL: Add CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
data_loader = GEEDataLoader()
simulation_engine = SimulationEngine()
simulate_api = SimulateAPI()

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "earth_engine": EE_STATUS
    }


# ============================================================================
# DEBUG ENDPOINTS (NOT FOR PRODUCTION USE)
# ============================================================================

@app.get("/ee-test", tags=["Debug"])
def earth_engine_test():
    """
    ⚠️ DEBUG ONLY - Simple Earth Engine connectivity test
    
    Fetches mean elevation from NASA DEM to verify EE works.
    Not used in production.
    """
    image = ee.Image("NASA/NASADEM_HGT/001")
    mean_elevation = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=ee.Geometry.Point([78.9629, 20.5937]),  # India center
        scale=1000,
        maxPixels=1e9
    ).getInfo()

    return {
        "message": "Earth Engine working",
        "sample_data": mean_elevation
    }


@app.get("/regions", tags=["Reference"])
def list_regions():
    """
    Get list of available regions
    """
    regions = get_available_regions()
    return {
        "regions": regions,
        "count": len(regions)
    }


@app.get("/regions/{region_name}", tags=["Reference"])
def get_region_details(region_name: str):
    """
    Get details about a specific region
    """
    try:
        info = get_region_info(region_name)
        return {
            "region": region_name,
            "info": info
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/data-test/{region_name}", tags=["Debug"])
def test_data_loader(region_name: str, year: int = 2020):
    """
    ⚠️ DEBUG ONLY - Test GEE data loader
    
    Tests whether baseline data can be fetched from Google Earth Engine.
    Not used in production flow.
    
    Args:
        region_name: Name of region (e.g., 'test', 'Tamil Nadu')
        year: Year of data (default: 2020)
    """
    try:
        # Fetch baseline state
        data = data_loader.fetch_baseline_state(region_name, year)
        
        return {
            "status": "success",
            "message": f"Successfully loaded data for {region_name} in {year}",
            "data": data
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        error_msg = str(e)
        
        # Check if it's an Earth Engine registration error
        if "not registered" in error_msg.lower() or "earth engine" in error_msg.lower():
            return {
                "status": "warning",
                "message": "Earth Engine project not registered (expected for new projects)",
                "note": "This is normal - register your project at: https://console.cloud.google.com/earth-engine",
                "error": error_msg,
                "mock_data": {
                    "region": region_name,
                    "year": year,
                    "land_cover": {"note": "Would contain Dynamic World land cover data"},
                    "rainfall": {"note": "Would contain CHIRPS rainfall data"},
                    "temperature": {"note": "Would contain MODIS temperature data"},
                    "ndvi": {"note": "Would contain MODIS NDVI data"}
                }
            }
        
        # Other errors
        raise HTTPException(status_code=500, detail=f"Data fetch error: {str(e)}")


@app.get("/simulation-test/{region_name}", tags=["Debug"])
def test_simulation(
    region_name: str = "test",
    year: int = 2020,
    rainfall_delta: float = -15.0,
    temp_delta: float = 1.2,
    urban_growth: float = 30.0
):
    """
    ⚠️ DEBUG ONLY - Test complete simulation pipeline
    
    Tests the full simulation flow with mock data fallback.
    Not used in production - use POST /simulate instead.
    
    Args:
        region_name: Region to simulate
        year: Baseline year
        rainfall_delta: Rainfall change (%)
        temp_delta: Temperature change (°C)
        urban_growth: Urban growth (%)
    """
    try:
        # Step 1: Try to fetch baseline data from GEE
        try:
            baseline_data = data_loader.fetch_baseline_state(region_name, year)
            data_source = "real_gee_data"
        except Exception as e:
            # If GEE fails (e.g., not registered), use mock data
            error_msg = str(e)
            if "not registered" in error_msg.lower() or "earth engine" in error_msg.lower():
                # Use mock baseline data for simulation
                baseline_data = {
                    'region': region_name,
                    'year': year,
                    'land_cover': {
                        'classes': {
                            '1': 500,   # trees
                            '2': 300,   # grass
                            '4': 700,   # crops
                            '5': 200,   # shrub
                            '6': 200,   # built
                            '7': 100    # bare
                        },
                        'metadata': {'note': 'Mock data - GEE not available'}
                    },
                    'rainfall': {'annual_mean_mm': 1000},
                    'temperature': {'mean_celsius': 25.0},
                    'ndvi': {'mean_ndvi': 0.55}
                }
                data_source = "mock_data"
            else:
                raise  # Re-raise if it's a different error
        
        # Step 2: Define scenario
        scenario = {
            'target_year': year + 15,
            'rainfall_delta': rainfall_delta,
            'temperature_delta': temp_delta,
            'urban_growth': urban_growth
        }
        
        # Step 3: Run simulation
        results = simulation_engine.run_simulation(baseline_data, scenario)
        
        # Step 4: Get summary
        summary = simulation_engine.get_scenario_summary(results)
        
        return {
            "status": "success",
            "message": "Simulation completed successfully",
            "data_source": data_source,
            "note": "Using mock data because Earth Engine is not registered" if data_source == "mock_data" else None,
            "summary": summary,
            "results": results
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")


# ============================================================================
# PRODUCTION API ENDPOINTS
# ============================================================================

@app.post("/simulate", response_model=SimulationResponse, tags=["Production"])
async def simulate_scenario(request: SimulationRequest):
    """
    🚀 PRODUCTION ENDPOINT: Run Earth future simulation
    
    This endpoint accepts scenario parameters and returns simulated future Earth state.
    
    **This is SIMULATION, not prediction.**
    
    Example request:
    ```json
    {
        "region": "Tamil Nadu",
        "year": 2035,
        "rainfall_delta": -15.0,
        "temperature_delta": 1.2,
        "urban_growth": 30.0
    }
    ```
    
    Returns:
    - scenario_id: Unique identifier
    - tile_url: Map tile URL template
    - stats: Summary statistics
    - metadata: Additional information
    """
    return await simulate_api.run_simulation(request)


@app.get("/cache/stats", tags=["System"])
def get_cache_stats():
    """Get cache statistics"""
    cache = get_cache()
    stats = cache.get_stats()
    
    return {
        "entries": stats['size'],
        "max_size": stats['max_size'],
        "ttl_hours": stats['ttl_hours'],
        "scenarios": [
            {"scenario_id": sid} for sid in stats['cached_scenarios']
        ]
    }


@app.post("/cache/clear", tags=["System"])
def clear_cache_endpoint():
    """Clear all cached scenarios"""
    cache = get_cache()
    initial_size = cache.size()
    cache.clear()
    return {
        "status": "ok",
        "message": "Cache cleared successfully",
        "cleared_count": initial_size
    }
