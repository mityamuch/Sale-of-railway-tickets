from typing import List
from pydantic import BaseModel


class Route(BaseModel):
    route_id: int
    stations: List[int]  # Список station_id
    route_name: str
