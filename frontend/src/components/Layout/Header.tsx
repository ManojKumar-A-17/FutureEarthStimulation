import { motion } from 'framer-motion';
import { Globe2 } from 'lucide-react';

export function Header() {
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

        {/* Status Indicators  - REMOVED */}

      </div>

      {/* Decorative line */}
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent" />
    </motion.header>
  );
}
