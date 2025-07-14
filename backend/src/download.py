import planetary_computer

def get_band_urls(items, bands=["B04", "B08"]):
    signed_items = [planetary_computer.sign(item) for item in items]
    urls = []
    for item in signed_items:
        urls.append({b: item.assets[b].href for b in bands})
    return urls
