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

## Kafka Producer Script

The `producer.py` script generates fake ecommerce events and sends them to Kafka.

### Installation

Install dependencies in the Python container:

```bash
docker-compose exec python-app pip install -r requirements.txt
```

### Usage

**Basic usage (default: 1-5 seconds between events):**
```bash
docker-compose exec python-app python producer.py
```

**High load simulation (0.1-0.5 seconds between events):**
```bash
docker-compose exec python-app python producer.py --rate-min 0.1 --rate-max 0.5
```

**Produce a specific number of events:**
```bash
docker-compose exec python-app python producer.py --max-events 100
```

**Custom rate and topic:**
```bash
docker-compose exec python-app python producer.py --rate-min 2 --rate-max 5 --topic my-topic
```

### Producer Options

- `--rate-min`: Minimum seconds between events (default: 1.0)
- `--rate-max`: Maximum seconds between events (default: 5.0)
- `--max-events`: Maximum number of events to produce (default: unlimited)
- `--topic`: Kafka topic name (default: `ecommerce-events`)
- `--bootstrap-servers`: Kafka bootstrap servers (default: uses `KAFKA_BOOTSTRAP_SERVERS` env var or `kafka:9093`)

### Event Structure

Each event contains:
- `user_id`: UUID4
- `event_type`: One of "view", "add_to_cart", "purchase"
- `product`: Random word
- `timestamp`: ISO format datetime
- `amount`: Random amount between $10-$100

### Testing the Producer

1. **Start the producer** (in one terminal):
   ```bash
   docker-compose exec python-app python producer.py --max-events 10
   ```

2. **Consume messages** (in another terminal):
   ```bash
   docker-compose exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic ecommerce-events --from-beginning
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