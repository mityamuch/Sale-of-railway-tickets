from datetime import datetime
from typing import List
from pymongo import ReturnDocument
from models.ticket import TicketPlace
from utils.elasticsearch_connector import search_trains
from utils.hazelcast_connector import lock_ticket, unlock_ticket
from utils.mongo_setup import db


class TicketService:

    @staticmethod
    def search_tickets(departure_station: str,
                       arrival_station: str, departure_date: datetime) -> List[TicketPlace]:
        trains = search_trains(departure_station,
                               arrival_station,
                               departure_date)
        tickets = []

        for train in trains:
            try:
                # Получение билетов для каждого поезда из MongoDB
                train_tickets = db.tickets.find({"train_id": train["train_id"],
                                                 "status": "free"})
                for ticket in train_tickets:
                    tickets.append(TicketPlace(**ticket))
            except Exception as e:
                print(f"Error fetching tickets for train {train['train_id']}: {e}")

        return tickets

    @staticmethod
    async def book_ticket(ticket_id: int) -> bool:
        if lock_ticket(ticket_id):
            try:
                update_data = {
                    "$set": {
                        "status": "booked",
                        "booking_time": datetime.now()
                    }
                }
                updated_ticket = await db.tickets.find_one_and_update(
                    {"ticket_id": ticket_id},
                    update_data,
                    return_document=ReturnDocument.AFTER
                )

                if updated_ticket:
                    unlock_ticket(ticket_id)
                    return True

                unlock_ticket(ticket_id)
                return False
            except Exception as e:
                print(f"Error updating ticket: {e}")
                unlock_ticket(ticket_id)
                return False

        return False

    @staticmethod
    async def purchase_ticket(ticket_id: int) -> bool:
        payment_successful = True  # Заглушка
        result = await db.tickets.find_one({"ticket_id": ticket_id})
        if payment_successful and result["status"] == 'booked':
            try:
                update_data = {
                    "$set": {
                        "status": "purchased",
                        "payment_time": datetime.now()
                    }
                }
                updated_ticket = await db.tickets.find_one_and_update(
                    {"ticket_id": ticket_id},
                    update_data,
                    return_document=ReturnDocument.AFTER
                )

                if updated_ticket:
                    # unlock_ticket(ticket_id)
                    return True

                print(f"Ticket with ID {ticket_id} not found for purchase.")
                return False
            except Exception as e:
                print(f"Error purchasing ticket: {e}")
                return False

        return False

    @staticmethod
    async def get_ticket(ticket_id):
        result = await db.tickets.find_one({"ticket_id": ticket_id})
        if result:
            return result
        return None

    @staticmethod
    async def add_ticket(ticket_data):
        ticket_data.status = "free"
        ticket_data.booking_time = datetime(1, 1, 1, 0, 0, 0)
        ticket_data.payment_time = datetime(1, 1, 1, 0, 0, 0)
        existing_ticket = await db.tickets.find_one({"ticket_id": ticket_data.ticket_id})
        if existing_ticket:
            return None
        ticket_dict = ticket_data.dict()
        insert_result = await db.tickets.insert_one(ticket_dict)
        inserted_ticket = await db.tickets.find_one({"_id": insert_result.inserted_id})

        return inserted_ticket
