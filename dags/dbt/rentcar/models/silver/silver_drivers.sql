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
    userId,
    licenseNumber,
    phonenumber,
    -- license_expiry_dt,
    status,
    cityid, 
    joined_dt
  FROM {{ ref('stg_drivers') }}
  -- {% if is_incremental() %}
  --   WHERE joined_dt >= DATEADD(day, -1, CURRENT_TIMESTAMP())
  -- {% endif %}
),

cleaned AS (
  SELECT
    _id,
    userId AS user_id,
    UPPER(TRIM(licenseNumber))      AS license_no,
    -- license_expiry_dt,
    -- DATEDIFF(day, CURRENT_DATE(), license_expiry_dt) AS days_to_expiry,
    CASE WHEN status IN ('available','on_trip','offline') THEN status ELSE 'offline' END AS status,
    joined_dt
  FROM src
)

SELECT * FROM cleaned
