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
    driverId,
    type,
    make,
    model,
    licensePlate,
    capacity,
    status,
    specs:year::INT  AS year,
    mileageKm,
    retired_dt
  FROM {{ ref('stg_vehicles') }}
  {% if is_incremental() %}
    WHERE COALESCE(retired_dt, CURRENT_TIMESTAMP()) >= DATEADD(day, -1, CURRENT_TIMESTAMP())
  {% endif %}
),

cleaned AS (
  SELECT
    _id,
    driverId,
    INITCAP(type)                             AS vehicle_type,
    UPPER(make)                               AS make_clean,
    UPPER(model)                              AS model_clean,
    UPPER(licensePlate)                       AS plate_clean,
    capacity,
    CASE WHEN status IN ('idle','busy','maintenance','retired') THEN status ELSE 'idle' END AS status,
    year,
    mileageKm,
    CASE 
      WHEN retired_dt IS NULL THEN NULL 
      ELSE DATEDIFF(year, TO_DATE(year||'-01-01'), CURRENT_DATE()) 
    END AS vehicle_age,
    retired_dt
  FROM src
)

SELECT * FROM cleaned
