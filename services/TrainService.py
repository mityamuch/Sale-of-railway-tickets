from services.mongo_service import db


class TrainService:

    @staticmethod
    async def initialize_train(train_data):
        await db.trains.insert_one(train_data)

    @staticmethod
    async def get_train(train_id):
        return await db.trains.find_one({"_id": train_id})

    @staticmethod
    async def get_available_trains(departure_station_id, arrival_station_id, departure_date):
        return await db.trains.find({
            "departure_station_id": departure_station_id,
            "arrival_station_id": arrival_station_id,
            "departure_date": {"$gte": departure_date}
        }).to_list(length=100)  # Здесь ограничиваем результат 100 записями для примера

    @staticmethod
    async def update_train(train_id, train_data):
        updated_train = await db.trains.find_one_and_update({"_id": train_id}, {"$set": train_data},
                                                            return_document=True)
        return updated_train

    @staticmethod
    async def delete_train(train_id):
        deleted_train = await db.trains.delete_one({"_id": train_id})
        return deleted_train.deleted_count > 0
