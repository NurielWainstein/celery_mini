
# PostgreSQL Setup Instructions

1. Pull the PostgreSQL Docker image:
   ```bash
   docker pull postgres
   ```

2. Run the PostgreSQL container:
   ```bash
   docker run --name postgres-server -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=celery_db -p 5432:5432 -d postgres
   ```

3. Once the container is running, you can execute the Python script to interact with the PostgreSQL database:
   ```bash
   python initiators/init_sql.py
   ```

# Elastic Setup Instructions

1. Pull the Elastic Docker image:
   ```bash
    docker pull docker.elastic.co/elasticsearch/elasticsearch:8.6.0
    ```

2. Run the Elastic container:
   ```bash
    docker run --name elasticsearch -d -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.transport.ssl.enabled=false" -p 9200:9200 -p 9300:9300 docker.elastic.co/elasticsearch/elasticsearch:8.6.0
    ```

3. Once the container is running, you can execute the Python script to interact with the Elastic database:
   ```
   python initiators/init_elastic.py
   ```
