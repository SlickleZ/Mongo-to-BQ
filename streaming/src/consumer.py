from kafka import KafkaConsumer
import json
import logging


_logger = logging.getLogger(__name__)

if __name__ == "__main__":
    consumer = KafkaConsumer(
        "lottery.preference", 
        bootstrap_servers=['broker:9092'],
        auto_offset_reset="earliest",
        group_id="consumer-group-bq")
    _logger.info("Starting the consumer...")
    for msg in consumer:
        msg_json = json.loads(msg.value)
        print(f"Registered User: {msg_json.get('name')}, Address: {msg_json.get('address')}")