{{ 
  config(
    materialized='table', 
    unique_key='_id',
    schema = 'silver'
  ) 
}}

WITH src AS (
  SELECT
    _id,
    vehicleId,
    type,
    reported_dt,
    started_dt,
    ended_dt,
    cost,
    description,
    -- mechanic,
    DATEDIFF('hour', started_dt, ended_dt) AS laborHours,
    CASE WHEN DATEDIFF('day', started_dt, ended_dt) >= 1 THEN 'completed' ELSE 'ongoing' END AS status
  FROM {{ ref('stg_maintenance') }}
  -- {% if is_incremental() %}
  --   WHERE reported_dt >= DATEADD(day, -1, CURRENT_TIMESTAMP())
  -- {% endif %}
),

cleaned_maintenance AS (
  SELECT
    _id,
    vehicleId,
    type,
    reported_dt,
    started_dt,
    ended_dt,
    cost,
    description,
    -- mechanic:name    AS mechanic_name,
    -- mechanic:contact AS mechanic_contact,
    laborHours,
    status,
    DATEDIFF(hour, started_dt, ended_dt)    AS maintenance_hours
    --DATE_TRUNC('day', reported_dt)          AS maintenance_date
  FROM src
)

SELECT * FROM cleaned_maintenance
