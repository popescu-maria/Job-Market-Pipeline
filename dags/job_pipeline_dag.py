from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "maria",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="job_market_ingestion",
    default_args=default_args,
    start_date=datetime(2026, 8, 1),
    schedule="@hourly",
    catchup=False,
) as dag:
    BashOperator(
        task_id="run_ingestion",
        bash_command="cd /opt/airflow && PYTHONPATH=/opt/airflow python -m src.ingestion.main",
    )