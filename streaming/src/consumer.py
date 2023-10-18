from kafka import KafkaConsumer, TopicPartition
from google.cloud import bigquery
from google.oauth2 import service_account
from os import getenv
from datetime import datetime
from zoneinfo import ZoneInfo
import json


# BigQuery config
SCOPES = ["https://www.googleapis.com/auth/bigquery"]
SERVICE_ACCOUNT_FILE = "gsa.json"
BQ_PROJECT = getenv("GCP_PROJECT_ID")
BQ_DATASET = "bq_dataset_kafka"
BQ_TABLE_NAME = "lottery_preference"


try:
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    bqClient = bigquery.Client(credentials=credentials)

    consumer = KafkaConsumer(
        "lottery.preference", 
        bootstrap_servers=["broker:29092"],
        auto_commit_interval_ms=500,
        group_id="consumer-group-bq"
    )
    print("Start to consume messages...")

    for msg in consumer:
        msg_json = [json.loads(msg.value)]
        msg_json[0]["_id"] = msg_json[0]["_id"]["$oid"]
        timestamp_bangkok = datetime.strptime(msg_json[0]["event_timestamp"]["$date"], "%Y-%m-%dT%H:%M:%S.%fZ").astimezone(ZoneInfo("Asia/Bangkok"))
        msg_json[0]["event_timestamp"] = timestamp_bangkok.strftime("%Y-%m-%d %H:%M:%S")

        print(f"Message received: {msg_json}")
        print(f"The last committed offset: {consumer.committed(TopicPartition('lottery.preference', 0))}")

        errors = bqClient.insert_rows_json(
            f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_NAME}",
            msg_json
        )
        if errors == []:
            print("New rows have been added into BigQuery.")
        else:
            print(f"Encountered errors while inserting rows: {errors}")

except Exception as e:
    print(e)