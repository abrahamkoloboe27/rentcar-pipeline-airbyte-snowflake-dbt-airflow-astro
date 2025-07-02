from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteConnectionTestOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

# 1. Définition des arguments par défaut
default_args = {
    'owner': 'abraham',
    'depends_on_past': False,
    'email': ['abklb27@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 2. Instanciation du DAG
with DAG(
    dag_id='test_connexions_airbyte_snowflake',
    description='Test des connexions Airbyte et Snowflake',
    default_args=default_args,
    start_date=datetime(2025, 7, 2),
    schedule_interval=None,
    catchup=False,
    tags=['airbyte', 'snowflake', 'test'],
) as dag:

    # 3. Test connexion Airbyte
    test_airbyte_conn = AirbyteConnectionTestOperator(
        task_id='test_airbyte_connection',
        airbyte_conn_id='airbyte_conn',   
    )

    # 4. Test connexion Snowflake
    test_snowflake_conn = SnowflakeOperator(
        task_id='test_snowflake_connection',
        snowflake_conn_id='rentcar_snowflake_conn', 
        sql='SELECT 1;',
    )

    # 5. Orchestration
    test_airbyte_conn >> test_snowflake_conn
