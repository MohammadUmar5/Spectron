import rasterio
import time
from rasterio.env import Env
from rasterio.errors import RasterioIOError
from rasterio.windows import Window
import numpy as np

def read_band(url, timeout=120, max_size=2048):
    """
    Read a raster band from a URL with timeout and progress indication.
    Uses windowed reading to limit memory usage.
    
    Args:
        url (str): URL to the raster file
        timeout (int): Timeout in seconds (default: 120)
        max_size (int): Maximum dimension size to read (default: 2048)
    
    Returns:
        tuple: (array, transform) where array is the raster data and transform is the geotransform
    """
    print(f"→ Opening {url[-60:]}")  # Show just the end of URL
    
    # Set up environment with timeout
    env_options = {
        'GDAL_HTTP_TIMEOUT': str(timeout),
        'GDAL_HTTP_CONNECTTIMEOUT': '30',
        'VSI_CURL_ALLOWED_EXTENSIONS': '.tif,.tiff',
        'GDAL_DISABLE_READDIR_ON_OPEN': 'EMPTY_DIR',
        'GDAL_HTTP_MAX_RETRY': '3',
        'GDAL_HTTP_RETRY_DELAY': '1'
    }
    
    try:
        with Env(**env_options):
            start_time = time.time()
            print("→ Connecting to remote file...")
            
            with rasterio.open(url) as src:
                print(f"→ File info: {src.width}x{src.height} pixels, {src.count} bands")
                
                # Calculate window to read (downsample if too large)
                if src.width > max_size or src.height > max_size:
                    # Calculate scale factor to fit within max_size
                    scale = min(max_size / src.width, max_size / src.height)
                    new_width = int(src.width * scale)
                    new_height = int(src.height * scale)
                    
                    print(f"→ Downsampling from {src.width}x{src.height} to {new_width}x{new_height}")
                    
                    # Read with resampling
                    array = src.read(1, 
                                   out_shape=(new_height, new_width),
                                   resampling=rasterio.enums.Resampling.bilinear)
                    
                    # Adjust transform for the new resolution
                    transform = src.transform * src.transform.scale(
                        (src.width / new_width),
                        (src.height / new_height)
                    )
                else:
                    print("→ Reading full resolution data...")
                    array = src.read(1)
                    transform = src.transform
                
                elapsed_time = time.time() - start_time
                data_size_mb = array.nbytes / (1024 * 1024)
                print(f"→ Done in {elapsed_time:.1f} seconds ({data_size_mb:.1f} MB)")
                
                return array, transform
                
    except RasterioIOError as e:
        print(f"✗ Error reading raster: {e}")
        raise
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        raise

def read_band_with_retry(url, max_retries=3, timeout=120, max_size=2048):
    """
    Read a raster band with retry logic.
    
    Args:
        url (str): URL to the raster file
        max_retries (int): Maximum number of retry attempts
        timeout (int): Timeout in seconds for each attempt
        max_size (int): Maximum dimension size to read
    
    Returns:
        tuple: (array, transform) where array is the raster data and transform is the geotransform
    """
    for attempt in range(max_retries):
        try:
            return read_band(url, timeout, max_size)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"→ Attempt {attempt + 1} failed, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"✗ All {max_retries} attempts failed")
                raise e