{{ 
  config(
    materialized = 'table',
    schema = 'marts_ride'
  ) 
}}

SELECT
  _id                      AS driver_key,
  userId                   AS user_key,    -- link back to dim_user
  license_no               AS license_number,
  license_expiry_dt        AS expiry_date,
  days_to_expiry           AS days_until_expiry,
  status                   AS driver_status,
  joined_dt                AS joined_date
FROM {{ ref('silver_drivers') }}
