import { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import type {
  Map as LeafletMap,
  Rectangle,
  TileLayer,
  LayerGroup,
} from 'leaflet';
import type { Region } from '@/types/simulation';

interface MapViewProps {
  selectedRegion: Region | null;
}

export function MapView({ selectedRegion }: MapViewProps) {
  const mapRef = useRef<LeafletMap | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const rectangleRef = useRef<Rectangle | null>(null);

  const [isMapReady, setIsMapReady] = useState(false);

  /* ---------------- MAP INITIALIZATION ---------------- */
  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const initMap = async () => {
      const L = await import('leaflet');
      await import('leaflet/dist/leaflet.css');

      const map = L.map(containerRef.current!, {
        center: [20.5937, 78.9629], // India
        zoom: 5,
        zoomControl: true,
      });

      /* ---------- BASE MAPS ---------- */

      // 1️⃣ Dark map (labels included)
      const darkMap = L.tileLayer(
        'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        { attribution: '&copy; CARTO' }
      );

      // 2️⃣ Street / Light map
      const streetMap = L.tileLayer(
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        { attribution: '&copy; OpenStreetMap contributors' }
      );

      // 3️⃣ Satellite imagery
      const satelliteBase = L.tileLayer(
        'https://server.arcgisonline.com/ArcGIS/rest/services/' +
          'World_Imagery/MapServer/tile/{z}/{y}/{x}',
        { attribution: '&copy; Esri' }
      );

      // Satellite labels overlay
      const satelliteLabels = L.tileLayer(
        'https://services.arcgisonline.com/ArcGIS/rest/services/' +
          'Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
        { attribution: '&copy; Esri', opacity: 0.9 }
      );

      const satelliteMap = L.layerGroup([
        satelliteBase,
        satelliteLabels,
      ]);

      // 4️⃣ Weather (rain overlay on dark map)
      const weatherApiKey = import.meta.env.VITE_OPENWEATHER_API_KEY;

      const weatherOverlay = weatherApiKey
        ? L.tileLayer(
            `https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=${weatherApiKey}`,
            { opacity: 0.6 }
          )
        : null;

      const weatherMap: LayerGroup | null = weatherOverlay
        ? L.layerGroup([darkMap, weatherOverlay])
        : null;

      /* ---------- DEFAULT MAP ---------- */
      darkMap.addTo(map);

      /* ---------- LAYER CONTROL ---------- */
      L.control
        .layers(
          {
            'Dark Map': darkMap,
            'Street Map': streetMap,
            'Satellite (Labeled)': satelliteMap,
            ...(weatherMap ? { 'Weather (Rain)': weatherMap } : {}),
          },
          {},
          { position: 'topright' }
        )
        .addTo(map);

      mapRef.current = map;
      setIsMapReady(true);
    };

    initMap();

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  /* ---------------- REGION HIGHLIGHT ---------------- */
  useEffect(() => {
    if (!mapRef.current || !isMapReady || !selectedRegion) return;

    const updateRegion = async () => {
      const L = await import('leaflet');

      if (rectangleRef.current) {
        mapRef.current!.removeLayer(rectangleRef.current);
      }

      const bounds = L.latLngBounds(
        [selectedRegion.bbox[1], selectedRegion.bbox[0]],
        [selectedRegion.bbox[3], selectedRegion.bbox[2]]
      );

      rectangleRef.current = L.rectangle(bounds, {
        color: 'hsl(174, 72%, 56%)',
        weight: 2,
        dashArray: '8,4',
        fillOpacity: 0.12,
      }).addTo(mapRef.current!);

      mapRef.current!.flyToBounds(bounds, {
        padding: [20, 20],
        duration: 1.5,
      });
    };

    updateRegion();
  }, [selectedRegion, isMapReady]);

  /* ---------------- UI ---------------- */
  return (
    <motion.div
      className="relative h-full w-full overflow-hidden rounded-lg border border-border/30"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <div ref={containerRef} className="h-full w-full" />

      {!isMapReady && (
        <div className="absolute inset-0 flex items-center justify-center bg-card/80">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
        </div>
      )}

      {selectedRegion && (
        <div className="absolute bottom-4 left-4 rounded-md bg-background/80 px-3 py-2 backdrop-blur">
          <span className="text-xs text-muted-foreground">REGION //</span>
          <span className="ml-2 font-semibold text-primary">
            {selectedRegion.name}
          </span>
        </div>
      )}
    </motion.div>
  );
}
