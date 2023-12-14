from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from models.ticket import TicketPlace
from services.TicketService import TicketService

router = APIRouter()


@router.post("/book/{ticket_id}", response_model=bool)
async def book_ticket(ticket_id: int) -> bool:
    result = await TicketService.book_ticket(ticket_id)
    if result:
        return True
    return False


@router.post("/purchase/{ticket_id}", response_model=bool)
async def purchase_ticket(ticket_id: int):
    result = await TicketService.purchase_ticket(ticket_id)
    if result:
        return True
    return False


@router.get("/search-tickets/", response_model=List[TicketPlace])
async def search_tickets_route(departure_station: str, arrival_station: str, departure_date: datetime):
    try:
        return TicketService.search_tickets(departure_station, arrival_station, departure_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ticket_id}", response_model=TicketPlace, responses={
    404: {"description": "Билет не найден"},
    500: {"description": "Ошибка сервера"},
})
async def get_ticket(ticket_id: int):
    result = await TicketService.get_ticket(ticket_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Билет не найден")
    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail="Ошибка сервера")
    return TicketPlace(**result)


@router.post("/", response_model=TicketPlace, responses={
    409: {"description": "Билет с таким ID уже существует"}
})
async def add_ticket(ticket_request: TicketPlace):
    result = await TicketService.add_ticket(ticket_request)
    if result is None:
        raise HTTPException(status_code=409, detail="Билет с таким ID уже существует")
    return TicketPlace(**result)
