select
    dispatching_base_num,
    pickup_datetime,
    dropoff_datetime,
    pulocationid,
    dolocationid,
    sr_flag,
    affiliated_base_number
from {{ source('staging', 'fav_2019') }}
where extract(year from date(pickup_datetime)) = 2019
