import { useState } from 'react';
import { motion } from 'framer-motion';
import { Check, ChevronsUpDown, MapPin, Search } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
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
  const [open, setOpen] = useState(false);
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

      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="w-full justify-between border-primary/30 bg-secondary/50 hover:bg-secondary/80 focus:ring-primary/30"
            disabled={isLoading}
          >
            {selectedRegion ? selectedRegion.name : "Select region..."}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[300px] p-0 glass-panel border-primary/30" align="start">
          <Command>
            <CommandInput placeholder="Search country or region..." />
            <CommandList>
              <CommandEmpty>No region found.</CommandEmpty>
              <CommandGroup>
                {regions.map((region) => (
                  <CommandItem
                    key={region.id}
                    value={region.name}
                    onSelect={() => {
                      onSelect(region.id);
                      setOpen(false);
                    }}
                    className="cursor-pointer hover:bg-primary/10 aria-selected:bg-primary/10"
                  >
                    <Check
                      className={cn(
                        "mr-2 h-4 w-4",
                        selectedRegionId === region.id ? "opacity-100" : "opacity-0"
                      )}
                    />
                    {region.name}
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>

      {selectedRegion && (
        <p className="text-xs text-muted-foreground italic">
          {selectedRegion.description}
        </p>
      )}
    </motion.div>
  );
}
