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
    driverId,
    brand,
    model,
    licensePlate,
    status,
    year::INT AS year,
    mileageKm,
    acquisitionDate
  FROM {{ ref('stg_vehicles') }}
),

cleaned AS (
  SELECT
    _id,
    driverId,
    UPPER(brand) AS brand_clean,
    UPPER(model) AS model_clean,
    UPPER(licensePlate) AS plate_clean,
    CASE 
      WHEN status IN ('idle','busy','maintenance','retired') 
      THEN status 
      ELSE 'idle' 
    END AS status_clean,
    year,
    mileageKm,
    CASE 
      WHEN acquisitionDate IS NULL THEN NULL 
      ELSE DATEDIFF(year, TO_DATE(year||'-01-01'), CURRENT_DATE()) 
    END AS vehicle_age,
    acquisitionDate
  FROM src
)

SELECT * FROM cleaned
