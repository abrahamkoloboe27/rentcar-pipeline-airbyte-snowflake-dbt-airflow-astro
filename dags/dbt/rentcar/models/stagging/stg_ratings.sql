{{ config(
    materialized = 'incremental',
    unique_key    = '_id',
    schema = 'stg'
) }}

WITH raw AS (
  SELECT
    _id,
    tripid,
    toid,
    stars,
    comment,
    givenby,
    createdAt::timestamp_ntz AS created_dt
  FROM RIDE_SHARE_V1.ratings
  -- {% if is_incremental() %}
  --   WHERE createdAt >= DATEADD(day, -1, CURRENT_TIMESTAMP())
  -- {% endif %}
)

SELECT * FROM raw
