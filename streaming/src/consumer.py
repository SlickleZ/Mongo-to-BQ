from kafka import KafkaConsumer, TopicPartition
import json


try:
    print("Starting the consumer...")
    consumer = KafkaConsumer(
        "lottery.preference", 
        bootstrap_servers=["broker:29092"],
        auto_commit_interval_ms=500,
        group_id="consumer-group-bq")

    for msg in consumer:
        msg_json = json.loads(msg.value)
        print(f"Message received: {msg_json}")
        print(f"The last committed offset: {consumer.committed(TopicPartition('lottery.preference', 0))}")
except Exception as e:
    print(e)