import motor.motor_asyncio
from pymongo import MongoClient

# Асинхронный клиент
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

db = client.railway_ticket_system

# Синхронный клиент (для настройки шардинга и других административных задач)
sync_client = MongoClient('mongodb://localhost:27017')


def setup_sharding():
    # Выбираем базу данных и админскую базу данных
    sdb = sync_client["railway_ticket_system"]
    admin_db = sync_client["admin"]

    # Включаем шардинг для базы данных
    admin_db.command("enableSharding", "your_database_name")

    # Устанавливаем ключ шардинга для коллекции
    sdb.command("shardCollection", "railway_ticket_system", key={"station_id": 1})
