{{ 
  config(
    materialized = 'table',
    schema = 'marts_ride'
  ) 
}}

SELECT
  t._id                        AS trip_key,
  DATE_TRUNC('day', t.requested_dt) AS date_key,
  t.userId                     AS user_key,
  t.driverId                   AS driver_key,
  t.vehicleId                  AS vehicle_key,
  t.duration_min               AS duration_minutes,
  t.amount                     AS fare_amount,
  t.currency                   AS fare_currency,
  t.weight_kg                  AS package_weight,
  t.rental_mins                AS rental_duration,
  t.serviceType                AS service_type,
  t.status                     AS trip_status,
  t.requested_dt               AS requested_date,
  t.started_dt                 AS started_date,
  t.ended_dt                   AS ended_date
FROM {{ ref('silver_trips') }} AS t
