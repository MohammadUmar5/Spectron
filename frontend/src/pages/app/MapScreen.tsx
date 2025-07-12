import MapView from "../../components/map/MapView";
import SideBar from "../../components/map/SideBar";

const MapScreen = () => {
  return (
    <div className="flex map-screen-container h-full w-full">
      <SideBar />
      <MapView />
    </div>
  );
};

export default MapScreen;
