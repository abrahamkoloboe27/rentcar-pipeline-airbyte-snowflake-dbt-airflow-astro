{{ 
  config(
    materialized = 'table',
    schema = 'marts_maintenance'
  ) 
}}

SELECT
  v._id                     AS vehicle_key,
  v.vehicle_type            AS type,
  v.make_clean              AS make,
  v.model_clean             AS model
FROM {{ ref('silver_vehicles') }} AS v
