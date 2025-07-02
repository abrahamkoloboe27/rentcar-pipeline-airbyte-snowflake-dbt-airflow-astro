from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.airbyte.hooks.airbyte import AirbyteHook
from airflow.operators.python import PythonOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator

default_args = {
    'owner': 'abraham',
    'depends_on_past': False,
    'email': ['abklb27@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='test_connexions_airbyte_snowflake',
    description='Test des connexions Airbyte et Snowflake',
    default_args=default_args,
    start_date=datetime(2025, 7, 2),
    schedule_interval=None,
    catchup=False,
    tags=['airbyte', 'test'],
) as dag:

    test_airbyte_conn = PythonOperator(
        task_id='test_airbyte_connection',
        python_callable=lambda: AirbyteHook(airbyte_conn_id="airbyte_conn").test_connection(),
    )

    trigger_airbyte = AirbyteTriggerSyncOperator(
        task_id='trigger_airbyte_sync',
        airbyte_conn_id='airbyte_conn',
        connection_id='YOUR_UUID_HERE',
        asynchronous=False,
    )


    test_airbyte_conn >> trigger_airbyte 
