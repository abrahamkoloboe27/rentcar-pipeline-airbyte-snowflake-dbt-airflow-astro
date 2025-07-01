{{ config(
    materialized='incremental',
    unique_key='_id',
    schema = 'stg'
) }}

with raw as (
  select * from RIDE_SHARE_V1.cities
)

select
  _id            as city_id,
  countryid      as country_id,
  name          as city_name,
  latitude,
  longitude
from raw
;
