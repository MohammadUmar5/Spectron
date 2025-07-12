import { useMap } from "react-leaflet";
import { useEffect } from "react";
import L from "leaflet";
const SearchControl = (): null => {
  const map = useMap();
  useEffect(() => {
    const geocoder = L.Control.geocoder({
      defaultMarkGeocode: true,
      placeholder: "Search..",
    }).addTo(map);
    return () => {
      map.removeControl(geocoder);
    };
  }, [map]);
  return null;
};

export default SearchControl;
