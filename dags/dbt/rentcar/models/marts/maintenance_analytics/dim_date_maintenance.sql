{{ 
  config(
    materialized = 'table',
    schema = 'marts_maintenance'
  ) 
}}

WITH dates AS (
  SELECT DISTINCT maintenance_date AS date
  FROM {{ ref('silver_maintenance') }}
)

SELECT
  date                                         AS date_key,
  YEAR(date)                                   AS year,
  QUARTER(date)                                AS quarter,
  MONTH(date)                                  AS month,
  DAY(date)                                    AS day,
  DAYOFWEEK(date)                              AS day_of_week,
  IFF(DAYOFWEEK(date) IN (1,7), TRUE, FALSE)   AS is_weekend,
  TO_VARCHAR(date, 'YYYY-MM-DD')               AS date_iso
FROM dates
ORDER BY date
