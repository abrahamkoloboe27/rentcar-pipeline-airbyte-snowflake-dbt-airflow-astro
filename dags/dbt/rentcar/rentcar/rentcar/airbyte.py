# airbyte.py
from dagster_airbyte import build_airbyte_assets_definitions
from .resources import airbyte_cloud

# Génère un asset par connexion Airbyte dans ton workspace Cloud
airbyte_connection_assets = build_airbyte_assets_definitions(
    workspace=airbyte_cloud,
    #connection_id="2b7ee052-8dc1-42eb-8084-f125cb14473a",
)
