from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from models.ticket import (TicketPlace,
                           TicketNotFoundException,
                           TicketAlreadyBookedException,
                           TicketLockFailedException,
                           TicketUpdateException,
                           TicketNotBookedException,
                           TicketPurchaseFailedException)
from services.TicketService import TicketService

router = APIRouter()


@router.post("/book/{ticket_id}", response_model=bool, responses={
    404: {"description": "Билет не найден"},
    400: {"description": "Билет уже забронирован или куплен"},
    503: {"description": "Не удалось заблокировать билет"},
    500: {"description": "Ошибка сервера"},
})
async def book_ticket(ticket_id: int):
    try:
        result = await TicketService.book_ticket(ticket_id)
        return result
    except TicketNotFoundException:
        raise HTTPException(status_code=404, detail="Билет не найден")
    except TicketAlreadyBookedException:
        raise HTTPException(status_code=400, detail="Билет уже забронирован или куплен")
    except TicketLockFailedException:
        raise HTTPException(status_code=503, detail="Не удалось заблокировать билет")
    except TicketUpdateException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/purchase/{ticket_id}", response_model=bool, responses={
    404: {"description": "Билет не найден"},
    400: {"description": "Билет не забронирован"},
    500: {"description": "Ошибка произведения оплаты"},
})
async def purchase_ticket(ticket_id: int):
    try:
        result = await TicketService.purchase_ticket(ticket_id)
        return result
    except TicketNotFoundException:
        raise HTTPException(status_code=404, detail="Билет не найден")
    except TicketNotBookedException:
        raise HTTPException(status_code=400, detail="Билет не забронирован")
    except TicketPurchaseFailedException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search-tickets/", response_model=List[TicketPlace])
async def search_tickets_route(departure_station: str, arrival_station: str, departure_date: datetime):
    try:
        return await TicketService.search_tickets(departure_station, arrival_station, departure_date)
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
