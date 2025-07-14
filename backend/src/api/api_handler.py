from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Any
from datetime import datetime
import os
import sys

# Import the shared analysis function from the analysis module
from ..analysis import perform_ndvi_analysis

router = APIRouter()

def validate_date_format(date_string: str, field_name: str) -> None:
    """
    Validate date format and raise HTTPException if invalid.
    
    Args:
        date_string: Date string to validate
        field_name: Name of the field for error messages
    
    Raises:
        HTTPException: If date format is invalid
    """
    try:
        datetime.fromisoformat(date_string)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {field_name} format. Use YYYY-MM-DD format."
        )

def validate_bbox(min_lon: float, min_lat: float, max_lon: float, max_lat: float) -> None:
    """
    Validate bounding box coordinates.
    
    Args:
        min_lon: Minimum longitude
        min_lat: Minimum latitude
        max_lon: Maximum longitude
        max_lat: Maximum latitude
    
    Raises:
        HTTPException: If coordinates are invalid
    """
    # Validate coordinates order
    if min_lon >= max_lon or min_lat >= max_lat:
        raise HTTPException(
            status_code=400, 
            detail="Invalid bounding box: min coordinates must be less than max coordinates"
        )
    
    # Validate longitude range
    if not (-180 <= min_lon <= 180 and -180 <= max_lon <= 180):
        raise HTTPException(
            status_code=400,
            detail="Longitude values must be between -180 and 180"
        )
    
    # Validate latitude range
    if not (-90 <= min_lat <= 90 and -90 <= max_lat <= 90):
        raise HTTPException(
            status_code=400,
            detail="Latitude values must be between -90 and 90"
        )

@router.get("/search")
async def search_satellite_data(
    start_date: str = Query(..., description="Start date in ISO format (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date in ISO format (YYYY-MM-DD)"),
    min_lon: float = Query(..., description="Minimum longitude"),
    min_lat: float = Query(..., description="Minimum latitude"), 
    max_lon: float = Query(..., description="Maximum longitude"),
    max_lat: float = Query(..., description="Maximum latitude"),
    max_cloud_cover: int = Query(20, description="Maximum cloud cover percentage (0-100)", ge=0, le=100),
    max_size: int = Query(1024, description="Maximum size for raster processing", gt=0)
) -> Dict[str, Any]:
    """
    Search for satellite imagery and perform complete NDVI analysis.
    
    Args:
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)
        min_lon: Minimum longitude (-180 to 180)
        min_lat: Minimum latitude (-90 to 90)
        max_lon: Maximum longitude (-180 to 180)
        max_lat: Maximum latitude (-90 to 90)
        max_cloud_cover: Maximum cloud cover percentage (0-100)
        max_size: Maximum size for raster processing
    
    Returns:
        Dict containing analysis results and metadata
    
    Raises:
        HTTPException: If validation fails or analysis encounters errors
    """
    
    # Validate date formats
    validate_date_format(start_date, "start_date")
    validate_date_format(end_date, "end_date")
    
    # Validate date order
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)
    
    if start_dt >= end_dt:
        raise HTTPException(
            status_code=400,
            detail="start_date must be before end_date"
        )
    
    # Validate bounding box
    validate_bbox(min_lon, min_lat, max_lon, max_lat)
    
    # Construct bbox array from individual coordinates
    bbox = [min_lon, min_lat, max_lon, max_lat]
    
    try:
        # Perform the analysis using the shared function from main.py
        analysis_results = perform_ndvi_analysis(
            bbox=bbox,
            start_date=start_date,
            end_date=end_date,
            max_cloud_cover=max_cloud_cover,
            max_size=max_size
        )
        
        # Return structured API response
        return {
            "status": "success",
            "query": {
                "start_date": start_date,
                "end_date": end_date,
                "bbox": bbox,
                "max_cloud_cover": max_cloud_cover,
                "max_size": max_size
            },
            "analysis": analysis_results
        }
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )