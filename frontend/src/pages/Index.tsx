import { useMemo } from 'react';
import { motion } from 'framer-motion';
import { Header } from '@/components/Layout/Header';
import { MapView } from '@/components/Map/MapView';
import { ControlPanel } from '@/components/Controls/ControlPanel';
import { ResultsPanel } from '@/components/Results/ResultsPanel';
import { useSimulation, useRegions, useBackendHealth } from '@/hooks/useSimulation';
import { Toaster } from '@/components/ui/sonner';
import { toast } from 'sonner';
import { useEffect } from 'react';

const Index = () => {
  const { 
    params, 
    updateParam, 
    result, 
    runSimulation, 
    resetParams, 
    isLoading, 
    error 
  } = useSimulation();

  const { data: regionsData, isLoading: isRegionsLoading } = useRegions();
  const { data: healthData, isLoading: isCheckingHealth } = useBackendHealth();

  const regions = useMemo(() => regionsData?.regions ?? [], [regionsData]);
  const selectedRegion = useMemo(
    () => regions.find(r => r.id === params.region) ?? null,
    [regions, params.region]
  );

  const isConnected = healthData?.status === 'healthy';

  // Show toast on simulation complete
  useEffect(() => {
    if (result && !isLoading) {
      toast.success('Simulation Complete', {
        description: `${result.stats.overall_stress_level.toUpperCase()} stress scenario generated`,
      });
    }
  }, [result, isLoading]);

  // Show error toast
  useEffect(() => {
    if (error) {
      toast.error('Simulation Failed', {
        description: error.message,
      });
    }
  }, [error]);

  return (
    <div className="flex h-screen flex-col bg-background">
      <Toaster position="top-right" theme="dark" />
      
      <Header isConnected={isConnected} isCheckingHealth={isCheckingHealth} />

      <div className="flex flex-1 overflow-hidden">
        {/* Control Panel Sidebar */}
        <motion.aside 
          className="hidden w-80 flex-shrink-0 border-r border-border/50 bg-card/50 lg:block"
          initial={{ x: -100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <ControlPanel
            regions={regions}
            params={params}
            onParamChange={updateParam}
            onRun={runSimulation}
            onReset={resetParams}
            isLoading={isLoading}
            isRegionsLoading={isRegionsLoading}
          />
        </motion.aside>

        {/* Main Content Area */}
        <main className="flex flex-1 flex-col overflow-hidden">
          {/* Map Section */}
          <div className="relative flex-1 p-4">
            <MapView selectedRegion={selectedRegion} />
            
            {/* Mobile Controls Overlay */}
            <div className="absolute left-4 top-4 z-20 lg:hidden">
              <motion.div 
                className="glass-panel rounded-lg p-4"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
              >
                <ControlPanel
                  regions={regions}
                  params={params}
                  onParamChange={updateParam}
                  onRun={runSimulation}
                  onReset={resetParams}
                  isLoading={isLoading}
                  isRegionsLoading={isRegionsLoading}
                />
              </motion.div>
            </div>
          </div>

          {/* Results Section */}
          <motion.div 
            className="border-t border-border/50 bg-card/30 p-6"
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            <ResultsPanel 
              result={result} 
              isLoading={isLoading} 
              error={error} 
            />
          </motion.div>
        </main>
      </div>
    </div>
  );
};

export default Index;
