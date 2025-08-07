# Airflow DAG that orchestrates the ETL pipeline: extract CSV → transform with Spark → load to MinIO
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
sys.path.append('/opt/airflow/src')
from src.etl import extract, transform, load

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='mini_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for sales data processing',
    schedule_interval=timedelta(days=1),
    catchup=False,
    max_active_runs=1,
    tags=['etl', 'sales']
)

extract_task = PythonOperator(
    task_id='extract_csv_to_parquet',
    python_callable=extract,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_calculate_top_products',
    python_callable=transform,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_to_minio',
    python_callable=load,
    dag=dag
)

extract_task >> transform_task >> load_task