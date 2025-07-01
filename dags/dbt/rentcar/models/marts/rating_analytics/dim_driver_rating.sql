{{ 
  config(
    materialized = 'table',
    schema = 'marts_rating'
  ) 
}}

SELECT
  d._id                     AS driver_key,
  d.userId                  AS user_key,
  d.license_no              AS license_number
FROM {{ ref('silver_drivers') }} AS d
