from config import LOCAL_ELASTIC_HOST
from dbi.elastic.elasticsearch_client import ElasticsearchClient

# replace this using proper management tools like Terraform, for now LOCAL_ELASTIC_HOST is a workaround for simplicity
if __name__ == "__main__":
    client = ElasticsearchClient(host=LOCAL_ELASTIC_HOST)
    client.create_index()
