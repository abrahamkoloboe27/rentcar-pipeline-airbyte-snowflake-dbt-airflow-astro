FROM astrocrpublic.azurecr.io/runtime:3.0-4

RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir astronomer-cosmos dbt-core dbt-postgres dbt-snowflake apache-airflow-providers-snowflake apache-airflow-providers-airbyte && deactivate
