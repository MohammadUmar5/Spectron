from pydantic import BaseModel
from typing import List

class AOIRequest(BaseModel):
    aoi: List[float]  # For example: [min_lon, min_lat, max_lon, max_lat]
    start_date: str
    end_date: str