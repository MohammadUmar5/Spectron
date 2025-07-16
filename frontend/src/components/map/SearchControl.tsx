import { useMap } from "react-leaflet";
import { useEffect } from "react";
import L from "leaflet";

type Props = {
  onLocationSelected: (box: [number, number, number, number]) => void;
};

const SearchControl = ({ onLocationSelected }: Props): null => {
  const map = useMap();

  useEffect(() => {
    const geocoder = L.Control.geocoder({
      defaultMarkGeocode: true,
      placeholder: "Search...",
    })
      .on("markgeocode", function (e: any) {
        const bbox = e.geocode.bbox; // Leaflet LatLngBounds
        const southWest = bbox.getSouthWest();
        const northEast = bbox.getNorthEast();

        const minLat = southWest.lat;
        const minLon = southWest.lng;
        const maxLat = northEast.lat;
        const maxLon = northEast.lng;

        // Zoom to the selected location
        map.fitBounds(bbox);

        // Send the bounding box to parent
        onLocationSelected([minLon, minLat, maxLon, maxLat]);
      })
      .addTo(map);

    return () => {
      map.removeControl(geocoder);
    };
  }, [map, onLocationSelected]);

  return null;
};

export default SearchControl;
