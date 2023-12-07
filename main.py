import uvicorn
from fastapi import FastAPI
from routes import station_routes, route_routes, train_routes, ticket_routes
from utils.elasticsearch_connector import create_train_index
from utils.mongo_setup import setup_sharding

#setup_sharding()
print("Sharding enabled.")

create_train_index()

app = FastAPI()

app.include_router(station_routes.router, prefix="/station", tags=["Stations"])
app.include_router(route_routes.router, prefix="/route", tags=["Routes"])
app.include_router(train_routes.router, prefix="/train", tags=["Trains"])
app.include_router(ticket_routes.router, prefix="/ticket", tags=["Tickets"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
