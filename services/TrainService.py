from utils.elasticsearch_connector import search_trains, add_train_to_index, delete_train_from_index
from utils.mongo_setup import db


class TrainService:

    @staticmethod
    async def initialize_train(train_data):

        existing_station = await db.trains.find_one({"train_id": train_data["train_id"]})
        if existing_station:
            return None
        await add_train_to_index(train_data)
        insert_result = await db.trains.insert_one(train_data)
        inserted_train = await db.trains.find_one({"_id": insert_result.inserted_id})

        return inserted_train

    @staticmethod
    async def get_train(train_id):
        result = await db.trains.find_one({"train_id": train_id})
        if result:
            return result
        return None

    @staticmethod
    async def get_available_trains(departure_station_id, arrival_station_id, departure_date):
        return search_trains(departure_station_id, arrival_station_id, departure_date)

    @staticmethod
    async def delete_train(train_id):
        deleted_train = await db.trains.delete_one({"train_id": train_id})
        delete_train_from_index(train_id)
        return deleted_train.deleted_count > 0
