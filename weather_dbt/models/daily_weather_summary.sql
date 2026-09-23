select
    city,
    cast(measured_at as date) as weather_date,
    count(*) as measurements_count,
    avg(temperature) as avg_temperature,
    min(temperature) as min_temperature,
    max(temperature) as max_temperature,
    avg(windspeed) as avg_windspeed
from {{ ref('stg_weather') }}
group by
    city,
    cast(measured_at as date)
order by
    weather_date DESC
