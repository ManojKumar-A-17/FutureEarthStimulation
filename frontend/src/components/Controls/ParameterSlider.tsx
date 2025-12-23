import { motion } from 'framer-motion';
import { Slider } from '@/components/ui/slider';
import { cn } from '@/lib/utils';

interface ParameterSliderProps {
  label: string;
  icon: React.ReactNode;
  value: number;
  min: number;
  max: number;
  step: number;
  unit: string;
  onChange: (value: number) => void;
  colorScheme?: 'default' | 'temperature' | 'rainfall' | 'urban';
  delay?: number;
}

function getValueColor(value: number, min: number, max: number, scheme: string): string {
  const normalized = (value - min) / (max - min);
  
  switch (scheme) {
    case 'temperature':
      if (value <= 0) return 'text-cyan-400';
      if (value <= 2) return 'text-yellow-400';
      return 'text-orange-400';
    case 'rainfall':
      if (value >= 0) return 'text-emerald-400';
      if (value >= -25) return 'text-yellow-400';
      return 'text-red-400';
    case 'urban':
      if (value <= 30) return 'text-emerald-400';
      if (value <= 60) return 'text-yellow-400';
      return 'text-orange-400';
    default:
      return 'text-primary';
  }
}

export function ParameterSlider({
  label,
  icon,
  value,
  min,
  max,
  step,
  unit,
  onChange,
  colorScheme = 'default',
  delay = 0,
}: ParameterSliderProps) {
  const valueColor = getValueColor(value, min, max, colorScheme);
  
  const formatValue = (v: number) => {
    if (v > 0 && (colorScheme === 'temperature' || colorScheme === 'rainfall')) {
      return `+${v}`;
    }
    return v.toString();
  };

  return (
    <motion.div 
      className="space-y-3"
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ delay }}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-primary">{icon}</span>
          <label className="font-mono text-xs uppercase tracking-wider text-muted-foreground">
            {label}
          </label>
        </div>
        <div className={cn(
          "font-mono text-lg font-bold tabular-nums",
          valueColor
        )}>
          {formatValue(value)}{unit}
        </div>
      </div>

      <div className="relative">
        <div className="absolute -bottom-4 flex w-full justify-between text-[10px] text-muted-foreground/60">
          <span>{min}{unit}</span>
          <span>{max}{unit}</span>
        </div>
        <Slider
          value={[value]}
          onValueChange={([v]) => onChange(v)}
          min={min}
          max={max}
          step={step}
          className="cursor-pointer"
        />
      </div>
    </motion.div>
  );
}
