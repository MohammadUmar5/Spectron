from pystac_client import Client

def search_items(bbox, start, end):
    catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
    results = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=f"{start}/{end}",
        query={"eo:cloud_cover": {"lt": 10}},
    )
    items = list(results.items())
    items.sort(key=lambda x: x.datetime)
    return items[:2]
