import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface StressIndicatorProps {
  value: number;
  label: string;
  showLabel?: boolean;
}

function getStressLevel(value: number): { 
  level: string; 
  color: string; 
  bgColor: string;
} {
  if (value <= 0.3) return { level: 'LOW', color: 'text-stress-low', bgColor: 'bg-stress-low' };
  if (value <= 0.6) return { level: 'MEDIUM', color: 'text-stress-medium', bgColor: 'bg-stress-medium' };
  if (value <= 0.8) return { level: 'HIGH', color: 'text-stress-high', bgColor: 'bg-stress-high' };
  return { level: 'SEVERE', color: 'text-stress-severe', bgColor: 'bg-stress-severe' };
}

export function StressIndicator({ value, label, showLabel = true }: StressIndicatorProps) {
  const { level, color, bgColor } = getStressLevel(value);
  const percentage = Math.round(value * 100);

  return (
    <div className="space-y-2">
      {showLabel && (
        <div className="flex items-center justify-between">
          <span className="font-mono text-xs uppercase tracking-wider text-muted-foreground">
            {label}
          </span>
          <span className={cn("font-mono text-sm font-bold", color)}>
            {percentage}%
          </span>
        </div>
      )}
      
      <div className="relative h-2 overflow-hidden rounded-full bg-secondary">
        <motion.div
          className={cn("absolute inset-y-0 left-0 rounded-full", bgColor)}
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        />
        <div className="absolute inset-0 stress-gradient opacity-20" />
      </div>

      {showLabel && (
        <div className="flex justify-end">
          <span className={cn(
            "rounded px-2 py-0.5 font-mono text-[10px] font-bold uppercase",
            bgColor,
            "text-background"
          )}>
            {level}
          </span>
        </div>
      )}
    </div>
  );
}
