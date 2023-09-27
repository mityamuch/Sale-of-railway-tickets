from datetime import datetime
from models.ticket import TicketPlace
from services.es_service import search_trains
from services.hazelcast_service import lock_ticket, unlock_ticket
from typing import List

from services.mongo_service import db


class TicketService:

    @staticmethod
    def search_tickets(departure_station: str, arrival_station: str, departure_date: datetime) -> List[TicketPlace]:
        # Используем ElasticSearch для получения списка доступных поездов
        trains = search_trains(departure_station, arrival_station, departure_date)

        # Здесь может быть логика преобразования данных из ElasticSearch в модели TicketPlace, если это необходимо

        return trains

    @staticmethod
    def book_ticket(ticket_id: int) -> bool:
        # Используем Hazelcast для блокировки места
        if lock_ticket(ticket_id):
            # Если блокировка успешно установлена, сохраняем статус билета как "booked" в MongoDB
            # TODO: Сохранение статуса билета в MongoDB
            return True
        return False

    @staticmethod
    def purchase_ticket(ticket_id: int) -> bool:
        # Здесь будет логика оплаты билета. После успешной оплаты:
        # 1. Сохраняем статус билета как "purchased" в MongoDB
        # 2. Снимаем блокировку в Hazelcast

        # TODO: Реализовать логику оплаты
        payment_successful = True  # Заглушка

        if payment_successful:
            # TODO: Сохранение статуса билета в MongoDB
            unlock_ticket(ticket_id)
            return True
        return False

    @staticmethod
    async def get_ticket(ticket_id):
        return await db.tickets.find_one({"_id": ticket_id})

    @staticmethod
    async def update_ticket_status(ticket_id, status):
        await db.tickets.update_one({"_id": ticket_id}, {"$set": {"status": status}})