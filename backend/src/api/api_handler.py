from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import Response
from typing import Dict, Any, Literal, List
from datetime import datetime
import os
import sys

# Import the shared analysis function from the analysis module
from ..analysis import perform_ndvi_analysis
from ..database.database import db_handler

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
        
        # Enhanced response with database integration
        return {
            "status": "success",
            "analysis_id": analysis_results["analysis_id"],
            "query": {
                "start_date": start_date,
                "end_date": end_date,
                "bbox": bbox,
                "max_cloud_cover": max_cloud_cover,
                "max_size": max_size,
                "selection_mode": selection_mode
            },
            "image_urls": {
                "early_ndvi": f"/api/analysis/{analysis_results['analysis_id']}/image/early",
                "late_ndvi": f"/api/analysis/{analysis_results['analysis_id']}/image/late",
                "difference": f"/api/analysis/{analysis_results['analysis_id']}/image/difference",
                "composite": f"/api/analysis/{analysis_results['analysis_id']}/image/composite"
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

@router.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: str) -> Dict[str, Any]:
    """
    Get analysis metadata by analysis ID.
    
    Args:
        analysis_id: The analysis ID to retrieve
        
    Returns:
        Dict containing analysis metadata
    """
    try:
        analysis_data = db_handler.get_analysis_results(analysis_id)
        
        if not analysis_data:
            raise HTTPException(status_code=404, detail=f"Analysis {analysis_id} not found")
        
        # Add image URLs to response
        analysis_data["image_urls"] = {
            "early_ndvi": f"/api/analysis/{analysis_id}/image/early",
            "late_ndvi": f"/api/analysis/{analysis_id}/image/late", 
            "difference": f"/api/analysis/{analysis_id}/image/difference",
            "composite": f"/api/analysis/{analysis_id}/image/composite"
        }
        
        return {
            "status": "success",
            "analysis": analysis_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving analysis {analysis_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analysis: {str(e)}")

@router.get("/analysis/{analysis_id}/image/{image_type}")
async def get_analysis_image(
    analysis_id: str,
    image_type: Literal["early", "late", "difference", "composite"]
):
    """
    Get analysis image by analysis ID and image type.
    
    Args:
        analysis_id: The analysis ID
        image_type: Type of image (early, late, difference, composite)
        
    Returns:
        PNG image as binary response
    """
    try:
        if image_type == "composite":
            # For composite images, we need to generate them on-demand
            # Get the analysis data first
            analysis_data = db_handler.get_analysis_results(analysis_id)
            if not analysis_data:
                raise HTTPException(status_code=404, detail=f"Analysis {analysis_id} not found")
            
            # Get individual images and create composite
            early_bytes = db_handler.get_image_data(analysis_id, "early")
            late_bytes = db_handler.get_image_data(analysis_id, "late") 
            diff_bytes = db_handler.get_image_data(analysis_id, "difference")
            
            if not all([early_bytes, late_bytes, diff_bytes]):
                raise HTTPException(status_code=404, detail="Required images not found for composite")
            
            # Note: For now, return difference image as placeholder
            # Full composite generation would require reconstructing NDVI arrays
            image_data = diff_bytes
        else:
            image_data = db_handler.get_image_data(analysis_id, image_type)
        
        if not image_data:
            raise HTTPException(
                status_code=404, 
                detail=f"Image {image_type} not found for analysis {analysis_id}"
            )
        
        return Response(
            content=image_data,
            media_type="image/png",
            headers={
                "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
                "Content-Disposition": f"inline; filename={analysis_id}_{image_type}.png"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving image {image_type} for analysis {analysis_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve image: {str(e)}")

@router.get("/analyses")
async def list_analyses(
    limit: int = Query(20, description="Maximum number of analyses to return", ge=1, le=100)
) -> Dict[str, Any]:
    """
    List recent analyses.
    
    Args:
        limit: Maximum number of results to return
        
    Returns:
        Dict containing list of analyses
    """
    try:
        analyses = db_handler.list_analyses(limit)
        
        # Add image URLs to each analysis
        for analysis in analyses:
            analysis_id = analysis["analysis_id"]
            analysis["image_urls"] = {
                "early_ndvi": f"/api/analysis/{analysis_id}/image/early",
                "late_ndvi": f"/api/analysis/{analysis_id}/image/late",
                "difference": f"/api/analysis/{analysis_id}/image/difference", 
                "composite": f"/api/analysis/{analysis_id}/image/composite"
            }
        
        return {
            "status": "success",
            "count": len(analyses),
            "analyses": analyses
        }
        
    except Exception as e:
        print(f"Error listing analyses: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list analyses: {str(e)}")