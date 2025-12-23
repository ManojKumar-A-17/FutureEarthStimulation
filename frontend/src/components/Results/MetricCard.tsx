import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface MetricCardProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  unit?: string;
  trend?: 'positive' | 'negative' | 'neutral';
  delay?: number;
}

export function MetricCard({ 
  icon, 
  label, 
  value, 
  unit = '', 
  trend = 'neutral',
  delay = 0 
}: MetricCardProps) {
  const trendColors = {
    positive: 'text-stress-low border-stress-low/30',
    negative: 'text-stress-severe border-stress-severe/30',
    neutral: 'text-primary border-primary/30',
  };

  const numValue = typeof value === 'number' ? value : parseFloat(value);
  const displayValue = !isNaN(numValue) 
    ? numValue > 0 && trend !== 'neutral' 
      ? `+${numValue.toFixed(1)}` 
      : numValue.toFixed(1)
    : value;

  return (
    <motion.div
      className={cn(
        "glass-panel rounded-lg border-l-2 p-4 transition-all hover:bg-card/90",
        trendColors[trend]
      )}
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ delay, duration: 0.3 }}
    >
      <div className="flex items-start justify-between">
        <div className="rounded-md bg-secondary/50 p-2 text-muted-foreground">
          {icon}
        </div>
      </div>
      
      <div className="mt-3">
        <p className="font-mono text-xs uppercase tracking-wider text-muted-foreground">
          {label}
        </p>
        <p className={cn(
          "mt-1 font-mono text-2xl font-bold tabular-nums",
          trendColors[trend].split(' ')[0]
        )}>
          {displayValue}
          <span className="ml-1 text-sm font-normal text-muted-foreground">{unit}</span>
        </p>
      </div>
    </motion.div>
  );
}
