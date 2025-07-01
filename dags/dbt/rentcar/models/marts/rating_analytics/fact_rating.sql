{{ 
  config(
    materialized = 'table',
    schema = 'marts_rating'
  ) 
}}

SELECT
  r._id                     AS rating_key,
  DATE_TRUNC('day', r.created_dt) AS date_key,
  r.tripId                  AS trip_key,
  r.raterId                 AS rater_key,
  r.rateeId                 AS ratee_key,
  r.stars                   AS rating_stars,
  r.comment                 AS rating_comment
FROM {{ ref('silver_ratings') }} AS r
