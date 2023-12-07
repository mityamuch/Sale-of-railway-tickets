import coloredlogs
from elasticsearch import Elasticsearch
import logging

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
logger.info("ElasticSearch: " + str(client.info()))


def create_train_index():
    """ Создание индекса для поездов """
    try:
        body = {
            "mappings": {
                "properties": {
                    "departure_station_id": {"type": "integer"},
                    "arrival_station_id": {"type": "integer"},
                    "departure_date": {"type": "date"}
                    # ... другие поля ...
                }
            }
        }
        response = client.indices.create(index="trains", body=body, ignore=400)
        logger.info("Train index created successfully.")
        return response
    except Exception as e:
        logger.error(f"Error creating train index: {e}")
        return None


def add_train_to_index(train_data):
    """ Добавление информации о поезде в индекс """
    try:
        response = client.index(index="trains", body=train_data)
        logger.info("Train data added to index successfully.")
        return response
    except Exception as e:
        logger.error(f"Error adding train data to index: {e}")
        return None


def search_trains(departure_station_id, arrival_station_id, departure_date):
    """ Поиск поездов по заданным критериям """
    try:
        query = {
            "bool": {
                "must": [
                    {"match": {"departure_station_id": departure_station_id}},
                    {"match": {"arrival_station_id": arrival_station_id}},
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
