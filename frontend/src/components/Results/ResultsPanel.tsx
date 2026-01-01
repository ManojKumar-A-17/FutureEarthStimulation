import { motion, AnimatePresence } from 'framer-motion';
import {
  Building2,
  TreePine,
  Wheat,
  Activity,
  Clock,
  Database,
  Zap,
  AlertTriangle
} from 'lucide-react';
import { MetricCard } from './MetricCard';
import { StressIndicator } from './StressIndicator';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import type { SimulationResponse } from '@/types/simulation';
import { format } from 'date-fns';

interface ResultsPanelProps {
  result: SimulationResponse | null;
  isLoading: boolean;
  error: Error | null;
}

function getStressLevelStyle(level: string) {
  switch (level) {
    case 'low': return 'bg-stress-low/20 text-stress-low border-stress-low/30';
    case 'medium': return 'bg-stress-medium/20 text-stress-medium border-stress-medium/30';
    case 'high': return 'bg-stress-high/20 text-stress-high border-stress-high/30';
    case 'severe': return 'bg-stress-severe/20 text-stress-severe border-stress-severe/30';
    default: return 'bg-muted text-muted-foreground';
  }
}

export function ResultsPanel({ result, isLoading, error }: ResultsPanelProps) {
  if (error) {
    return (
      <motion.div
        className="glass-panel rounded-lg p-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <div className="flex items-center gap-3 text-destructive">
          <AlertTriangle className="h-5 w-5" />
          <span className="font-medium">Simulation Error</span>
        </div>
        <p className="mt-2 text-sm text-muted-foreground">{error.message}</p>
      </motion.div>
    );
  }

  if (isLoading) {
    return (
      <motion.div
        className="glass-panel flex flex-col items-center justify-center rounded-lg p-12"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <div className="relative">
          <div className="h-16 w-16 rounded-full border-2 border-primary/30" />
          <div className="absolute inset-0 h-16 w-16 animate-spin rounded-full border-2 border-transparent border-t-primary" />
        </div>
        <p className="mt-4 font-mono text-sm text-muted-foreground">
          Processing satellite data...
        </p>
        <p className="text-xs text-muted-foreground/60">
          This may take 3-5 seconds for new scenarios
        </p>
      </motion.div>
    );
  }

  if (!result) {
    return (
      <motion.div
        className="glass-panel flex flex-col items-center justify-center rounded-lg p-12 text-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <Activity className="h-12 w-12 text-muted-foreground/40" />
        <p className="mt-4 font-mono text-sm text-muted-foreground">
          No simulation results yet
        </p>
        <p className="text-xs text-muted-foreground/60">
          Adjust parameters and run a simulation
        </p>
      </motion.div>
    );
  }

  const { stats, results, metadata, scenario_id, data_source } = result;

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={scenario_id}
        className="space-y-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
      >
        {/* Header with badges */}
        <div className="flex flex-wrap items-center gap-2">
          <h3 className="font-mono text-xs uppercase tracking-widest text-primary">
            Simulation Results
          </h3>
          <div className="flex-1" />

          {stats.cached && (
            <Badge variant="outline" className="gap-1 border-primary/30 bg-primary/10 text-primary">
              <Zap className="h-3 w-3" />
              Cached
            </Badge>
          )}

          <Badge
            variant="outline"
            className={cn("uppercase", getStressLevelStyle(stats.overall_stress_level))}
          >
            {stats.overall_stress_level} Stress
          </Badge>

          <Badge variant="outline" className="border-border/50">
            {data_source === 'real' ? '🛰️ Real Data' : '📊 Mock Data'}
          </Badge>
        </div>

        {/* Summary Cards Grid */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            icon={<Building2 className="h-4 w-4" />}
            label="Urban Gain"
            value={stats.urban_gain_pct}
            unit="%"
            trend={stats.urban_gain_pct > 20 ? 'negative' : 'neutral'}
            delay={0.1}
          />
          <MetricCard
            icon={<TreePine className="h-4 w-4" />}
            label="Vegetation Loss"
            value={stats.vegetation_loss_pct}
            unit="%"
            trend={stats.vegetation_loss_pct > 5 ? 'negative' : 'neutral'}
            delay={0.2}
          />
          <MetricCard
            icon={<Wheat className="h-4 w-4" />}
            label="Crop Stress"
            value={stats.crop_stress_index.toFixed(1)}
            unit="%"
            trend={stats.crop_stress_index > 0.5 ? 'negative' : 'neutral'}
            delay={0.3}
          />
          <MetricCard
            icon={<Activity className="h-4 w-4" />}
            label="Trees Change"
            value={stats.trees_change_pct}
            unit="%"
            trend={stats.trees_change_pct < 0 ? 'negative' : 'positive'}
            delay={0.4}
          />
        </div>

        {/* Stress Indicators */}
        <motion.div
          className="glass-panel rounded-lg p-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <h4 className="mb-4 font-mono text-xs uppercase tracking-widest text-muted-foreground">
            Climate Stress Breakdown
          </h4>
          <div className="grid gap-6 md:grid-cols-2">
            <StressIndicator
              value={stats.combined_stress_index ?? 0}
              label="Combined Stress Index"
            />
            <StressIndicator
              value={stats.rainfall_stress_index ?? 0}
              label="Rainfall Stress"
            />
            <StressIndicator
              value={stats.temperature_stress_index ?? 0}
              label="Temperature Stress"
            />
            <StressIndicator
              value={stats.vegetation_stress_index ?? 0}
              label="Vegetation Stress"
            />
          </div>
        </motion.div>

        {/* Land Transitions */}
        <motion.div
          className="glass-panel rounded-lg p-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
        >
          <h4 className="mb-4 font-mono text-xs uppercase tracking-widest text-muted-foreground">
            Land Transitions
          </h4>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-md bg-secondary/30 p-4">
              <p className="font-mono text-xs text-muted-foreground">Degraded Area</p>
              <p className="mt-1 font-mono text-xl font-bold text-stress-high">
                {results.land_transitions.degraded_area_km2.toLocaleString()}
                <span className="text-sm font-normal text-muted-foreground"> km²</span>
              </p>
            </div>
            <div className="rounded-md bg-secondary/30 p-4">
              <p className="font-mono text-xs text-muted-foreground">Urbanized Area</p>
              <p className="mt-1 font-mono text-xl font-bold text-stress-medium">
                {results.land_transitions.urbanized_area_km2.toLocaleString()}
                <span className="text-sm font-normal text-muted-foreground"> km²</span>
              </p>
            </div>
          </div>
        </motion.div>

        {/* Metadata Footer */}
        <motion.div
          className="flex flex-wrap items-center gap-x-6 gap-y-2 text-xs text-muted-foreground"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
        >
          <div className="flex items-center gap-1">
            <Database className="h-3 w-3" />
            <span className="font-mono">{scenario_id.slice(0, 12)}...</span>
          </div>
          <div className="flex items-center gap-1">
            <Clock className="h-3 w-3" />
            <span>{format(new Date(metadata.generated_at), 'PPp')}</span>
          </div>
          <div>
            Baseline: {metadata.baseline_year} → Target: {metadata.target_year}
          </div>
          <div>
            Computed in {stats.computation_time_seconds.toFixed(2)}s
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
