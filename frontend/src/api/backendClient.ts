import type { 
  RegionsResponse, 
  SimulationRequest, 
  SimulationResponse, 
  HealthResponse,
  CacheStats 
} from '@/types/simulation';

const API_BASE = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000';

class BackendClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE) {
    this.baseUrl = baseUrl;
  }

  async checkHealth(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) {
      throw new Error('Backend health check failed');
    }
    return response.json();
  }

  async getRegions(): Promise<RegionsResponse> {
    const response = await fetch(`${this.baseUrl}/regions`);
    if (!response.ok) {
      throw new Error('Failed to fetch regions');
    }
    return response.json();
  }

  async simulate(params: SimulationRequest): Promise<SimulationResponse> {
    const response = await fetch(`${this.baseUrl}/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    
    if (!response.ok) {
      if (response.status === 422) {
        const error = await response.json();
        throw new Error(`Validation error: ${JSON.stringify(error.detail)}`);
      }
      throw new Error(`Simulation failed: ${response.status}`);
    }
    
    return response.json();
  }

  async getCacheStats(): Promise<CacheStats> {
    const response = await fetch(`${this.baseUrl}/cache/stats`);
    if (!response.ok) {
      throw new Error('Failed to fetch cache stats');
    }
    return response.json();
  }

  async clearCache(): Promise<{ status: string; message: string; cleared_count: number }> {
    const response = await fetch(`${this.baseUrl}/cache/clear`, {
      method: 'POST',
    });
    if (!response.ok) {
      throw new Error('Failed to clear cache');
    }
    return response.json();
  }
}

export const backendClient = new BackendClient();
export default backendClient;
