# kafka-spark-streaming

## Docker Compose Setup

This project uses Docker Compose to orchestrate all required services for Kafka-Spark streaming.

### Services

The `docker-compose.yml` file defines the following services:

- **Zookeeper** - Required for Kafka coordination
- **Kafka** - Message broker for streaming data
- **PostgreSQL** - Database for storing processed data
- **Spark Master** - Spark cluster master node
- **Spark Worker** - Spark cluster worker node
- **Python App** - Container for running Python streaming scripts

### Quick Start

1. **Start all services:**
   ```bash
   docker-compose up -d
   ```

2. **Stop all services:**
   ```bash
   docker-compose down
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f [service-name]
   ```

4. **Access Python container:**
   ```bash
   docker-compose exec python-app bash
   ```

### Service Endpoints

- **Kafka**: `localhost:9092` (from host) or `kafka:9093` (from containers)
- **Zookeeper**: `localhost:2181`
- **PostgreSQL**: `localhost:5432`
  - Database: `kafka_spark_db`
  - Username: `postgres`
  - Password: `postgres`
- **Spark Master UI**: `http://localhost:8080`
- **Spark Master**: `spark://spark-master:7077` (from containers)

### Environment Variables

The Python container is pre-configured with the following environment variables:

- `KAFKA_BOOTSTRAP_SERVERS=kafka:9093`
- `POSTGRES_HOST=postgres`
- `POSTGRES_PORT=5432`
- `POSTGRES_DB=kafka_spark_db`
- `POSTGRES_USER=postgres`
- `POSTGRES_PASSWORD=postgres`
- `SPARK_MASTER=spark://spark-master:7077`

### Working with the Python Container

The Python container has your project directory mounted at `/app`. To install dependencies:

```bash
docker-compose exec python-app pip install -r requirements.txt
```

To run your Python scripts:

```bash
docker-compose exec python-app python your_script.py
```

### Useful Commands

- **Restart a specific service:**
  ```bash
  docker-compose restart [service-name]
  ```

- **View status of all services:**
  ```bash
  docker-compose ps
  ```

- **Remove all containers and volumes:**
  ```bash
  docker-compose down -v
  ```