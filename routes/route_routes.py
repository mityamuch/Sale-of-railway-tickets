from fastapi import APIRouter
from models.route import Route
from services.RouteService import RouteService

router = APIRouter()


@router.post("/", response_model=Route)
async def add_route(route_data: Route):
    result = await RouteService.add_route(route_data.model_dump())
    return Route(**result)


@router.get("/{route_id}", response_model=Route)
async def get_route(route_id: int):
    result = await RouteService.get_route(route_id)
    return Route(**result)
