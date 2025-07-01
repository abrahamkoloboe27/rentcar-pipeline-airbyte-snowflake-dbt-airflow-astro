{{ config(
    materialized='table',
    schema = 'silver'
) }}

SELECT
  _id            AS country_key,
  name           AS country_name,
  isoCode        AS country_iso,
  currency       AS currency_code,
  locale         AS locale
FROM {{ ref('stg_countries') }}

