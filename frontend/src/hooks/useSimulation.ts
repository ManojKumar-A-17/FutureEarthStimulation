import { useState, useCallback } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import backendClient from '@/api/backendClient';
import type { SimulationRequest, SimulationResponse } from '@/types/simulation';
import { PARAMETER_CONSTRAINTS } from '@/types/simulation';

export interface SimulationParams {
  region: string;
  year: number;
  rainfall_delta: number;
  temperature_delta: number;
  urban_growth: number;
}

export function useSimulation() {
  const [params, setParams] = useState<SimulationParams>({
    region: 'tamilnadu',
    year: PARAMETER_CONSTRAINTS.year.default,
    rainfall_delta: PARAMETER_CONSTRAINTS.rainfall_delta.default,
    temperature_delta: PARAMETER_CONSTRAINTS.temperature_delta.default,
    urban_growth: PARAMETER_CONSTRAINTS.urban_growth.default,
  });

  const [result, setResult] = useState<SimulationResponse | null>(null);

  const mutation = useMutation({
    mutationFn: (request: SimulationRequest) => backendClient.simulate(request),
    onSuccess: (data) => {
      setResult(data);
    },
  });

  const runSimulation = useCallback(() => {
    mutation.mutate(params);
  }, [params, mutation]);

  const resetParams = useCallback(() => {
    setParams({
      region: params.region,
      year: PARAMETER_CONSTRAINTS.year.default,
      rainfall_delta: PARAMETER_CONSTRAINTS.rainfall_delta.default,
      temperature_delta: PARAMETER_CONSTRAINTS.temperature_delta.default,
      urban_growth: PARAMETER_CONSTRAINTS.urban_growth.default,
    });
    setResult(null);
  }, [params.region]);

  const updateParam = useCallback(<K extends keyof SimulationParams>(
    key: K,
    value: SimulationParams[K]
  ) => {
    setParams(prev => ({ ...prev, [key]: value }));
  }, []);

  return {
    params,
    setParams,
    updateParam,
    result,
    runSimulation,
    resetParams,
    isLoading: mutation.isPending,
    error: mutation.error,
    isError: mutation.isError,
  };
}

export function useRegions() {
  return useQuery({
    queryKey: ['regions'],
    queryFn: () => backendClient.getRegions(),
    staleTime: Infinity,
  });
}

export function useBackendHealth() {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => backendClient.checkHealth(),
    refetchInterval: 30000,
    retry: 1,
  });
}
