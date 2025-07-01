{{ 
  config(
    materialized = 'table',
    schema = 'marts_rating'
  ) 
}}

SELECT
  u._id                    AS user_key,
  u.full_name              AS user_name,
  u.email_clean            AS email,
  u.phone_clean            AS phone,
  u.signup_dt              AS signup_date,
  u.countryId              AS country_key,
  u.status                 AS user_status
FROM {{ ref('silver_users') }} AS u
