const API_URL = "http://localhost:8000/api/search";

type NDVIQueryParams = {
  start_date: string;
  end_date: string;
  min_lon: number;
  min_lat: number;
  max_lon: number;
  max_lat: number;
  max_cloud_cover?: number;
  max_size?: number;
};

type NDVIResponse = {
  status: string;
  query: {
    start_date: string;
    end_date: string;
    bbox: [number, number, number, number];
    max_cloud_cover: number;
    max_size: number;
  };
  analysis: {
    [key: string]: unknown;
  };
};

export async function fetchNDVIAnalysis(params: NDVIQueryParams): Promise<NDVIResponse> {
  const {
    start_date,
    end_date,
    min_lon,
    min_lat,
    max_lon,
    max_lat,
    max_cloud_cover = 20,
    max_size = 1024,
  } = params;

  const query = new URLSearchParams({
    start_date,
    end_date,
    min_lon: min_lon.toString(),
    min_lat: min_lat.toString(),
    max_lon: max_lon.toString(),
    max_lat: max_lat.toString(),
    max_cloud_cover: max_cloud_cover.toString(),
    max_size: max_size.toString(),
  });

  try {
    const response = await fetch(`${API_URL}?${query.toString()}`, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      const errorBody = (await response.json()) as { detail?: string };
      const message = errorBody?.detail ?? "API request failed";
      throw new Error(message);
    }

    const data = (await response.json()) as NDVIResponse;
    return data;

  } catch (err) {
    if (err instanceof Error) {
      console.error("NDVI Analysis Error:", err.message);
      throw err;
    } else {
      throw new Error("Unknown error occurred");
    }
  }
}
