import { useState } from "react";
import MapView from "../../components/map/MapView";
import Widget from "../../components/map/Widget";
import { fetchNDVIAnalysis } from "../../services/backend";

const Dashboard = () => {
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");
  const [box, setBox] = useState<[number, number, number, number] | null>(null);
  const [loading, setLoading] = useState(false);
  const [images, setImages] = useState<string[]>([]);
  const [mode, setMode] = useState<string>("Exact");
  const handleSubmit = async () => {
    if (!startDate || !endDate || !box) {
      alert("Please select dates and draw an area on the map.");
      return;
    }

    setLoading(true);
    setImages([]);
    //mode either exact/quality/smart
    console.log(mode);
    try {
      const result = await fetchNDVIAnalysis({
        start_date: startDate,
        end_date: endDate,
        min_lon: box[0],
        min_lat: box[1],
        max_lon: box[2],
        max_lat: box[3],
        max_size: 1024,
      });

      console.log("NDVI result:", result);

      // Let's assume result.analysis.image_urls = string[]
      const urls: string[] = result.analysis.image_urls ?? [];

      setImages(urls);
    } catch (err) {
      console.error("Error fetching NDVI:", err);
      alert("Failed to fetch NDVI data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full w-full">
      <div className="flex flex-1">
        <Widget
          startDate={startDate}
          endDate={endDate}
          setStartDate={setStartDate}
          setEndDate={setEndDate}
          onSubmit={handleSubmit}
          setMode={setMode}
          mode={mode}
        />
        <MapView onBoxDrawn={setBox} />
      </div>

      <div className="w-full p-4 bg-white border-t max-h-[40vh] overflow-y-auto">
        {loading ? (
          <div className="text-center text-accentColor font-semibold animate-pulse">
            🛰️ Fetching satellite imagery... please wait (~40 seconds)
          </div>
        ) : images.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {images.map((url, index) => (
              <div key={index} className="rounded overflow-hidden shadow-md">
                <img
                  src={url}
                  alt={`NDVI Image ${index + 1}`}
                  className="w-full object-cover"
                />
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center text-gray-500">
            No imagery loaded yet.
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
