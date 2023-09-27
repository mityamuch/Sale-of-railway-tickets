from services.mongo_service import db


class StationService:

    @staticmethod
    async def add_station(station_data):
        await db.stations.insert_one(station_data)

    @staticmethod
    async def get_station(station_id):
        return await db.stations.find_one({"_id": station_id})
