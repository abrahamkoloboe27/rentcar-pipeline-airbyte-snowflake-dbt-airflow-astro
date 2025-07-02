{{ config(
    materialized = 'table',
    unique_key    = '_id',
    schema = 'stg'
) }}

WITH raw AS (
  SELECT
    _id,
    --fullname:first  AS first_name,
    fullname,
    email,
    phonenumber,
    cityid,
    registrationdate::timestamp_ntz AS signup_dt,
    countryid
  FROM RIDE_SHARE_V1.users
  -- {% if is_incremental() %}
  --   WHERE signupDate >= DATEADD(day, -1, CURRENT_TIMESTAMP())
  -- {% endif %}
)

SELECT * FROM raw
