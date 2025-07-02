from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import airbyte_connection_assets, rentcar_dbt_assets
from .project import rentcar_project
from .schedules import schedules
from .resources import *

defs = Definitions(
    assets=[
            airbyte_connection_assets, 
            rentcar_dbt_assets, 
            ],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=rentcar_project),
        "airbyte": airbyte_workspace
    },
)
