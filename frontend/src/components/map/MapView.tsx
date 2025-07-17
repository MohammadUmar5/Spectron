import { useRef } from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import type { Map as LeafletMap } from "leaflet";

import "leaflet/dist/leaflet.css";
import "leaflet-control-geocoder";
import "leaflet-control-geocoder/dist/Control.Geocoder.css";
import "leaflet-draw";
import "leaflet-draw/dist/leaflet.draw.css";

import SearchControl from "./SearchControl";
import DrawControl from "./DrawControl";

type MapViewProps = {
  onBoxDrawn: (box: [number, number, number, number]) => void;
};

const MapView = ({ onBoxDrawn }: MapViewProps) => {
  const mapRef = useRef<LeafletMap | null>(null);

  const handleAOICreated = (geojson: any) => {
    const coords = geojson.geometry.coordinates[0]; // outer ring of polygon
    const lons = coords.map((c: number[]) => c[0]);
    const lats = coords.map((c: number[]) => c[1]);

    const minLon = Math.min(...lons);
    const maxLon = Math.max(...lons);
    const minLat = Math.min(...lats);
    const maxLat = Math.max(...lats);

    // Prevent invalid (point or flat line) bounding boxes
    if (minLon === maxLon || minLat === maxLat) {
      alert("Please draw a valid area (not just a dot or a line).");
      return;
    }

    // Zoom into the drawn bounding box
    if (mapRef.current) {
      mapRef.current.fitBounds([
        [minLat, minLon],
        [maxLat, maxLon],
      ]);
    }

    onBoxDrawn([minLon, minLat, maxLon, maxLat]);
  };

  return (
    <div className="w-full h-full relative">
      <MapContainer
        center={[28.6139, 77.209]} // New Delhi
        zoom={6}
        className="w-full h-[calc(100vh-50px)] rounded-md z-0"
        whenCreated={(mapInstance) => {
          mapRef.current = mapInstance;
        }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="© OpenStreetMap contributors"
        />
        <SearchControl onLocationSelected={onBoxDrawn} />
        <DrawControl onCreated={handleAOICreated} />
      </MapContainer>
    </div>
  );
};

export default MapView;
