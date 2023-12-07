import logging
import coloredlogs
import hazelcast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hazelcast")
coloredlogs.install()


def get_hazelcast_client():
    client = hazelcast.HazelcastClient()
    logger.info("Connected to cluster")
    return client


hazelcast_client = get_hazelcast_client()


def cache_station(station_id, station_data):
    try:
        stations_map = hazelcast_client.get_map("stations")
        stations_map.put(station_id, station_data)
        logger.info(f"Station data cached for station ID: {station_id}")
    except Exception as e:
        logger.error(f"Error caching station data for station ID {station_id}: {e}")


def get_cached_station(station_id):
    try:
        stations_map = hazelcast_client.get_map("stations")
        station_data = stations_map.get(station_id)
        if station_data is None:
            logger.warning(f"No data found in cache for station ID: {station_id}")
        else:
            logger.info(f"Retrieved data from cache for station ID: {station_id}")
        return station_data
    except Exception as e:
        logger.error(f"Error retrieving station data for station ID {station_id}: {e}")
        return None


def lock_ticket(ticket_id):
    try:
        tickets_lock = hazelcast_client.cp_subsystem.get_lock(ticket_id)
        if tickets_lock.try_lock():
            logger.info(f"Ticket ID {ticket_id} locked successfully.")
            return True
        logger.warning(f"Ticket ID {ticket_id} is already locked.")
        return False
    except Exception as e:
        logger.error(f"Error locking ticket ID {ticket_id}: {e}")
        return False


def unlock_ticket(ticket_id):
    try:
        tickets_lock = hazelcast_client.cp_subsystem.get_lock(ticket_id)
        tickets_lock.unlock()
        logger.info(f"Ticket ID {ticket_id} unlocked successfully.")
    except Exception as e:
        logger.error(f"Error unlocking ticket ID {ticket_id}: {e}")
