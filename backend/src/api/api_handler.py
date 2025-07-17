from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Any, Literal
from datetime import datetime
import os
import sys

# Import the shared analysis function from the analysis module
from ..analysis import perform_ndvi_analysis

router = APIRouter()

@router.get("/search")
async def search_satellite_data(
    start_date: str = Query(..., description="Start date in ISO format (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date in ISO format (YYYY-MM-DD)"),
    min_lon: float = Query(..., description="Minimum longitude"),
    min_lat: float = Query(..., description="Minimum latitude"), 
    max_lon: float = Query(..., description="Maximum longitude"),
    max_lat: float = Query(..., description="Maximum latitude"),
    max_cloud_cover: int = Query(20, description="Maximum cloud cover percentage (0-100)", ge=0, le=100),
    max_size: int = Query(1024, description="Maximum size for raster processing", gt=0),
    selection_mode: Literal["smart", "exact", "quality"] = Query(
        "smart", 
        description="Image selection strategy: 'smart' (seasonal matching), 'exact' (closest to dates), 'quality' (best available)"
    ),
    max_date_deviation_days: int = Query(
        30, 
        description="Maximum days deviation from requested dates (only used with 'exact' mode)", 
        ge=0
    )
) -> Dict[str, Any]:
    """
    Search for satellite imagery and perform complete NDVI analysis.
    
    Selection modes:
    - 'smart': Finds images from same season/month for long-term analysis (default)
    - 'exact': Finds images closest to your exact start/end dates
    - 'quality': Finds best quality images regardless of seasonal matching
    
    Args:
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)
        min_lon: Minimum longitude (-180 to 180)
        min_lat: Minimum latitude (-90 to 90)
        max_lon: Maximum longitude (-180 to 180)
        max_lat: Maximum latitude (-90 to 90)
        max_cloud_cover: Maximum cloud cover percentage (0-100)
        max_size: Maximum size for raster processing
        selection_mode: Strategy for selecting images
        max_date_deviation_days: Maximum allowed deviation from requested dates (exact mode only)
    
    Returns:
        Dict containing analysis results, metadata, and selection rationale
    """
    
    # ... existing validation code ...
    
    # Construct bbox array from individual coordinates
    bbox = [min_lon, min_lat, max_lon, max_lat]
    
    try:
        # Perform the analysis using the enhanced function
        analysis_results = perform_ndvi_analysis(
            bbox=bbox,
            start_date=start_date,
            end_date=end_date,
            max_cloud_cover=max_cloud_cover,
            max_size=max_size,
            selection_mode=selection_mode,
            max_date_deviation_days=max_date_deviation_days
        )
        
        # Enhanced response with selection rationale
        return {
            "status": "success",
            "query": {
                "start_date": start_date,
                "end_date": end_date,
                "bbox": bbox,
                "max_cloud_cover": max_cloud_cover,
                "max_size": max_size,
                "selection_mode": selection_mode
            },
            "selection_rationale": {
                "mode_used": selection_mode,
                "requested_dates": [start_date, end_date],
                "selected_dates": [
                    analysis_results["early_image"]["datetime"][:10],
                    analysis_results["late_image"]["datetime"][:10]
                ],
                "date_deviations_days": analysis_results.get("date_deviations", [0, 0]),
                "reason": analysis_results.get("selection_reason", "Smart seasonal matching applied")
            },
            "analysis": analysis_results
        }
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )