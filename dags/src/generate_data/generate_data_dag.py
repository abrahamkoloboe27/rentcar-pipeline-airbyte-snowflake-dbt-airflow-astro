import os 
import sys
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

logging.info(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from create_index_mongo import generate_index
from create_data_mongo import generate_data_all
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'abraham',
    'depends_on_past': False,
    'email': ['abklb27@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='generate_data_dag',
    description='This dag generate synthetic data to MongoDB Atlas',
    default_args=default_args,
    #start_date=datetime(2025, 7, 2),
    catchup=False,
    #schedule="@daily",
    tags=['generate_data','create_index', "rentcar"],
) as dag:

    generate_data_task = PythonOperator(
        task_id='generate_data_task',
        python_callable=generate_data_all,
    )

    create_index_task = PythonOperator(
        task_id='create_index_task',
        python_callable=generate_index,
    )

    generate_data_task >> create_index_task