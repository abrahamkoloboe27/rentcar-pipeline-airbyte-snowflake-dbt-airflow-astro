{{ config(
    materialized = 'incremental',
    unique_key    = '_id',
    schema = 'stg'
) }}

WITH raw AS (
  SELECT
    _id,
    vehicleId,
    type,
    description, 
    startdate::timestamp_ntz  AS started_dt,
    enddate::timestamp_ntz    AS ended_dt,
    cost
  FROM RIDE_SHARE_V1.maintenance
  -- {% if is_incremental() %}
  --   WHERE reportedAt >= DATEADD(day, -1, CURRENT_TIMESTAMP())
  -- {% endif %}
)
SELECT * FROM raw
