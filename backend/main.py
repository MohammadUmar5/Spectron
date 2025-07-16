from src.aoi import get_bbox
from src.analysis import perform_ndvi_analysis
from fastapi import FastAPI
from src.api.api_handler import router as search_router
import uvicorn

app = FastAPI(title="Satellite Data API", version="1.0.0")

# Include the search router
app.include_router(search_router, prefix="/api", tags=["search"])

@app.get("/")
async def root():
    return {"message": "Satellite Data API is running"}

def main():
    """Main function for command-line execution."""
    # Configuration - modify these for your analysis
    bbox = get_bbox()
    
    # Example configuration for year-long gap (seasonal analysis)
    start_date = "2022-06-01"
    end_date = "2024-06-30"
    
    max_cloud_cover = 15  # Stricter cloud cover for better results
    
    try:
        results = perform_ndvi_analysis(bbox, start_date, end_date, max_cloud_cover)
        return results
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        print("Suggestions:")
        print("  - Try increasing max_cloud_cover")
        print("  - Expand the date range")
        print("  - Choose a different AOI")
        raise

if __name__ == "__main__":
    # main()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)