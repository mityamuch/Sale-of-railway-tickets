from datetime import datetime
from pydantic import BaseModel


class Train(BaseModel):
    train_id: int
    route_id: int
    departure_date: datetime
    arrival_date: datetime
