from pydantic import BaseModel
from datetime import datetime
from typing import List


class Train(BaseModel):
    train_id: int
    route_id: int
    departure_date: datetime
    arrival_date: datetime
