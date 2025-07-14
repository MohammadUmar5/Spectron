from pystac_client import Client
import planetary_computer

def search_items(start: str, end: str, bbox: list):
    """
    Search for Sentinel-2 items using STAC API
    
    Args:
        start: Start date in ISO format (YYYY-MM-DD)
        end: End date in ISO format (YYYY-MM-DD)
        bbox: Bounding box as [min_lon, min_lat, max_lon, max_lat]
    """
    client = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
    
    search = client.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=f"{start}/{end}",
        query={"eo:cloud_cover": {"lt": 20}},
    )
    
    items = list(search.items())
    return sorted(items, key=lambda x: x.properties["eo:cloud_cover"])
