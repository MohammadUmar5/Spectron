import { MapContainer, TileLayer } from "react-leaflet";

import "leaflet/dist/leaflet.css";
import "leaflet-control-geocoder";
import "leaflet-control-geocoder/dist/Control.Geocoder.css";
import "leaflet-draw";
import "leaflet-draw/dist/leaflet.draw.css";

import SearchControl from "./SearchControl";
import DrawControl from "./DrawControl";

const MapView = () => {
  const handleAOICreated = (geojson: any) => {
    console.log("geojson:", geojson);
  };

  return (
    <MapContainer center={[28.6139, 77.209]} zoom={6}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="© OpenStreetMap contributors"
      />
      <SearchControl />
      <DrawControl onCreated={handleAOICreated} />
    </MapContainer>
  );
};

export default MapView;
