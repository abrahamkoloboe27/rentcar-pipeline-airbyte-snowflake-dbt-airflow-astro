{{ 
  config(
    materialized='incremental', 
    unique_key='_id',
    schema = 'silver'
  ) 
}}

WITH src AS (
  SELECT
    _id,
    first_name,
    last_name,
    email,
    phone,
    signup_dt,
    countryId,
    status
  FROM {{ ref('stg_users') }}
  {% if is_incremental() %}
    WHERE signup_dt >= DATEADD(day, -1, CURRENT_TIMESTAMP())
  {% endif %}
),

cleaned AS (
  SELECT
    _id,
    -- Nom complet
    CONCAT(first_name, ' ', last_name)    AS full_name,
    LOWER(TRIM(email))                   AS email_clean,
    REGEXP_REPLACE(phone, '\\D+', '')    AS phone_clean,
    signup_dt,
    countryId,
    CASE WHEN status IN ('active','blocked') THEN status ELSE 'unknown' END AS status
  FROM src
)

SELECT * FROM cleaned
