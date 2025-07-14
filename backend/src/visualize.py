import cv2
import numpy as np

def percentile_stretch(data, lower_percentile=2, upper_percentile=98):
    """
    Apply percentile stretch to enhance image contrast while preserving data integrity.
    
    Args:
        data: Input array (NDVI values)
        lower_percentile: Lower percentile for stretch (default: 2)
        upper_percentile: Upper percentile for stretch (default: 98)
    
    Returns:
        numpy.ndarray: Stretched data normalized to 0-255 range
    """
    # Calculate percentile values
    lower_val = np.percentile(data, lower_percentile)
    upper_val = np.percentile(data, upper_percentile)
    
    # Apply stretch with soft clipping at percentiles
    stretched = np.clip(data, lower_val, upper_val)
    
    # Normalize to 0-255 range
    normalized = ((stretched - lower_val) / (upper_val - lower_val) * 255).astype(np.uint8)
    
    return normalized

def save_ndvi_diff(diff, output_path="ndvi_diff.png"):
    """
    Save NDVI difference as a colored image using only OpenCV.
    
    Args:
        diff: NDVI difference array (values typically between -1 and 1)
        output_path: Output file path
    
    Returns:
        str: Path to saved image
    """
    print(f"NDVI difference stats:")
    print(f"  Min: {diff.min():.3f}")
    print(f"  Max: {diff.max():.3f}")
    print(f"  Mean: {diff.mean():.3f}")
    print(f"  Std: {diff.std():.3f}")
    
    # For difference images, use a diverging colormap
    # Center the colormap around 0 (no change)
    abs_max = max(abs(diff.min()), abs(diff.max()))
    
    # Normalize to 0-255 range, centered around 127 (middle gray)
    diff_normalized = ((diff + abs_max) / (2 * abs_max) * 255).astype(np.uint8)
    
    # Use numeric colormap IDs that are compatible with all OpenCV versions
    colormaps_to_try = [
        (2, 'JET'),     # Classic rainbow - good for differences
        (9, 'HSV'),     # HSV colormap
        (4, 'RAINBOW'), # Rainbow colormap
        (11, 'COOL'),   # Cool colormap
        (0, 'AUTUMN'),  # Autumn colormap
        (6, 'SUMMER'),  # Summer colormap
        (7, 'SPRING'),  # Spring colormap
    ]
    
    colored = None
    used_colormap = None
    
    for colormap_id, name in colormaps_to_try:
        try:
            colored = cv2.applyColorMap(diff_normalized, colormap_id)
            used_colormap = name
            print(f"Using {name} colormap (ID: {colormap_id}) for difference")
            break
        except Exception as e:
            print(f"Colormap {name} (ID: {colormap_id}) failed: {e}")
            continue
    
    if colored is None:
        print("Creating custom difference colormap")
        # Create custom red-green diverging colormap
        colored = create_custom_diverging_colormap(diff_normalized)
        used_colormap = "Custom diverging"
    
    # Save the image
    success = cv2.imwrite(output_path, colored)
    if success:
        print(f"Difference image saved using {used_colormap} colormap to: {output_path}")
        return output_path
    else:
        raise Exception(f"Failed to save image to {output_path}")

def save_individual_images(ndvi, output_path="ndvi_image.png", title="NDVI"):
    """
    Save individual NDVI images with appropriate colormaps.
    
    Args:
        ndvi: NDVI array (values typically between -1 and 1)
        output_path: Output file path
        title: Title for the image (for logging)
    
    Returns:
        str: Path to saved image
    """
    print(f"{title} stats:")
    print(f"  Min: {ndvi.min():.3f}")
    print(f"  Max: {ndvi.max():.3f}")
    print(f"  Mean: {ndvi.mean():.3f}")
    print(f"  Std: {ndvi.std():.3f}")
    
    # For NDVI images, apply percentile stretch for better visualization
    ndvi_normalized = percentile_stretch(ndvi, 2, 98)
    
    # Use numeric colormap IDs that work with all OpenCV versions
    colormaps_to_try = [
        (6, 'SUMMER'),  # Summer colormap (good for vegetation)
        (7, 'SPRING'),  # Spring colormap (good for vegetation)
        (2, 'JET'),     # JET colormap
        (9, 'HSV'),     # HSV colormap
        (4, 'RAINBOW'), # Rainbow colormap
        (0, 'AUTUMN'),  # Autumn colormap
        (11, 'COOL'),   # Cool colormap
        (12, 'HOT'),    # Hot colormap
    ]
    
    colored = None
    used_colormap = None
    
    for colormap_id, name in colormaps_to_try:
        try:
            colored = cv2.applyColorMap(ndvi_normalized, colormap_id)
            used_colormap = name
            print(f"Using {name} colormap (ID: {colormap_id}) for {title}")
            break
        except Exception as e:
            print(f"Colormap {name} (ID: {colormap_id}) failed: {e}")
            continue
    
    if colored is None:
        print("Creating custom vegetation colormap")
        # Create custom vegetation colormap (brown to green)
        colored = create_custom_vegetation_colormap(ndvi_normalized)
        used_colormap = "Custom vegetation"
    
    # Save the image
    success = cv2.imwrite(output_path, colored)
    if success:
        print(f"{title} saved using {used_colormap} colormap to: {output_path}")
        return output_path
    else:
        raise Exception(f"Failed to save {title} to {output_path}")

def create_custom_diverging_colormap(normalized_data):
    """
    Create a custom red-green diverging colormap for difference images.
    Red = vegetation loss, Green = vegetation gain, Gray = no change
    """
    height, width = normalized_data.shape
    colored = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Values < 127 are red (vegetation loss)
    # Values > 127 are green (vegetation gain)
    # Values = 127 are gray (no change)
    
    # Create a smooth transition from red to green
    for i in range(height):
        for j in range(width):
            val = normalized_data[i, j]
            
            if val < 127:
                # Red to gray transition (vegetation loss)
                intensity = (127 - val) / 127.0
                colored[i, j] = [
                    int(100 * intensity),      # Blue (low)
                    int(100 * intensity),      # Green (low)
                    int(255 * intensity + 100) # Red (high)
                ]
            elif val > 127:
                # Gray to green transition (vegetation gain)
                intensity = (val - 127) / 128.0
                colored[i, j] = [
                    int(100 * (1 - intensity)), # Blue (low)
                    int(255 * intensity + 100), # Green (high)
                    int(100 * (1 - intensity))  # Red (low)
                ]
            else:
                # No change (gray)
                colored[i, j] = [128, 128, 128]
    
    return colored

def create_custom_vegetation_colormap(normalized_data):
    """
    Create a custom vegetation colormap from brown (low NDVI) to green (high NDVI).
    """
    height, width = normalized_data.shape
    colored = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Brown to green gradient
    # Low values: brown/red
    # High values: green
    
    for i in range(height):
        for j in range(width):
            val = normalized_data[i, j]
            intensity = val / 255.0
            
            # Create brown to green transition
            if intensity < 0.3:
                # Very low NDVI - brown/red
                colored[i, j] = [
                    int(50 + 100 * intensity),  # Blue
                    int(50 + 150 * intensity),  # Green
                    int(150 + 100 * intensity)  # Red
                ]
            elif intensity < 0.7:
                # Medium NDVI - yellow/green transition
                t = (intensity - 0.3) / 0.4
                colored[i, j] = [
                    int(50 * (1 - t)),    # Blue
                    int(150 + 100 * t),   # Green
                    int(200 * (1 - t))    # Red
                ]
            else:
                # High NDVI - green
                t = (intensity - 0.7) / 0.3
                colored[i, j] = [
                    int(50 * (1 - t)),    # Blue
                    int(200 + 55 * t),    # Green
                    int(50 * (1 - t))     # Red
                ]
    
    return colored

def create_composite_image(early_ndvi, late_ndvi, diff, output_path="composite_ndvi.png"):
    """
    Create a composite image showing all three visualizations side by side.
    
    Args:
        early_ndvi: Early NDVI array
        late_ndvi: Late NDVI array
        diff: NDVI difference array
        output_path: Output file path
    
    Returns:
        str: Path to saved composite image
    """
    # Resize all images to same size for composite
    height, width = early_ndvi.shape
    target_width = 400  # Resize for composite
    target_height = int(height * target_width / width)
    
    # Process each image
    early_colored = process_ndvi_for_composite(early_ndvi, target_height, target_width, "vegetation")
    late_colored = process_ndvi_for_composite(late_ndvi, target_height, target_width, "vegetation")
    diff_colored = process_ndvi_for_composite(diff, target_height, target_width, "difference")
    
    # Create composite (side by side)
    composite = np.hstack([early_colored, late_colored, diff_colored])
    
    # Add labels (if OpenCV supports text)
    try:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(composite, "Early NDVI", (10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(composite, "Late NDVI", (target_width + 10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(composite, "Difference", (2 * target_width + 10, 30), font, 1, (255, 255, 255), 2)
    except:
        pass  # Skip text if not supported
    
    success = cv2.imwrite(output_path, composite)
    if success:
        print(f"Composite image saved to: {output_path}")
        return output_path
    else:
        raise Exception(f"Failed to save composite image to {output_path}")

def process_ndvi_for_composite(data, height, width, colormap_type):
    """Helper function to process NDVI data for composite image."""
    # Normalize data
    if colormap_type == "difference":
        abs_max = max(abs(data.min()), abs(data.max()))
        normalized = ((data + abs_max) / (2 * abs_max) * 255).astype(np.uint8)
    else:  # vegetation
        normalized = percentile_stretch(data, 2, 98)
    
    # Resize
    resized = cv2.resize(normalized, (width, height))
    
    # Apply colormap using numeric IDs
    try:
        if colormap_type == "difference":
            colored = cv2.applyColorMap(resized, 2)  # JET
        else:
            colored = cv2.applyColorMap(resized, 6)  # SUMMER
    except:
        # Fallback to custom colormap
        if colormap_type == "difference":
            colored = create_custom_diverging_colormap(resized)
        else:
            colored = create_custom_vegetation_colormap(resized)
    
    return colored

def check_opencv_colormaps():
    """Check which colormaps are available in the current OpenCV version."""
    print(f"OpenCV version: {cv2.__version__}")
    
    # Test numeric colormap IDs (these should work in most OpenCV versions)
    numeric_colormaps = [
        (0, 'AUTUMN'), (1, 'BONE'), (2, 'JET'), (3, 'WINTER'),
        (4, 'RAINBOW'), (5, 'OCEAN'), (6, 'SUMMER'), (7, 'SPRING'),
        (8, 'COOL'), (9, 'HSV'), (10, 'PINK'), (11, 'HOT'),
        (12, 'PARULA'), (13, 'MAGMA'), (14, 'INFERNO'), (15, 'PLASMA'),
        (16, 'VIRIDIS'), (17, 'CIVIDIS'), (18, 'TWILIGHT'), (19, 'TWILIGHT_SHIFTED'),
        (20, 'TURBO')
    ]
    
    available = []
    test_image = np.zeros((100, 100), dtype=np.uint8)
    
    for colormap_id, name in numeric_colormaps:
        try:
            cv2.applyColorMap(test_image, colormap_id)
            available.append((colormap_id, name))
        except Exception:
            pass
    
    print(f"Available numeric colormaps: {available}")
    return available

# Test function to verify colormaps work
def test_colormaps():
    """Test which colormaps work with current OpenCV installation."""
    print("Testing OpenCV colormaps...")
    available = check_opencv_colormaps()
    
    if available:
        print(f"Found {len(available)} working colormaps")
        print("Recommended colormaps for NDVI:")
        print("  - SUMMER (ID: 6): Good for vegetation")
        print("  - SPRING (ID: 7): Good for vegetation")
        print("  - JET (ID: 2): Good for differences")
        print("  - HSV (ID: 9): Good for differences")
    else:
        print("No standard colormaps found - will use custom colormaps")
    
    return available

if __name__ == "__main__":
    # Run colormap test
    test_colormaps()
