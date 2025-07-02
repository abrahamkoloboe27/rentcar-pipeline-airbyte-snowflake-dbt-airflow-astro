from datetime import datetime, timedelta
import os
import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException

# Liste des variables d'environnement à vérifier
REQUIRED_ENV_VARS = [
    'MONGODB_URI',
    'DB_NAME',
    'BATCH_SIZE',
    'NB_COUNTRIES',
    'NB_CITIES',
    'NB_USERS',
    'NB_DRIVERS',
    'NB_VEHICLES',
    'NB_TRIPS',
    'NB_MAINTENANCE',
]

def check_env_vars(**kwargs):
    """
    Vérifie que toutes les variables d'environnement requises sont définies et non vides.
    En cas d'absence ou de valeur vide, provoque un échec du DAG.
    """
    missing_vars = []
    for var in REQUIRED_ENV_VARS:
        value = os.getenv(var)
        if value is None or value == '':
            missing_vars.append(var)
        else:
            logging.info(f"Variable {var} = {value}")

    if missing_vars:
        error_msg = f"Variables manquantes ou vides : {', '.join(missing_vars)}"
        logging.error(error_msg)
        raise AirflowFailException(error_msg)
    logging.info("Toutes les variables d'environnement sont correctement définies.")

# Définition du DAG
default_args = {
    'owner': 'abraham',
    'depends_on_past': False,
    'email': ['abklb27@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='check_env_vars_dag',
    description='Vérifie que les variables d\'environnement sont correctement définies',
    default_args=default_args,
    start_date=datetime(2025, 7, 2),
    #schedule_interval='@daily',
    catchup=False,
    tags=['env_check', 'rentcar'],
) as dag:

    task_check_env = PythonOperator(
        task_id='check_environment_variables',
        python_callable=check_env_vars,
        provide_context=True,
    )

    task_check_env
