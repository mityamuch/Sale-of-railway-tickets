from fastapi import APIRouter
from models.ticket import TicketPlace
from services.TicketService import TicketService

router = APIRouter()


@router.post("/book/{ticket_id}", response_model=TicketPlace)
async def book_ticket(ticket_id: int):
    result = await TicketService.book_ticket(ticket_id)
    return result


@router.post("/purchase/{ticket_id}", response_model=TicketPlace)
async def purchase_ticket(ticket_id: int):
    result = await TicketService.purchase_ticket(ticket_id)
    return result


@router.get("/{ticket_id}", response_model=TicketPlace)
async def get_ticket(ticket_id: int):
    result = await TicketService.get_ticket(ticket_id)
    return TicketPlace(**result)


@router.post("/", response_model=TicketPlace)
async def add_ticket(ticket_id: int):
    result = await TicketService.add_ticket(ticket_id)
    return TicketPlace(**result)
