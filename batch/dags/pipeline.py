from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta, datetime
from tasks.mongo_to_bq import load_mongo_to_bq
from tasks.reconcile import reconcile
from time import tzset


tzset()

default_args = {
    "owner": "SlickleZ",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    dag_id="load_lottery_logs",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    start_date=datetime.now() - timedelta(days=1),
    tags=["mongodb", "bigquery"]
)

mongo_to_bq = PythonOperator(
    task_id="mongo-to-bq",
    python_callable=load_mongo_to_bq,
    op_kwargs={'execution_date': datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)},
    dag=dag
)

reconcile = PythonOperator(
    task_id="reconcile",
    python_callable=reconcile,
    op_kwargs={'execution_date': datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)},
    dag=dag
)

mongo_to_bq >> reconcile