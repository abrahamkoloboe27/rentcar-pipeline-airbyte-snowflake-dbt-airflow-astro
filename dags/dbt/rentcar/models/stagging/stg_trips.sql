{{ config(
    materialized = 'table',
    unique_key    = '_id',
    schema = 'stg'
) }}

WITH raw AS (
  SELECT
    _id,
    serviceType,
    userId,
    driverId,
    vehicleId,
    origin,
    destination,
    requestedAt::timestamp_ntz AS requested_dt,
    acceptedAt::timestamp_ntz  AS accepted_dt,
    startedAt::timestamp_ntz   AS started_dt,
    endedAt::timestamp_ntz     AS ended_dt,
    status,
    amount,
    fare,
    serviceDetails,
    currency
  FROM RIDE_SHARE_V1.trips
  -- {% if is_incremental() %}
  --   WHERE requestedAt >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
  -- {% endif %}
)

SELECT * FROM raw
