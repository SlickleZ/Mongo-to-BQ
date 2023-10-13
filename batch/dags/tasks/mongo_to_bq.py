from pymongo.mongo_client import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2 import service_account
from os import getenv


def load_mongo_to_bq(execution_date, **context):
    # BigQuery config
    SCOPES = ["https://www.googleapis.com/auth/bigquery"]
    SERVICE_ACCOUNT_FILE = "/opt/airflow/dags/gsa.json"
    BQ_PROJECT = getenv("GCP_PROJECT_ID")
    BQ_DATASET = "bq_dataset_kafka"
    BQ_TABLE_NAME = "lottery_logs"

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    bqClient = bigquery.Client(credentials=credentials)
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        schema=[
            bigquery.SchemaField("_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("user_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("lottery_number", "STRING"),
            bigquery.SchemaField("created_timestamp", "TIMESTAMP", mode="REQUIRED"),
        ],
    )
    client = MongoClient("mongodb://mongodb:27017/?replicaSet=rs0")

    try:
        client.admin.command("ping")
        db = client.get_database(name="lottery")

        prev_execution_date = execution_date - timedelta(hours=24)
        print(f"Load data for date: {prev_execution_date}")
        data_to_load = db.logs.find({
            "created_timestamp": {
                "$gte": prev_execution_date,
                "$lt": execution_date
            }
        })

        list_of_data = []
        for data in data_to_load:
            data["_id"] = str(data["_id"])
            data["lottery_number"] = str(data["lottery_number"])
            data["created_timestamp"] = data["created_timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            list_of_data.append(data)
        print(f"Result: {list_of_data}")

        if list_of_data:
            job = bqClient.load_table_from_json(
                list_of_data,
                f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_NAME}${prev_execution_date.strftime('%Y%m%d')}",
                job_config=job_config
            )
            job.result()

        context["ti"].xcom_push(key="lottery_mongo_count", value=len(list_of_data))
    except PyMongoError as e:
        raise(e)