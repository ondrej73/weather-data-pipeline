select
    id,
    city,
    measured_at,
    temperature,
    windspeed,
    is_day
from {{ source('weather', 'weather_raw') }}