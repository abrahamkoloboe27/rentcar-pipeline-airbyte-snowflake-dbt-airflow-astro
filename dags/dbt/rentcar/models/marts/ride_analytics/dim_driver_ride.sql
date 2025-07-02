{{ 
  config(
    materialized = 'table',
    schema = 'marts_ride'
  ) 
}}

SELECT
  _id                      AS driver_key,
  user_id                  AS user_key,    -- link back to dim_user
  license_no               AS license_number,
  status                   AS driver_status,
  joined_dt                AS joined_date
FROM {{ ref('silver_drivers') }}
