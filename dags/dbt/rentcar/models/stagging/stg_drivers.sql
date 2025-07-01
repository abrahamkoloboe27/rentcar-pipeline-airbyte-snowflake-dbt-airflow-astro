{{ config(
    materialized = 'incremental',
    unique_key    = '_id',
     schema = 'stg'
) }}

WITH raw AS (
  SELECT
    _id,
    userId,
    cityid,
    registrationdate::timestamp_ntz , 
    fullname,
    phonenumber,
    licenseNumber,
    status,
    inactive_since::timestamp_ntz , 
    banned_since::timestamp_ntz , 
    suspended_since::timestamp_ntz , 
    suspended_reason,
    banned_reason
  FROM RIDE_SHARE_V1.drivers
  {% if is_incremental() %}
    WHERE joinedDate >= DATEADD(day, -1, CURRENT_TIMESTAMP())
  {% endif %}
)

SELECT * FROM raw
