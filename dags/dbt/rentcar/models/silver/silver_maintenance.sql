{{ 
  config(
    materialized='incremental', 
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
    mechanic,
    laborHours,
    status
  FROM {{ ref('stg_maintenance') }}
  {% if is_incremental() %}
    WHERE reported_dt >= DATEADD(day, -1, CURRENT_TIMESTAMP())
  {% endif %}
),

cleaned AS (
  SELECT
    _id,
    vehicleId,
    type,
    reported_dt,
    started_dt,
    ended_dt,
    cost,
    description,
    mechanic:name    AS mechanic_name,
    mechanic:contact AS mechanic_contact,
    laborHours,
    status,
    DATEDIFF(hour, started_dt, ended_dt)    AS maintenance_hours,
    DATE_TRUNC('day', reported_dt)          AS maintenance_date
  FROM src
)

SELECT * FROM cleaned
