// API Types for Alternate Earth Futures Simulator

export interface Region {
  id: string;
  name: string;
  bbox: [number, number, number, number]; // [minLng, minLat, maxLng, maxLat]
  description: string;
}

export interface RegionsResponse {
  regions: Region[];
  count: number;
}

export interface SimulationRequest {
  region: string;
  year: number;
  rainfall_delta: number;
  temperature_delta: number;
  urban_growth: number;
}

export interface ClimateStress {
  combined_stress_index: number;
  rainfall_stress: number;
  temperature_stress: number;
  vegetation_stress: number;
}

export interface LandTransitions {
  degraded_area_km2: number;
  urbanized_area_km2: number;
  transitions: {
    crops_to_bare?: number;
    trees_to_shrub?: number;
    [key: string]: number | undefined;
  };
}

export interface SimulationStats {
  urban_gain_pct: number;
  vegetation_loss_pct: number;
  crop_stress_index: number;
  trees_change_pct: number;
  crops_change_pct: number;
  overall_stress_level: 'low' | 'medium' | 'high' | 'severe';
  rainfall_stress_index?: number;
  temperature_stress_index?: number;
  vegetation_stress_index?: number;
  combined_stress_index?: number;
  cached: boolean;
  computation_time_seconds: number;
}

export interface SimulationMetadata {
  region: string;
  baseline_year: number;
  target_year: number;
  generated_at: string;
}

export interface SimulationResponse {
  scenario_id: string;
  metadata: SimulationMetadata;
  results: {
    climate_stress: ClimateStress;
    land_transitions: LandTransitions;
  };
  stats: SimulationStats;
  tile_url: string;
  data_source: 'real' | 'mock';
}

export interface HealthResponse {
  status: string;
  earth_engine: string;
}

export interface CacheStats {
  entries: number;
  max_size: number;
  ttl_hours: number;
  scenarios: Array<{ scenario_id: string }>;
}

export const PARAMETER_CONSTRAINTS = {
  year: { min: 2025, max: 2100, default: 2050, step: 5 },
  rainfall_delta: { min: -50, max: 30, default: 0, step: 5 },
  temperature_delta: { min: -2, max: 5, default: 0, step: 0.5 },
  urban_growth: { min: 0, max: 100, default: 0, step: 10 },
} as const;
