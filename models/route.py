from pydantic import BaseModel
from typing import List


class Route(BaseModel):
    route_id: int
    stations: List[int]  # Список station_id
    route_name: str
