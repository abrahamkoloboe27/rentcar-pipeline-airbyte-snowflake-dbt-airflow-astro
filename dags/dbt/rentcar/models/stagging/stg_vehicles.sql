{{ config(
    materialized = 'table',
    unique_key    = '_id',
    schema = 'stg'
) }}

WITH raw AS (
  SELECT
    _id,
    driverId,
    brand,
    model,
    licenseplate,
    mileagekm,
    status,
    year, 
    acquisitiondate::timestamp_ntz AS acquisitiondate
  FROM RIDE_SHARE_V1.vehicles
  -- {% if is_incremental() %}
  --   WHERE retiredAt >= DATEADD(day, -1, CURRENT_TIMESTAMP())
  --      OR updatedAt  >= DATEADD(day, -1, CURRENT_TIMESTAMP())
  --      -- si tu as un champ updatedAt sinon retire cette ligne
  -- {% endif %}
)

SELECT * FROM raw
