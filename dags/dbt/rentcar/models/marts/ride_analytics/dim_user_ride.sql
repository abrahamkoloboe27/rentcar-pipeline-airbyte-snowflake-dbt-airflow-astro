{{ config(
    materialized='table',
    schema = 'marts_ride'
) }}

WITH users AS (
  SELECT
    _id        AS user_key,
    fullname  AS user_name,
    email AS email,
    phonenumber AS phone,
    signup_dt  AS signup_date,
    countryid  AS country_key
    -- status     AS user_status
  FROM {{ ref('silver_users') }}
),
countries AS (
  SELECT * FROM {{ ref('dim_country') }}
)

SELECT
  u.user_key,
  u.user_name,
  u.email,
  u.phone,
  u.signup_date,
  --u.user_status,
  c.country_name,
  c.country_iso,
  c.currency_code,
  c.locale
FROM users u
LEFT JOIN countries c
  ON u.country_key = c.country_key
