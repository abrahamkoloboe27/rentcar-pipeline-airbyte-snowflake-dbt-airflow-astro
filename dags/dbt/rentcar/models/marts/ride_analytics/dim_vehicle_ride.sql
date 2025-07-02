{{ 
  config(
    materialized = 'table',
    schema = 'marts_ride'
  ) 
}}

SELECT
  _id                      AS vehicle_key,
  driverId                 AS driver_key,   -- link back to dim_driver
  brand_clean              AS make,
  model_clean              AS model,
  plate_clean              AS plate_number,
  year                     AS model_year,
  mileageKm               AS current_mileage,
  vehicle_age              AS age_years,
  status_clean             AS vehicle_status,
  acquisitionDate         AS acquisition_date
FROM {{ ref('silver_vehicles') }}
