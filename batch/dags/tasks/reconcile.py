from google.cloud import bigquery
from google.oauth2 import service_account
from os import getenv
from datetime import datetime, timedelta


def reconcile(execution_date, **context):
    # BigQuery config
    SCOPES = ["https://www.googleapis.com/auth/bigquery"]
    SERVICE_ACCOUNT_FILE = "/opt/airflow/dags/gsa.json"
    BQ_PROJECT = getenv("GCP_PROJECT_ID")
    BQ_DATASET = "bq_dataset_kafka"
    BQ_TABLE_NAME = "lottery_logs"

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    bqClient = bigquery.Client(credentials=credentials)
    
    PARTITION_DATE = execution_date - timedelta(hours=24)
    QUERY = (
        f"SELECT COUNT(*) FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_NAME}` "
        f"WHERE TIMESTAMP_TRUNC(created_timestamp, DAY) = TIMESTAMP(\"{PARTITION_DATE.strftime('%Y-%m-%d')}\")"
    )
    
    query_job = bqClient.query(QUERY)
    rows_count = query_job.result()
    source_count = context["ti"].xcom_pull(key="lottery_mongo_count")
    
    for row in rows_count:
        print(f"Source count: {source_count}, Target count: {row[0]}")
        assert row[0] == source_count, "Target count rows does not equal to source count rows"