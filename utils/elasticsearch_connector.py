import logging
import coloredlogs
from elasticsearch import Elasticsearch, exceptions

from utils.mongo_setup import db

ELASTICSEARCH_URL = "http://localhost:9200"
ELASTICSEARCH_USERNAME = "elastic"
ELASTICSEARCH_PASSWORD = "your_password"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('elasticsearch')
coloredlogs.install()

client = Elasticsearch(
    ELASTICSEARCH_URL,
    http_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
    request_timeout=10,
    retry_on_timeout=True,
    retry_on_status=(),
    max_retries=10,
)


def create_train_index():
    """ Создание индекса для поездов """
    try:
        body = {
            "mappings": {
                "properties": {
                    "train_id": {"type": "integer"},
                    "route_id": {"type": "integer"},
                    "departure_date": {"type": "date"},
                    "arrival_date": {"type": "date"},
                    "stations": {"type": "integer"}
                }
            }
        }
        response = client.indices.create(index="trains", body=body, ignore=400)
        logger.info("Train index created successfully.")
        return response
    except Exception as e:
        logger.error(f"Error creating train index: {e}")
        return None


async def add_train_to_index(train_data):
    """ Добавление информации о поезде в индекс """
    try:
        route_id = train_data["route_id"]
        route = await db.routes.find_one({"route_id": route_id})
        stations = route["stations"]
        train_data["stations"] = stations

        response = client.index(index="trains", body=train_data)
        logger.info("Train data added to index successfully.")
        return response
    except exceptions.Any as e:
        logger.error(f"Error adding train data to index: {e}")
        return None


def search_trains(departure_station_id, arrival_station_id, departure_date):
    """ Поиск поездов по заданным критериям """
    try:
        query = {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {"term": {"stations": departure_station_id}},
                                {"term": {"stations": arrival_station_id}}
                            ],
                            "minimum_should_match": 2
                        }
                    },
                    {"range": {"departure_date": {"gte": departure_date}}}
                ]
            }
        }
        response = client.search(index="trains", body={"query": query})
        logger.info("Search for trains executed successfully.")
        return [hit["_source"] for hit in response["hits"]["hits"]]
    except Exception as e:
        logger.error(f"Error searching trains: {e}")
        return []


def delete_train_from_index(train_id):
    """ Удаление информации о поезде из индекса по идентификатору """
    try:
        query = {
            "query": {
                "term": {"train_id": train_id}
            }
        }
        response = client.delete_by_query(index="trains", body=query)
        logger.info("Train data deleted from index successfully.")
        return response
    except exceptions.NotFoundError:
        logger.error(f"Train data not found in index for id: {train_id}")
        return None
    except Exception as e:
        logger.error(f"Error deleting train data from index: {e}")
        return None
