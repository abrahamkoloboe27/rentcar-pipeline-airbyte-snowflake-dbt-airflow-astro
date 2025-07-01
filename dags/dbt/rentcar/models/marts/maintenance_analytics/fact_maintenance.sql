{{ 
  config(
    materialized = 'table',
    schema = 'marts_maintenance'
  ) 
}}

SELECT
  m._id                     AS maintenance_key,
  DATE_TRUNC('day', m.reported_dt) AS date_key,
  m.vehicleId               AS vehicle_key,
  m.cost                    AS maintenance_cost,
  m.maintenance_hours       AS maintenance_duration_hours,
  m.status                  AS maintenance_status
FROM {{ ref('silver_maintenance') }} AS m
