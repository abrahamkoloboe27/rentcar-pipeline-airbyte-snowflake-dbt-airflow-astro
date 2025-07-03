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
    tripId,
    givenbyid AS raterId,
    toid AS rateeId,
    stars,
    givenby,
    comment,
    created_dt
  FROM {{ ref('stg_ratings') }}
  -- {% if is_incremental() %}
  --   WHERE created_dt >= DATEADD(day, -1, CURRENT_TIMESTAMP())
  -- {% endif %}
),

cleaned_ratings AS (
  SELECT
    _id,
    tripId,
    raterId,
    rateeId,
    stars,
    comment,
    created_dt,
    givenby,
    DATE_TRUNC('day', created_dt) AS rating_date
  FROM src
)

SELECT * FROM cleaned_ratings
