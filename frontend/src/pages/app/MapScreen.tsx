import { Sidebar } from "../../components";
import MapView from "../../components/map/MapView";
import Widget from "../../components/map/Widget";

const MapScreen = () => {
  return (
    <div className="flex map-screen-container h-full w-full">
      <Widget />
      <Sidebar />
      <MapView />
    </div>
  );
};

export default MapScreen;
