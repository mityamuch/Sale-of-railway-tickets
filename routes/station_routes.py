from fastapi import APIRouter, HTTPException
from models.station import Station
from services.StationService import StationService

router = APIRouter()


@router.post("/", response_model=Station, responses={
    409: {"description": "Станция с таким ID уже существует"}
})
async def add_station(station_data: Station):
    result = await StationService.add_station(station_data.model_dump())
    if result is None:
        raise HTTPException(status_code=409, detail="Станция с таким ID уже существует")
    return result


@router.get("/{station_id}", response_model=Station, responses={
    404: {"description": "Станция не найдена"},
    500: {"description": "Ошибка сервера"},
})
async def get_station(station_id: int):
    result = await StationService.get_station(station_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Станция не найдена")
    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail="Ошибка сервера")
    return Station(**result)
