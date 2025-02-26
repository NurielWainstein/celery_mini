from dbi.elastic.elasticsearch_client import ElasticsearchClient

if __name__ == "__main__":
    client = ElasticsearchClient()
    client.create_index()
