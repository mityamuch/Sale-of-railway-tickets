from typing import List
from fastapi import APIRouter, HTTPException
from models.train import Train
from services.TrainService import TrainService

router = APIRouter()


@router.post("/trains/", response_model=Train)
async def add_train(train_data: Train):
    result = await TrainService.initialize_train(train_data.dict())
    return Train(**result)


@router.get("/{train_id}", response_model=Train)
async def get_train(train_id: int):
    result = await TrainService.get_train(train_id)
    if result:
        return Train(**result)

    raise HTTPException(status_code=404, detail="Train not found")


@router.get("/available/", response_model=List[Train])
async def available_trains(departure_station_id: int, arrival_station_id: int, departure_date: str):
    results = await TrainService.get_available_trains(departure_station_id,
                                                      arrival_station_id,
                                                      departure_date)
    return [Train(**result) for result in results]


@router.put("/{train_id}/", response_model=Train)
async def update_train(train_id: int, train_data: Train):
    result = await TrainService.update_train(train_id, train_data.dict())
    if result:
        return Train(**result)

    raise HTTPException(status_code=404, detail="Train not found")


@router.delete("/{train_id}/")
async def delete_train(train_id: int):
    success = await TrainService.delete_train(train_id)
    if success:
        return {"message": "Train deleted successfully"}

    raise HTTPException(status_code=404, detail="Train not found")
