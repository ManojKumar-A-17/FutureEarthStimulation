import { motion } from 'framer-motion';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { MapPin } from 'lucide-react';
import type { Region } from '@/types/simulation';

interface RegionSelectorProps {
  regions: Region[];
  selectedRegionId: string;
  onSelect: (regionId: string) => void;
  isLoading?: boolean;
}

export function RegionSelector({ 
  regions, 
  selectedRegionId, 
  onSelect, 
  isLoading 
}: RegionSelectorProps) {
  const selectedRegion = regions.find(r => r.id === selectedRegionId);

  return (
    <motion.div 
      className="space-y-2"
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ delay: 0.1 }}
    >
      <div className="flex items-center gap-2">
        <MapPin className="h-4 w-4 text-primary" />
        <label className="font-mono text-xs uppercase tracking-wider text-muted-foreground">
          Target Region
        </label>
      </div>
      
      <Select value={selectedRegionId} onValueChange={onSelect} disabled={isLoading}>
        <SelectTrigger className="glass-panel border-primary/30 bg-secondary/50 hover:border-primary/60 focus:ring-primary/30">
          <SelectValue placeholder="Select region..." />
        </SelectTrigger>
        <SelectContent className="glass-panel border-primary/30">
          {regions.map((region) => (
            <SelectItem 
              key={region.id} 
              value={region.id}
              className="cursor-pointer hover:bg-primary/10 focus:bg-primary/10"
            >
              <span className="font-medium">{region.name}</span>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      {selectedRegion && (
        <p className="text-xs text-muted-foreground italic">
          {selectedRegion.description}
        </p>
      )}
    </motion.div>
  );
}
