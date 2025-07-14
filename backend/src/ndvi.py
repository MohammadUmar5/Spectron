import numpy as np

def compute_ndvi(red, nir):
    """
    Compute NDVI with proper scaling for Sentinel-2 data.
    Sentinel-2 data comes as uint16 with scale factor of 0.0001.
    """
    # Convert to float and apply scale factor
    red_scaled = red.astype(np.float32) * 0.0001
    nir_scaled = nir.astype(np.float32) * 0.0001
    
    # Compute NDVI
    ndvi = (nir_scaled - red_scaled) / (nir_scaled + red_scaled + 1e-10)
    
    # Clip to valid NDVI range
    ndvi = np.clip(ndvi, -1, 1)
    
    return ndvi

def diff_ndvi(ndvi1, ndvi2):
    """
    Compute the difference between two NDVI arrays.
    """
    return ndvi2 - ndvi1