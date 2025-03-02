- install docker

- check if not in dockers dir, if not cd to it
```bash
cd dockers
```
# Create a local network
   ```bash
   docker network create my_network
   ```

# PostgreSQL Setup Instructions

1. Pull the PostgreSQL Docker image:
   ```bash
   docker build -t my_postgres_image -f Dockerfile_sql .
   ```

2. Run the PostgreSQL container:
   ```bash
   docker run --name my_postgres_container -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=celery_db -p 5432:5432 -d --network my_network my_postgres_image
   ```

# Elastic Setup Instructions

1. Pull the Elastic Docker image:
   ```bash
    docker pull docker.elastic.co/elasticsearch/elasticsearch:8.6.0
    ```

2. Run the Elastic container:
   ```bash
   docker run --name elasticsearch --network my_network -d -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.transport.ssl.enabled=false" -p 9200:9200 -p 9300:9300 docker.elastic.co/elasticsearch/elasticsearch:8.6.0
   ```

3. Once the container is running, you can execute the Python script to interact with the Elastic database:
   ```
   python initiators/init_elastic.py
   ```
   - this could take some seconds since the elastic server could still be booting up


# Elastic Setup Instructions

- cehck if not in source dir, if not cd to it
```bash
cd..
```

# App SetUp Instructions
1. Build the docker for the api:
   ```bash
   docker build -f dockers/Dockerfile_api -t fastapi-server .
   ```

2. Run the PostgreSQL container:
   ```bash
   docker run -d -p 8000:8000 --network my_network fastapi-server
   ```