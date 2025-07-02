{{ 
  config(
    materialized = 'table',
    schema = 'marts_rating'
  ) 
}}

SELECT
  d._id                     AS driver_key,
  d.user_id                  AS user_key,
  d.license_no              AS license_number,
  d.status                  AS driver_status,
  d.joined_dt              AS joined_date
FROM {{ ref('silver_drivers') }} AS d
