import requests
from src.aoi import get_bbox
from src.search import search_items
from src.download import get_band_urls

# Test connectivity
bbox = get_bbox()
items = search_items(bbox, "2024-06-01", "2024-06-15")
urls = get_band_urls(items)

print("Testing URL accessibility...")
for i, url_set in enumerate(urls):
    print(f"\nImage {i+1}:")
    for band, url in url_set.items():
        try:
            response = requests.head(url, timeout=10)
            size_mb = int(response.headers.get('content-length', 0)) / (1024 * 1024)
            print(f"  {band}: ✓ Accessible ({size_mb:.1f} MB)")
        except Exception as e:
            print(f"  {band}: ✗ Error - {e}")