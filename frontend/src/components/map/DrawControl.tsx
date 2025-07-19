import "leaflet-draw";
import L from "leaflet";
import { useEffect } from "react";
import { useMap } from "react-leaflet";
interface DrawControlProps {
  onCreated?: (geojson: GeoJSON.Feature) => void;
}

const DrawControl = ({ onCreated }: DrawControlProps) => {
  const map = useMap();
  useEffect(() => {
    const drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);
    const drawControl = new L.Control.Draw({
      draw: {
        polyline: false,
        circle: false,
        marker: false,
        circlemarker: false,
        polygon: {
          allowIntersection: false,
          showArea: true,
          shapeOptions: {
            color: "#e91e63",
          },
        },
      },
      edit: {
        featureGroup: drawnItems,
      },
    });
    map.addControl(drawControl);
    map.on(L.Draw.Event.CREATED, (e: any) => {
      const layer = e.layer;
      drawnItems.addLayer(layer);
      const geojson = layer.toGeoJSON();
      console.log("AOI:", geojson);
      onCreated?.(geojson);
    });
    return () => {
      map.off(L.Draw.Event.CREATED);
      map.removeControl(drawControl);
      map.removeLayer(drawnItems);
    };
  }, [map, onCreated]);
  return null;
};

export default DrawControl;
