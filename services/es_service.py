from utils.elasticsearch_connector import es_client


def create_train_index():
    es_client.indices.create(
        index="trains",
        body={
            "mappings": {
                "properties": {
                    "departure_station_id": {"type": "integer"},
                    "arrival_station_id": {"type": "integer"},
                    "departure_date": {"type": "date"}
                    # ... другие поля ...
                }
            }
        }
    )


def add_train_to_index(train_data):
    es_client.index(index="trains", body=train_data)


def search_trains(departure_station_id, arrival_station_id, departure_date):
    query = {
        "bool": {
            "must": [
                {"match": {"departure_station_id": departure_station_id}},
                {"match": {"arrival_station_id": arrival_station_id}},
                {"range": {"departure_date": {"gte": departure_date}}}
            ]
        }
    }

    response = es_client.search(index="trains", body={"query": query})
    return [hit["_source"] for hit in response["hits"]["hits"]]