{{
    config(
        materialized='table'
    )
}}
WITH dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)


SELECT 
    fhv.dispatching_base_num,
    fhv.pickup_datetime,
    fhv.dropoff_datetime,
    fhv.pulocationid,
    fhv.dolocationid,
    fhv.sr_flag,
    fhv.affiliated_base_number    
FROM {{ ref('stg_fhv_tripdata') }} fhv 
inner join dim_zones as pickup_zone
on fhv.pulocationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fhv.dolocationid = dropoff_zone.locationid