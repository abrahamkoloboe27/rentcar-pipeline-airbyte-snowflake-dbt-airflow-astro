{{ 
  config(
    materialized = 'table',
    schema = 'marts_maintenance'
  ) 
}}

SELECT
  v._id                     AS vehicle_key,
  v.driverid               AS driver_id,
  v.brand_clean            AS make,
  v.model_clean            AS model,
  v.plate_clean            AS plate_number,
  v.status_clean           AS status,
  v.year                   AS manufacture_year,
  v.mileagekm              AS mileage_km,
  v.vehicle_age            AS age_years,
  v.acquisitiondate        AS acquisition_date,
  v.type                   AS vehicle_type
FROM {{ ref('silver_vehicles') }} AS v
