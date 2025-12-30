"""
Pydantic models for API request/response validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from app.config import (
    RAIN_DELTA_MIN, RAIN_DELTA_MAX,
    TEMP_DELTA_MIN, TEMP_DELTA_MAX,
    URBAN_GROWTH_MIN, URBAN_GROWTH_MAX,
    TARGET_YEAR_MIN, TARGET_YEAR_MAX
)


class SimulationRequest(BaseModel):
    """Request model for /simulate endpoint"""
    
    region: str = Field(
        ...,
        description="Region name (e.g., 'Tamil Nadu', 'test')",
        examples=["Tamil Nadu", "test"]
    )
    
    year: int = Field(
        default=2035,
        ge=TARGET_YEAR_MIN,
        le=TARGET_YEAR_MAX,
        description=f"Target year for simulation ({TARGET_YEAR_MIN}-{TARGET_YEAR_MAX})"
    )
    
    rainfall_delta: float = Field(
        ...,
        ge=RAIN_DELTA_MIN,
        le=RAIN_DELTA_MAX,
        description=f"Rainfall change in percentage ({RAIN_DELTA_MIN} to {RAIN_DELTA_MAX})"
    )
    
    temperature_delta: float = Field(
        ...,
        ge=TEMP_DELTA_MIN,
        le=TEMP_DELTA_MAX,
        description=f"Temperature change in Celsius ({TEMP_DELTA_MIN} to {TEMP_DELTA_MAX})"
    )
    
    urban_growth: float = Field(
        default=0.0,
        ge=URBAN_GROWTH_MIN,
        le=URBAN_GROWTH_MAX,
        description=f"Urban growth in percentage ({URBAN_GROWTH_MIN} to {URBAN_GROWTH_MAX})"
    )
    
    @field_validator('region')
    @classmethod
    def validate_region(cls, v: str) -> str:
        """Validate region name - actual validation happens in simulate.py against all 80+ regions"""
        # Basic validation - just check it's not empty
        if not v or not v.strip():
            raise ValueError("Region cannot be empty")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "region": "Tamil Nadu",
                "year": 2035,
                "rainfall_delta": -15.0,
                "temperature_delta": 1.2,
                "urban_growth": 30.0
            }
        }


class SimulationResults(BaseModel):
    """Detailed simulation results"""
    
    climate_stress: Dict[str, Any] = Field(description="Climate stress analysis")
    land_transitions: Dict[str, Any] = Field(description="Land cover transitions")
    

class SimulationStats(BaseModel):
    """Summary statistics from simulation"""
    
    urban_gain_pct: float = Field(description="Urban area increase %")
    vegetation_loss_pct: float = Field(description="Vegetation loss %")
    crop_stress_index: float = Field(description="Crop stress index (0-1)")
    trees_change_pct: float = Field(description="Tree cover change %")
    crops_change_pct: float = Field(description="Crop area change %")
    overall_stress_level: str = Field(description="Overall stress level")
    
    # Detailed stress breakdown
    rainfall_stress_index: Optional[float] = Field(default=0.0, description="Rainfall stress %")
    temperature_stress_index: Optional[float] = Field(default=0.0, description="Temperature stress %")
    vegetation_stress_index: Optional[float] = Field(default=0.0, description="Vegetation stress %")
    combined_stress_index: Optional[float] = Field(default=0.0, description="Combined stress %")
    cached: bool = Field(default=False, description="Whether result was from cache")
    computation_time_seconds: float = Field(default=0.0, description="Time taken to compute")


class SimulationResponse(BaseModel):
    """Response model for /simulate endpoint"""
    
    scenario_id: str = Field(description="Unique scenario identifier")
    
    metadata: Dict[str, Any] = Field(description="Scenario metadata")
    
    results: SimulationResults = Field(description="Detailed simulation results")
    
    stats: SimulationStats = Field(description="Summary statistics")
    
    tile_url: str = Field(
        description="URL template for map tiles",
        examples=["/tiles/abc123/{z}/{x}/{y}.png"]
    )
    
    data_source: str = Field(
        default="real",
        description="Data source: 'real' or 'mock'"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
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
                    "target_year": 2035
                },
                "data_source": "mock"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    
    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    detail: Optional[str] = Field(None, description="Additional details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid region specified",
                "detail": "Region must be one of: Tamil Nadu, Karnataka, Kerala, India, test"
            }
        }
