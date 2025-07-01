{{ config(
    materialized='table',
    schema = 'marts_ride'
) }}

SELECT
  country_key,
  country_name,
  country_iso,
  currency_code,
  locale
FROM {{ ref('silver_countries') }}

