from fastapi import FastAPI
from routes import station_routes, route_routes, train_routes, ticket_routes

app = FastAPI()

app.include_router(station_routes.router, prefix="/station", tags=["Stations"])
app.include_router(route_routes.router, prefix="/route", tags=["Routes"])
app.include_router(train_routes.router, prefix="/train", tags=["Trains"])
app.include_router(ticket_routes.router, prefix="/ticket", tags=["Tickets"])
