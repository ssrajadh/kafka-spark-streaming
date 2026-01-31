#!/usr/bin/env python3
"""
Kafka Producer Script for Ecommerce Events
Generates fake ecommerce events and sends them to Kafka topic 'ecommerce-events'
"""

import json
import random
import time
import argparse
from datetime import datetime
from faker import Faker
from kafka import KafkaProducer
from kafka.errors import KafkaError
import os

# Initialize Faker
fake = Faker()

# Kafka configuration from environment variables
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'ecommerce-events')

# Event types
EVENT_TYPES = ["view", "add_to_cart", "purchase"]


def generate_event():
    """Generate a fake ecommerce event"""
    event = {
        "user_id": str(fake.uuid4()),
        "event_type": random.choice(EVENT_TYPES),
        "product": fake.word(),
        "timestamp": datetime.now().isoformat(),
        "amount": round(random.uniform(10, 100), 2)
    }
    return event


def create_producer(bootstrap_servers):
    """Create and return a Kafka producer"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            # Optional: Add retry and timeout configurations
            retries=3,
            acks='all',  # Wait for all replicas to acknowledge
            compression_type='gzip'  # Compress messages
        )
        print(f"✓ Connected to Kafka at {bootstrap_servers}")
        return producer
    except KafkaError as e:
        print(f"✗ Failed to create Kafka producer: {e}")
        raise


def produce_events(producer, topic, rate_min=1, rate_max=5, max_events=None):
    """
    Produce events to Kafka topic
    
    Args:
        producer: KafkaProducer instance
        topic: Kafka topic name
        rate_min: Minimum seconds between events
        rate_max: Maximum seconds between events
        max_events: Maximum number of events to produce (None for infinite)
    """
    event_count = 0
    
    print(f"\nStarting to produce events to topic '{topic}'")
    print(f"   Rate: {rate_min}-{rate_max} seconds between events")
    if max_events:
        print(f"   Max events: {max_events}")
    else:
        print(f"   Running indefinitely (Ctrl+C to stop)")
    print("-" * 60)
    
    try:
        while True:
            if max_events and event_count >= max_events:
                print(f"\n✓ Produced {event_count} events. Stopping.")
                break
            
            # Generate event
            event = generate_event()
            
            # Send to Kafka
            try:
                future = producer.send(topic, event)
                # Wait for the send to complete (optional, for error checking)
                record_metadata = future.get(timeout=10)
                
                event_count += 1
                print(f"[{event_count}] Event sent: {event['event_type']:15} | "
                      f"User: {event['user_id'][:8]}... | "
                      f"Product: {event['product']:15} | "
                      f"Amount: ${event['amount']:.2f} | "
                      f"Partition: {record_metadata.partition}, Offset: {record_metadata.offset}")
                
            except KafkaError as e:
                print(f"✗ Failed to send event: {e}")
            
            # Wait for next event (random interval between rate_min and rate_max)
            wait_time = random.uniform(rate_min, rate_max)
            time.sleep(wait_time)
            
    except KeyboardInterrupt:
        print(f"\n\nInterrupted by user. Produced {event_count} events total.")
    except Exception as e:
        print(f"\n✗ Error: {e}")
    finally:
        producer.flush()  # Ensure all messages are sent
        producer.close()
        print("✓ Producer closed.")


def main():
    parser = argparse.ArgumentParser(
        description='Generate fake ecommerce events and send to Kafka',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Produce events with default rate (1-5 seconds)
  python producer.py

  # Produce events every 0.5-2 seconds (high load)
  python producer.py --rate-min 0.5 --rate-max 2

  # Produce exactly 100 events
  python producer.py --max-events 100

  # High load: 1000 events with 0.1-0.5 second intervals
  python producer.py --rate-min 0.1 --rate-max 0.5 --max-events 1000
        """
    )
    
    parser.add_argument(
        '--rate-min',
        type=float,
        default=1.0,
        help='Minimum seconds between events (default: 1.0)'
    )
    
    parser.add_argument(
        '--rate-max',
        type=float,
        default=5.0,
        help='Maximum seconds between events (default: 5.0)'
    )
    
    parser.add_argument(
        '--max-events',
        type=int,
        default=None,
        help='Maximum number of events to produce (default: unlimited)'
    )
    
    parser.add_argument(
        '--topic',
        type=str,
        default=KAFKA_TOPIC,
        help=f'Kafka topic name (default: {KAFKA_TOPIC})'
    )
    
    parser.add_argument(
        '--bootstrap-servers',
        type=str,
        default=KAFKA_BOOTSTRAP_SERVERS,
        help=f'Kafka bootstrap servers (default: {KAFKA_BOOTSTRAP_SERVERS})'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.rate_min < 0 or args.rate_max < 0:
        print("✗ Error: Rate values must be non-negative")
        return
    
    if args.rate_min > args.rate_max:
        print("✗ Error: rate-min must be <= rate-max")
        return
    
    # Create producer and start producing
    try:
        producer = create_producer(args.bootstrap_servers)
        produce_events(
            producer,
            args.topic,
            rate_min=args.rate_min,
            rate_max=args.rate_max,
            max_events=args.max_events
        )
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
