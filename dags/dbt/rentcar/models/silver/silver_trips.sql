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
    serviceType,
    userId,
    driverId,
    vehicleId,
    requested_dt,
    accepted_dt,
    started_dt,
    ended_dt,
    status,
    fare:amount       AS amount,
    fare:currency     AS currency,
    serviceDetails:rentalDurationMins    AS rental_mins,
    serviceDetails:packageWeightKg       AS weight_kg
  FROM {{ ref('stg_trips') }}
  {% if is_incremental() %}
    WHERE requested_dt >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
  {% endif %}
),

cleaned AS (
  SELECT
    _id,
    serviceType,
    userId,
    driverId,
    vehicleId,
    requested_dt,
    accepted_dt,
    started_dt,
    ended_dt,
    DATEDIFF(second, started_dt, ended_dt)/60.0  AS duration_min,
    status,
    amount,
    currency,
    rental_mins,
    weight_kg,
    DATE_TRUNC('day', requested_dt)         AS trip_date,
    EXTRACT(hour FROM requested_dt)         AS trip_hour,
    CASE WHEN serviceType = 'ride' THEN 'ride' ELSE serviceType END AS service_type_clean
  FROM src
)

SELECT * FROM cleaned
