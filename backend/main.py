from src.aoi import get_bbox
from src.search import search_items
from src.download import get_band_urls
from src.fetch import read_band_with_retry
from src.ndvi import compute_ndvi, diff_ndvi
from src.visualize import save_ndvi_diff, save_individual_images
import time
from datetime import datetime, timedelta

def find_best_image_pair(bbox, start_date, end_date, max_cloud_cover=20):
    """
    Find the best pair of images for comparison across long time periods.
    
    Args:
        bbox: Bounding box coordinates
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        max_cloud_cover: Maximum acceptable cloud cover percentage
    
    Returns:
        tuple: (early_image, late_image) or raises exception if not found
    """
    print(f"Searching for images between {start_date} and {end_date}")
    
    # Search for all images in the time period
    all_items = search_items(bbox, start_date, end_date)
    print(f"Found {len(all_items)} total images")
    
    # Filter by cloud cover
    good_items = [item for item in all_items 
                  if item.properties.get('eo:cloud_cover', 100) <= max_cloud_cover]
    print(f"Found {len(good_items)} images with cloud cover <= {max_cloud_cover}%")
    
    if len(good_items) < 2:
        raise Exception(f"Not enough good quality images found. Try increasing max_cloud_cover or expanding date range.")
    
    # Sort by date
    good_items.sort(key=lambda x: x.datetime)
    
    # For long-term analysis, pick images from similar seasons to avoid seasonal bias
    # Try to find images from same month in different years
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)
    
    # If analyzing across years, prefer same season
    if (end_dt - start_dt).days > 300:  # More than 10 months
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
            print(f"Selected seasonal match: {early_image.datetime.strftime('%Y-%m-%d')} and {late_image.datetime.strftime('%Y-%m-%d')}")
        else:
            # Fallback to first and last good images
            early_image = good_items[0]
            late_image = good_items[-1]
            print(f"Using first and last good images: {early_image.datetime.strftime('%Y-%m-%d')} and {late_image.datetime.strftime('%Y-%m-%d')}")
    else:
        # For shorter periods, just use first and last
        early_image = good_items[0]
        late_image = good_items[-1]
        print(f"Using first and last images: {early_image.datetime.strftime('%Y-%m-%d')} and {late_image.datetime.strftime('%Y-%m-%d')}")
    
    return early_image, late_image

def main():
    # Configuration - modify these for your analysis
    bbox = get_bbox()
    
    # Example configurations for different time periods:
    
    # 1. Year-long gap (seasonal analysis)
    start_date = "2022-06-01"
    end_date = "2024-06-30"
    
    # 2. Multi-year analysis (urban development)
    # start_date = "2020-01-01"
    # end_date = "2024-12-31"
    
    # 3. Specific seasonal comparison
    # start_date = "2023-03-01"  # Spring
    # end_date = "2023-09-30"    # Fall
    
    max_cloud_cover = 15  # Stricter cloud cover for better results
    
    print(f"Processing area: {bbox}")
    print(f"Date range: {start_date} to {end_date}")
    print(f"Maximum cloud cover: {max_cloud_cover}%")
    
    # Step 1: Find best image pair
    print("\n=== STEP 1: FINDING BEST IMAGE PAIR ===")
    try:
        early_item, late_item = find_best_image_pair(bbox, start_date, end_date, max_cloud_cover)
        
        print(f"\nSelected images:")
        print(f"  Early: {early_item.datetime.strftime('%Y-%m-%d')} (Cloud: {early_item.properties.get('eo:cloud_cover', 'N/A'):.1f}%)")
        print(f"  Late:  {late_item.datetime.strftime('%Y-%m-%d')} (Cloud: {late_item.properties.get('eo:cloud_cover', 'N/A'):.1f}%)")
        
        time_gap = (late_item.datetime - early_item.datetime).days
        print(f"  Time gap: {time_gap} days ({time_gap/365.25:.1f} years)")
        
    except Exception as e:
        print(f"Error finding suitable images: {e}")
        print("Suggestions:")
        print("  - Try increasing max_cloud_cover")
        print("  - Expand the date range")
        print("  - Choose a different AOI")
        return
    
    # Step 2: Get URLs
    print("\n=== STEP 2: GETTING SIGNED URLS ===")
    items = [early_item, late_item]
    urls = get_band_urls(items)
    
    # Step 3: Load bands
    print("\n=== STEP 3: DOWNLOADING RASTER DATA ===")
    print("This may take several minutes...")
    
    try:
        print("\n[1/4] Reading B04 (Red) from early image...")
        b04_1, transform1 = read_band_with_retry(urls[0]["B04"], max_size=1024)
        
        print("\n[2/4] Reading B08 (NIR) from early image...")
        b08_1, _ = read_band_with_retry(urls[0]["B08"], max_size=1024)
        
        print("\n[3/4] Reading B04 (Red) from late image...")
        b04_2, transform2 = read_band_with_retry(urls[1]["B04"], max_size=1024)
        
        print("\n[4/4] Reading B08 (NIR) from late image...")
        b08_2, _ = read_band_with_retry(urls[1]["B08"], max_size=1024)
        
    except Exception as e:
        print(f"Error loading raster data: {e}")
        return
    
    # Step 4: NDVI Computation
    print("\n=== STEP 4: COMPUTING NDVI ===")
    ndvi1 = compute_ndvi(b04_1, b08_1)
    ndvi2 = compute_ndvi(b04_2, b08_2)
    
    print(f"Early NDVI range: {ndvi1.min():.3f} to {ndvi1.max():.3f}")
    print(f"Late NDVI range: {ndvi2.min():.3f} to {ndvi2.max():.3f}")
    
    diff = diff_ndvi(ndvi1, ndvi2)
    print(f"NDVI difference range: {diff.min():.3f} to {diff.max():.3f}")
    
    # Step 5: Save all visualizations
    print("\n=== STEP 5: SAVING VISUALIZATIONS ===")
    try:
        # Save individual NDVI images
        early_date = early_item.datetime.strftime('%Y-%m-%d')
        late_date = late_item.datetime.strftime('%Y-%m-%d')
        
        early_path = save_individual_images(ndvi1, f"ndvi_early_{early_date}.png", "Early NDVI")
        late_path = save_individual_images(ndvi2, f"ndvi_late_{late_date}.png", "Late NDVI")
        
        # Save difference image
        diff_path = save_ndvi_diff(diff, f"ndvi_difference_{early_date}_to_{late_date}.png")
        
        print(f"\nAll visualizations saved:")
        print(f"  Early NDVI: {early_path}")
        print(f"  Late NDVI: {late_path}")
        print(f"  Difference: {diff_path}")
        
    except Exception as e:
        print(f"Visualization failed: {e}")
        return
    
    print(f"\nAnalysis complete! 🎉")
    print(f"Time period analyzed: {time_gap} days")
    print(f"Mean NDVI change: {diff.mean():.4f}")
    print(f"Max vegetation loss: {diff.min():.4f}")
    print(f"Max vegetation gain: {diff.max():.4f}")

if __name__ == "__main__":
    main()