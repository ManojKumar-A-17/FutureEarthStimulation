import { motion } from 'framer-motion';
import { Calendar, CloudRain, Thermometer, Building2, Play, RotateCcw, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { RegionSelector } from './RegionSelector';
import { ParameterSlider } from './ParameterSlider';
import type { Region } from '@/types/simulation';
import type { SimulationParams } from '@/hooks/useSimulation';
import { PARAMETER_CONSTRAINTS } from '@/types/simulation';

interface ControlPanelProps {
  regions: Region[];
  params: SimulationParams;
  onParamChange: <K extends keyof SimulationParams>(key: K, value: SimulationParams[K]) => void;
  onRun: () => void;
  onReset: () => void;
  isLoading: boolean;
  isRegionsLoading: boolean;
}

export function ControlPanel({
  regions,
  params,
  onParamChange,
  onRun,
  onReset,
  isLoading,
  isRegionsLoading,
}: ControlPanelProps) {
  return (
    <motion.div 
      className="flex h-full flex-col gap-6 overflow-y-auto p-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      {/* Header */}
      <div className="space-y-1">
        <h2 className="font-mono text-xs uppercase tracking-widest text-primary">
          Simulation Parameters
        </h2>
        <div className="h-px bg-gradient-to-r from-primary/50 to-transparent" />
      </div>

      {/* Region Selector */}
      <RegionSelector
        regions={regions}
        selectedRegionId={params.region}
        onSelect={(id) => onParamChange('region', id)}
        isLoading={isRegionsLoading}
      />

      {/* Divider */}
      <div className="h-px bg-border/50" />

      {/* Parameter Sliders */}
      <div className="space-y-8">
        <ParameterSlider
          label="Target Year"
          icon={<Calendar className="h-4 w-4" />}
          value={params.year}
          min={PARAMETER_CONSTRAINTS.year.min}
          max={PARAMETER_CONSTRAINTS.year.max}
          step={PARAMETER_CONSTRAINTS.year.step}
          unit=""
          onChange={(v) => onParamChange('year', v)}
          delay={0.2}
        />

        <ParameterSlider
          label="Rainfall Change"
          icon={<CloudRain className="h-4 w-4" />}
          value={params.rainfall_delta}
          min={PARAMETER_CONSTRAINTS.rainfall_delta.min}
          max={PARAMETER_CONSTRAINTS.rainfall_delta.max}
          step={PARAMETER_CONSTRAINTS.rainfall_delta.step}
          unit="%"
          onChange={(v) => onParamChange('rainfall_delta', v)}
          colorScheme="rainfall"
          delay={0.3}
        />

        <ParameterSlider
          label="Temperature Change"
          icon={<Thermometer className="h-4 w-4" />}
          value={params.temperature_delta}
          min={PARAMETER_CONSTRAINTS.temperature_delta.min}
          max={PARAMETER_CONSTRAINTS.temperature_delta.max}
          step={PARAMETER_CONSTRAINTS.temperature_delta.step}
          unit="°C"
          onChange={(v) => onParamChange('temperature_delta', v)}
          colorScheme="temperature"
          delay={0.4}
        />

        <ParameterSlider
          label="Urban Growth"
          icon={<Building2 className="h-4 w-4" />}
          value={params.urban_growth}
          min={PARAMETER_CONSTRAINTS.urban_growth.min}
          max={PARAMETER_CONSTRAINTS.urban_growth.max}
          step={PARAMETER_CONSTRAINTS.urban_growth.step}
          unit="%"
          onChange={(v) => onParamChange('urban_growth', v)}
          colorScheme="urban"
          delay={0.5}
        />
      </div>

      {/* Spacer */}
      <div className="flex-1" />

      {/* Action Buttons */}
      <motion.div 
        className="space-y-3"
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        <Button 
          onClick={onRun} 
          disabled={isLoading}
          className="w-full gap-2 bg-primary font-mono uppercase tracking-wider text-primary-foreground hover:bg-primary/90 glow-primary"
          size="lg"
        >
          {isLoading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Processing...
            </>
          ) : (
            <>
              <Play className="h-4 w-4" />
              Run Simulation
            </>
          )}
        </Button>

        <Button 
          onClick={onReset}
          variant="outline"
          className="w-full gap-2 border-border/50 font-mono uppercase tracking-wider hover:bg-secondary"
        >
          <RotateCcw className="h-4 w-4" />
          Reset Parameters
        </Button>
      </motion.div>
    </motion.div>
  );
}
