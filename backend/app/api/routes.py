from fastapi import APIRouter
from app.schemas.aoi import AOIRequest

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Spectron backend is running!"}

@router.post("/detect")
async def detect_changes(data: AOIRequest):
    # Placeholder for actual logic
    return {"status": "processing", "aoi": data.aoi}