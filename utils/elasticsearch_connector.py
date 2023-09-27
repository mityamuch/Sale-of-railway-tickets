from elasticsearch import Elasticsearch

ELASTICSEARCH_URL = "http://localhost:9200"

es_client = Elasticsearch(ELASTICSEARCH_URL)