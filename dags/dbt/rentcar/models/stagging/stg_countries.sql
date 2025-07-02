{{ config(
    materialized = 'table',
    unique_key    = '_id', 
    schema = 'stg',
) }}

WITH raw AS (
  SELECT
    _id,
    name,
    isoCode,
    currency,
    locale
  FROM RIDE_SHARE_V1.countries
)

SELECT * FROM raw
