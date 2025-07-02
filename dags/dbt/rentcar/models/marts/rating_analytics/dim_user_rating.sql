{{ 
  config(
    materialized = 'table',
    schema = 'marts_rating'
  ) 
}}

SELECT
  u._id                    AS user_key,
  u.fullname              AS user_name,
  u.email                  AS email,
  u.phonenumber           AS phone,
  u.signup_dt              AS signup_date,
  u.countryid             AS country_key,
  u.cityid                AS city_key
FROM {{ ref('silver_users') }} AS u
