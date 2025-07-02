from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from .project import rentcar_project
from dagster_airbyte import airbyte_assets
from .resources import airbyte_workspace
from dagster_airbyte import AirbyteCloudWorkspace
import dagster as dg

@airbyte_assets(
    connection_id="2b7ee052-8dc1-42eb-8084-f125cb14473a", 
    workspace=airbyte_workspace,
    name="mongodb_atlas_to_snowflake",  
    group_name="mongodb_atlas_to_snowflake",
)
def airbyte_connection_assets(
    context: dg.AssetExecutionContext, airbyte: AirbyteCloudWorkspace
):
    yield from airbyte.sync_and_poll(context=context)

@dbt_assets(
    manifest=rentcar_project.manifest_path,
    name="rentcar_dbt_assets",
)
def rentcar_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()





    

