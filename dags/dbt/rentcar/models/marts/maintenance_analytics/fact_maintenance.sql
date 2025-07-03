{{ 
  config(
    materialized = 'table',
    schema = 'marts_maintenance'
  ) 
}}

SELECT
  m._id                     AS maintenance_key,
  DATE_TRUNC('day', m.started_dt) AS date_key,
  m.vehicleId              AS vehicle_key,
  m.type                   AS maintenance_type,
  m.started_dt             AS maintenance_start_date,
  m.ended_dt               AS maintenance_end_date,
  m.cost                   AS maintenance_cost,
  m.description            AS maintenance_description,
  m.laborhours             AS labor_hours,
  m.maintenance_hours      AS maintenance_duration_hours,
  m.status                 AS maintenance_status,
  m.reported_dt            AS reported_date
FROM {{ ref('silver_maintenance') }} AS m
