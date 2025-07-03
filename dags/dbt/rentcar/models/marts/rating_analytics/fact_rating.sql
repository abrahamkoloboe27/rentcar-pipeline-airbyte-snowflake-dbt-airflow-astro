{{ 
  config(
    materialized = 'table',
    schema = 'marts_rating'
  ) 
}}

SELECT
  r._id                     AS rating_key,
  DATE_TRUNC('day', r.rating_date) AS date_key,
  r.tripId                  AS trip_key,
  r.raterId                 AS rater_key,
  r.rateeId                 AS ratee_key,
  r.stars                   AS rating_stars,
  r.comment                 AS rating_comment,
  r.created_dt              AS created_at,
  r.rating_date             AS rated_at,
  r.givenby                 AS rated_by
FROM {{ ref('silver_ratings') }} AS r
