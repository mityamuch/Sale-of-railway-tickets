from fastapi import APIRouter
from models.station import Station
from services.StationService import StationService

router = APIRouter()


@router.post("/", response_model=Station)
async def add_station(station_data: Station):
    result = await StationService.add_station(station_data.model_dump())
    return Station(**result)


@router.get("/{station_id}", response_model=Station)
async def get_station(station_id: int):
    result = await StationService.get_station(station_id)
    return Station(**result)
