{{ 
  config(
    materialized='table', 
    unique_key='_id',
    schema = 'silver'
  ) 
}}

WITH src AS (
  SELECT
    _id,
    -- fullname:first  AS first_name,
    fullname,
    email,
    phonenumber,
    cityid,
    signup_dt,
    countryid
  FROM {{ ref('stg_users') }}
  -- {% if is_incremental() %}
  --   WHERE signup_dt >= DATEADD(day, -1, CURRENT_TIMESTAMP())
  -- {% endif %}
),

cleaned_users AS (
  SELECT
    _id,
    -- Nom complet
    --CONCAT(first_name, ' ', last_name)    AS full_name,
    LOWER(TRIM(email))                   AS email,
    REGEXP_REPLACE(phonenumber, '\\D+', '')  AS phonenumber ,  
    signup_dt,
    countryId, 
    cityid,
    fullname
    -- CASE WHEN status IN ('active','blocked') THEN status ELSE 'unknown' END AS status
  FROM src
)

SELECT
  _id,
  fullname,
  email,
  phonenumber,
  cityid,
  signup_dt,
  countryid
FROM cleaned_users
