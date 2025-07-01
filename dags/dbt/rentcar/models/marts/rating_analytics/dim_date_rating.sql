{{ 
  config(
    materialized = 'table',
    schema = 'marts_rating'
  ) 
}}

WITH dates AS (
  SELECT DISTINCT rating_date AS date
  FROM {{ ref('silver_ratings') }}
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
