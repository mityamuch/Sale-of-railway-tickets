from fastapi import APIRouter, HTTPException
from models.route import Route
from services.RouteService import RouteService

router = APIRouter()


@router.post("/", response_model=Route, responses={
    409: {"description": "Маршрут с таким ID уже существует"}
})
async def add_route(route_data: Route):

    result = await RouteService.add_route(route_data.model_dump())
    if result is None:
        raise HTTPException(status_code=409, detail="Маршрут с таким ID уже существует")
    return result


@router.get("/{route_id}", response_model=Route, responses={
    404: {"description": "Маршрут не найден"},
})
async def get_route(route_id: int):
    result = await RouteService.get_route(route_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Маршрут не найден")
    return result
