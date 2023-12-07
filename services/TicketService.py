from datetime import datetime

from pymongo import ReturnDocument

from models.ticket import TicketPlace
from typing import List
from utils.elasticsearch_connector import search_trains
from utils.hazelcast_connector import lock_ticket, unlock_ticket
from utils.mongo_setup import db


class TicketService:

    @staticmethod
    def search_tickets(departure_station: str, arrival_station: str, departure_date: datetime) -> List[TicketPlace]:
        trains = search_trains(departure_station, arrival_station, departure_date)
        tickets = []

        for train in trains:
            try:
                # Получение билетов для каждого поезда из MongoDB
                train_tickets = db.ticket_places.find({"train_id": train["train_id"], "status": "free"})
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
                updated_ticket = await db.ticket_places.find_one_and_update(
                    {"ticket_id": ticket_id},
                    update_data,
                    return_document=ReturnDocument.AFTER
                )

                if updated_ticket:
                    return True
                else:
                    unlock_ticket(ticket_id)
                    return False
            except Exception as e:
                print(f"Error updating ticket: {e}")
                unlock_ticket(ticket_id)
                return False
        else:
            return False

    @staticmethod
    def purchase_ticket(ticket_id: int) -> bool:
        payment_successful = True  # Заглушка

        if payment_successful:
            try:
                update_data = {
                    "$set": {
                        "status": "purchased",
                        "payment_time": datetime.now()
                    }
                }
                updated_ticket = db.ticket_places.find_one_and_update(
                    {"ticket_id": ticket_id},
                    update_data,
                    return_document=ReturnDocument.AFTER
                )

                if updated_ticket:
                    unlock_ticket(ticket_id)
                    return True
                else:
                    print(f"Ticket with ID {ticket_id} not found for purchase.")
                    return False
            except Exception as e:
                print(f"Error purchasing ticket: {e}")
                return False
        else:
            print("Payment failed")
            return False

    @staticmethod
    async def get_ticket(ticket_id):
        return await db.tickets.find_one({"_id": ticket_id})

    @staticmethod
    async def update_ticket_status(ticket_id, status):
        await db.tickets.update_one({"_id": ticket_id}, {"$set": {"status": status}})

    @staticmethod
    async def add_ticket(ticket_data):
        return await db.tickets.insert_one(ticket_data)