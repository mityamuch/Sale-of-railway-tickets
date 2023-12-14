from typing import List
from fastapi import APIRouter, HTTPException
from models.train import Train
from services.TrainService import TrainService

router = APIRouter()


@router.post("/", response_model=Train, responses={
    409: {"description": "Поезд с таким ID уже существует"}
})
async def add_train(train_data: Train):
    result = await TrainService.initialize_train(train_data.model_dump())
    if result is None:
        raise HTTPException(status_code=409, detail="Поезд с таким ID уже существует")
    return Train(**result)


@router.get("/{train_id}", response_model=Train, responses={
    404: {"description": "Поезд не найден"},
    500: {"description": "Ошибка сервера"},
})
async def get_train(train_id: int):

    result = await TrainService.get_train(train_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Поезд не найден")
    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail="Ошибка сервера")
    return Train(**result)


@router.get("/available/", response_model=List[Train])
async def available_trains(departure_station_id: int, arrival_station_id: int, departure_date: str):
    results = await TrainService.get_available_trains(departure_station_id,
                                                      arrival_station_id,
                                                      departure_date)
    return [Train(**result) for result in results]


@router.delete("/{train_id}/", responses={
    404: {"description": "Поезд не найден"},
})
async def delete_train(train_id: int):
    success = await TrainService.delete_train(train_id)
    if success:
        return {"message": "Train deleted successfully"}

    raise HTTPException(status_code=404, detail="Поезд не найден")
