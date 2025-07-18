"""
Enhanced NDVI Analysis Module with Multiple Selection Strategies
"""

from datetime import datetime, timedelta
from .search import search_items
from .download import get_band_urls
from .fetch import read_band_with_retry
from .ndvi import compute_ndvi, diff_ndvi
from .visualize import create_ndvi_diff_image, create_individual_ndvi_image, create_composite_image
from .database.database import db_handler


def find_best_image_pair(bbox, start_date, end_date, max_cloud_cover=20, 
                        selection_mode="smart", max_date_deviation_days=30):
    """
    Find the best pair of images using different selection strategies.
    
    Args:
        bbox: Bounding box coordinates
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        max_cloud_cover: Maximum acceptable cloud cover percentage
        selection_mode: 'smart', 'exact', or 'quality'
        max_date_deviation_days: Maximum deviation from requested dates (exact mode only)
    
    Returns:
        tuple: (early_image, late_image, selection_info)
    """
    print(f"Searching for images between {start_date} and {end_date}")
    print(f"Selection mode: {selection_mode}")
    
    # Search for all images in the time period
    all_items = search_items(start_date, end_date, bbox)
    print(f"Found {len(all_items)} total images")
    
    # Filter by cloud cover
    good_items = [item for item in all_items 
                  if item.properties.get('eo:cloud_cover', 100) <= max_cloud_cover]
    print(f"Found {len(good_items)} images with cloud cover <= {max_cloud_cover}%")
    
    if len(good_items) < 2:
        raise Exception(f"Not enough good quality images found. Try increasing max_cloud_cover or expanding date range.")
    
    # Sort by date
    good_items.sort(key=lambda x: x.datetime)
    
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)
    
    selection_info = {
        "mode": selection_mode,
        "total_images": len(all_items),
        "good_quality_images": len(good_items),
        "reason": ""
    }
    
    if selection_mode == "exact":
        # Find images closest to exact requested dates
        early_image = min(good_items, 
                         key=lambda x: abs((x.datetime.date() - start_dt.date()).days))
        late_image = min(good_items, 
                        key=lambda x: abs((x.datetime.date() - end_dt.date()).days))
        
        # Check if deviations are within acceptable range
        early_deviation = abs((early_image.datetime.date() - start_dt.date()).days)
        late_deviation = abs((late_image.datetime.date() - end_dt.date()).days)
        
        if early_deviation > max_date_deviation_days or late_deviation > max_date_deviation_days:
            raise Exception(f"No images found within {max_date_deviation_days} days of requested dates. "
                          f"Closest images are {early_deviation} and {late_deviation} days away.")
        
        selection_info["reason"] = f"Closest images to requested dates (±{early_deviation}/{late_deviation} days)"
        selection_info["date_deviations"] = [early_deviation, late_deviation]
        
        print(f"Selected exact date match: {early_image.datetime.strftime('%Y-%m-%d')} and {late_image.datetime.strftime('%Y-%m-%d')}")
        
    elif selection_mode == "quality":
        # Find best quality images regardless of seasonal matching
        early_image = good_items[0]  # Already sorted by cloud cover
        late_image = good_items[-1]  # Last chronologically
        
        selection_info["reason"] = "Best quality images selected (lowest cloud cover)"
        selection_info["date_deviations"] = [0, 0]  # Not applicable for quality mode
        
        print(f"Selected best quality images: {early_image.datetime.strftime('%Y-%m-%d')} and {late_image.datetime.strftime('%Y-%m-%d')}")
        
    else:  # selection_mode == "smart" (default)
        # Original smart seasonal matching logic
        time_span_days = (end_dt - start_dt).days
        
        if time_span_days > 300:  # More than 10 months
            target_month = start_dt.month
            
            # Find early image close to target month
            early_candidates = [item for item in good_items 
                              if abs(item.datetime.month - target_month) <= 1]
            
            # Find late image close to target month
            late_candidates = [item for item in good_items 
                             if abs(item.datetime.month - target_month) <= 1 and 
                             item.datetime.year > start_dt.year]
            
            if early_candidates and late_candidates:
                early_image = early_candidates[0]
                late_image = late_candidates[-1]
                selection_info["reason"] = f"Seasonal matching applied (target month: {target_month})"
                print(f"Selected seasonal match: {early_image.datetime.strftime('%Y-%m-%d')} and {late_image.datetime.strftime('%Y-%m-%d')}")
            else:
                # Fallback to first and last good images
                early_image = good_items[0]
                late_image = good_items[-1]
                selection_info["reason"] = "Fallback to first and last good quality images"
                print(f"Using first and last good images: {early_image.datetime.strftime('%Y-%m-%d')} and {late_image.datetime.strftime('%Y-%m-%d')}")
        else:
            # For shorter periods, just use first and last
            early_image = good_items[0]
            late_image = good_items[-1]
            selection_info["reason"] = "Short time period - using first and last good quality images"
            print(f"Using first and last images: {early_image.datetime.strftime('%Y-%m-%d')} and {late_image.datetime.strftime('%Y-%m-%d')}")
        
        selection_info["date_deviations"] = [0, 0]  # Not tracked for smart mode
    
    return early_image, late_image, selection_info


def perform_ndvi_analysis(bbox, start_date, end_date, max_cloud_cover=15, max_size=1024, 
                         selection_mode="smart", max_date_deviation_days=30):
    """
    Perform complete NDVI analysis workflow with enhanced selection options.
    
    Args:
        bbox: Bounding box coordinates
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        max_cloud_cover: Maximum acceptable cloud cover percentage
        max_size: Maximum size for raster data processing
        selection_mode: Image selection strategy ('smart', 'exact', 'quality')
        max_date_deviation_days: Maximum deviation from requested dates (exact mode only)
    
    Returns:
        dict: Analysis results including selection rationale
    """
    print(f"Processing area: {bbox}")
    print(f"Date range: {start_date} to {end_date}")
    print(f"Maximum cloud cover: {max_cloud_cover}%")
    print(f"Selection mode: {selection_mode}")
    
    # Step 1: Find best image pair with enhanced selection
    print("\n=== STEP 1: FINDING BEST IMAGE PAIR ===")
    early_item, late_item, selection_info = find_best_image_pair(
        bbox, start_date, end_date, max_cloud_cover, 
        selection_mode, max_date_deviation_days
    )
    
    print(f"\nSelected images:")
    print(f"  Early: {early_item.datetime.strftime('%Y-%m-%d')} (Cloud: {early_item.properties.get('eo:cloud_cover', 'N/A'):.1f}%)")
    print(f"  Late:  {late_item.datetime.strftime('%Y-%m-%d')} (Cloud: {late_item.properties.get('eo:cloud_cover', 'N/A'):.1f}%)")
    print(f"  Selection reason: {selection_info['reason']}")
    
    time_gap = (late_item.datetime - early_item.datetime).days
    print(f"  Time gap: {time_gap} days ({time_gap/365.25:.1f} years)")
    
    # ... rest of the analysis remains the same ...
    
    # Step 2: Get URLs
    print("\n=== STEP 2: GETTING SIGNED URLS ===")
    items = [early_item, late_item]
    urls = get_band_urls(items)
    
    # Step 3: Load bands
    print("\n=== STEP 3: DOWNLOADING RASTER DATA ===")
    print("This may take several minutes...")
    
    print("\n[1/4] Reading B04 (Red) from early image...")
    b04_1, _ = read_band_with_retry(urls[0]["B04"], max_size=max_size)
    
    print("\n[2/4] Reading B08 (NIR) from early image...")
    b08_1, _ = read_band_with_retry(urls[0]["B08"], max_size=max_size)
    
    print("\n[3/4] Reading B04 (Red) from late image...")
    b04_2, _ = read_band_with_retry(urls[1]["B04"], max_size=max_size)
    
    print("\n[4/4] Reading B08 (NIR) from late image...")
    b08_2, _ = read_band_with_retry(urls[1]["B08"], max_size=max_size)
    
    # Step 4: NDVI Computation
    print("\n=== STEP 4: COMPUTING NDVI ===")
    ndvi1 = compute_ndvi(b04_1, b08_1)
    ndvi2 = compute_ndvi(b04_2, b08_2)
    
    print(f"Early NDVI range: {ndvi1.min():.3f} to {ndvi1.max():.3f}")
    print(f"Late NDVI range: {ndvi2.min():.3f} to {ndvi2.max():.3f}")
    
    diff = diff_ndvi(ndvi1, ndvi2)
    print(f"NDVI difference range: {diff.min():.3f} to {diff.max():.3f}")
    
    # Step 5: Create visualizations and save to database
    print("\n=== STEP 5: CREATING VISUALIZATIONS AND SAVING TO DATABASE ===")
    
    early_date = early_item.datetime.strftime('%Y-%m-%d')
    late_date = late_item.datetime.strftime('%Y-%m-%d')
    
    # Create image bytes for database storage
    early_image_bytes = create_individual_ndvi_image(ndvi1, "Early NDVI")
    late_image_bytes = create_individual_ndvi_image(ndvi2, "Late NDVI")
    diff_image_bytes = create_ndvi_diff_image(diff)
    
    # Prepare metadata for database
    early_image_data = {
        "id": early_item.id,
        "datetime": str(early_item.datetime),
        "cloud_cover": early_item.properties.get("eo:cloud_cover"),
        "platform": early_item.properties.get("platform"),
        "instruments": early_item.properties.get("instruments")
    }
    
    late_image_data = {
        "id": late_item.id,
        "datetime": str(late_item.datetime),
        "cloud_cover": late_item.properties.get("eo:cloud_cover"),
        "platform": late_item.properties.get("platform"),
        "instruments": late_item.properties.get("instruments")
    }
    
    analysis_results = {
        "time_gap_days": time_gap,
        "mean_ndvi_change": float(diff.mean()),
        "max_vegetation_loss": float(diff.min()),
        "max_vegetation_gain": float(diff.max()),
        "ndvi_statistics": {
            "early": {
                "min": float(ndvi1.min()),
                "max": float(ndvi1.max()),
                "mean": float(ndvi1.mean()),
                "std": float(ndvi1.std())
            },
            "late": {
                "min": float(ndvi2.min()),
                "max": float(ndvi2.max()),
                "mean": float(ndvi2.mean()),
                "std": float(ndvi2.std())
            },
            "difference": {
                "min": float(diff.min()),
                "max": float(diff.max()),
                "mean": float(diff.mean()),
                "std": float(diff.std())
            }
        },
        "selection_info": selection_info
    }
    
    # Save to database
    analysis_id = db_handler.save_analysis_results(
        bbox=bbox,
        start_date=start_date,
        end_date=end_date,
        selection_mode=selection_mode,
        early_image_data=early_image_data,
        late_image_data=late_image_data,
        analysis_results=analysis_results,
        early_ndvi_image=early_image_bytes,
        late_ndvi_image=late_image_bytes,
        difference_image=diff_image_bytes
    )
    
    print(f"\nAll visualizations saved to database with analysis ID: {analysis_id}")
    print(f"  Early NDVI image: {len(early_image_bytes)} bytes")
    print(f"  Late NDVI image: {len(late_image_bytes)} bytes")
    print(f"  Difference image: {len(diff_image_bytes)} bytes")
    
    print(f"\nAnalysis complete! 🎉")
    print(f"Time period analyzed: {time_gap} days")
    print(f"Mean NDVI change: {diff.mean():.4f}")
    print(f"Max vegetation loss: {diff.min():.4f}")
    print(f"Max vegetation gain: {diff.max():.4f}")
    
    return {
        "analysis_id": analysis_id,
        "time_gap_days": time_gap,
        "mean_ndvi_change": float(diff.mean()),
        "max_vegetation_loss": float(diff.min()),
        "max_vegetation_gain": float(diff.max()),
        "early_image": {
            "id": early_item.id,
            "datetime": str(early_item.datetime),
            "cloud_cover": early_item.properties.get("eo:cloud_cover")
        },
        "late_image": {
            "id": late_item.id,
            "datetime": str(late_item.datetime),
            "cloud_cover": late_item.properties.get("eo:cloud_cover")
        },
        "database_stored": True,
        "selection_info": selection_info,
        "selection_reason": selection_info["reason"],
        "date_deviations": selection_info.get("date_deviations", [0, 0])
    }