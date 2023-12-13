from utils.mongo_setup import db


class RouteService:

    @staticmethod
    async def add_route(route_data):
        existing_route = await db.routes.find_one({"route_id": route_data["route_id"]})
        if existing_route:
            return None

        insert_result = await db.routes.insert_one(route_data)
        inserted_route = await db.routes.find_one({"_id": insert_result.inserted_id})

        return inserted_route

    @staticmethod
    async def get_route(route_id):
        result = await db.routes.find_one({"route_id": route_id})
        if result:
            return result
        return None
