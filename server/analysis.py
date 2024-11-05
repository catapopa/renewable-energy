import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry

def fetch_weather_data():
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": [46.7667, 44.428, 47.1667, 47.0458, 45.6486, 44.1807, 45.7537],
        "longitude": [23.6, 26.0967, 27.6, 21.9183, 25.6061, 28.6343, 21.2257],
        "start_date": "2023-11-01",  
        "end_date": "2024-11-02",    
        "hourly": ["cloud_cover_high", "wind_speed_100m"],
        "daily": ["sunshine_duration", "wind_speed_10m_max", "shortwave_radiation_sum"],
        "timezone": "auto"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Extract hourly and daily data
    response = responses[0]

    # Process daily data
    daily = response.Daily()
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ),
        "sunshine_duration": daily.Variables(0).ValuesAsNumpy(),
        "wind_speed_10m_max": daily.Variables(1).ValuesAsNumpy(),
        "shortwave_radiation_sum": daily.Variables(2).ValuesAsNumpy()
    }
    daily_dataframe = pd.DataFrame(data=daily_data)

    return daily_dataframe
