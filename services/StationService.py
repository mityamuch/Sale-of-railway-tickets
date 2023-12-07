from utils.hazelcast_connector import cache_station, get_cached_station
from utils.mongo_setup import db


class StationService:

    @staticmethod
    async def add_station(station_data):
        cache_station(station_data["_id"], station_data)
        await db.stations.insert_one(station_data)

    @staticmethod
    async def get_station(station_id):
        return get_cached_station(station_id)
