{{ 
  config(
    materialized = 'table',
    schema = 'marts_ride'
  ) 
}}

SELECT
  _id                      AS vehicle_key,
  driverId                 AS driver_key,   -- link back to dim_driver
  vehicle_type             AS type,
  make_clean               AS make,
  model_clean              AS model,
  year                     AS model_year,
  mileageKm                AS current_mileage,
  vehicle_age              AS age_years,
  status                   AS vehicle_status
FROM {{ ref('silver_vehicles') }}
