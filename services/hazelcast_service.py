# services/hazelcast_service.py

from utils.hazelcast_connector import hazelcast_client


def cache_station(station_id, station_data):
    stations_map = hazelcast_client.get_map("stations")
    stations_map.put(station_id, station_data)


def get_cached_station(station_id):
    stations_map = hazelcast_client.get_map("stations")
    return stations_map.get(station_id)


def lock_ticket(ticket_id):
    tickets_lock = hazelcast_client.get_lock(ticket_id)
    return tickets_lock.try_lock()


def unlock_ticket(ticket_id):
    tickets_lock = hazelcast_client.get_lock(ticket_id)
    tickets_lock.unlock()
