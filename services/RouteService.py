from services.mongo_service import db


class RouteService:

    @staticmethod
    async def add_route(route_data):
        await db.routes.insert_one(route_data)

    @staticmethod
    async def get_route(route_id):
        return await db.routes.find_one({"_id": route_id})
