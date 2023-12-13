from utils.hazelcast_connector import cache_station, get_cached_station
from utils.mongo_setup import db


class StationService:

    @staticmethod
    async def add_station(station_data):
        existing_station = await db.stations.find_one({"station_id": station_data["station_id"]})
        if existing_station:
            return None
        cache_station(station_data["station_id"], station_data)
        insert_result = await db.stations.insert_one(station_data)
        inserted_station = await db.stations.find_one({"_id": insert_result.inserted_id})

        return inserted_station

    @staticmethod
    async def get_station(station_id):
        return await get_cached_station(station_id)
