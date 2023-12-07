from utils.elasticsearch_connector import search_trains, add_train_to_index
from utils.mongo_setup import db


class TrainService:

    @staticmethod
    async def initialize_train(train_data):
        add_train_to_index(train_data)
        await db.trains.insert_one(train_data)

    @staticmethod
    async def get_train(train_id):
        return await db.trains.find_one({"_id": train_id})

    @staticmethod
    async def get_available_trains(departure_station_id, arrival_station_id, departure_date):
        return search_trains(departure_station_id, arrival_station_id, departure_date)

    @staticmethod
    async def update_train(train_id, train_data):
        updated_train = await db.trains.find_one_and_update({"_id": train_id}, {"$set": train_data},
                                                            return_document=True)
        return updated_train

    @staticmethod
    async def delete_train(train_id):
        deleted_train = await db.trains.delete_one({"_id": train_id})
        return deleted_train.deleted_count > 0
