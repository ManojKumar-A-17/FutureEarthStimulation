import { motion } from 'framer-motion';
import { Globe2, Activity, Wifi, WifiOff } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface HeaderProps {
  isConnected: boolean;
  isCheckingHealth: boolean;
}

export function Header({ isConnected, isCheckingHealth }: HeaderProps) {
  return (
    <motion.header 
      className="relative z-50 border-b border-border/50 bg-background/80 backdrop-blur-lg"
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
    >
      <div className="flex items-center justify-between px-6 py-4">
        {/* Logo & Title */}
        <div className="flex items-center gap-4">
          <div className="relative">
            <Globe2 className="h-8 w-8 text-primary animate-pulse-glow" />
            <div className="absolute -right-1 -top-1 h-2 w-2 rounded-full bg-primary animate-pulse" />
          </div>
          
          <div>
            <h1 className="text-xl font-bold tracking-tight">
              <span className="text-gradient">Alternate Earth</span>
              <span className="ml-2 text-foreground">Futures</span>
            </h1>
            <p className="font-mono text-xs text-muted-foreground">
              Climate Scenario Simulator • Powered by Satellite Data
            </p>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="flex items-center gap-4">
          <Badge 
            variant="outline" 
            className={cn(
              "gap-2 transition-colors",
              isConnected 
                ? "border-stress-low/50 bg-stress-low/10 text-stress-low" 
                : "border-destructive/50 bg-destructive/10 text-destructive"
            )}
          >
            {isCheckingHealth ? (
              <Activity className="h-3 w-3 animate-pulse" />
            ) : isConnected ? (
              <Wifi className="h-3 w-3" />
            ) : (
              <WifiOff className="h-3 w-3" />
            )}
            {isConnected ? 'Backend Connected' : 'Backend Offline'}
          </Badge>
        </div>
      </div>

      {/* Decorative line */}
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent" />
    </motion.header>
  );
}
