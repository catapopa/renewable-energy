import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# List of locations with their latitude and longitude
locations = [
    {"name": "Bucharest", "lat": 44.4268, "lon": 26.1025},
    {"name": "Cluj-Napoca", "lat": 46.7712, "lon": 23.6236},
    {"name": "Iasi", "lat": 47.1585, "lon": 27.6014},
    {"name": "Constanta", "lat": 44.1598, "lon": 28.6348},
    {"name": "Timisoara", "lat": 45.7489, "lon": 21.2087},
    {"name": "Brasov", "lat": 45.6580, "lon": 25.6012},
    {"name": "Oradea", "lat": 47.0722, "lon": 21.9218}
]

def fetch_weather_data():
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    all_daily_data = []

    for location in locations:
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": location["lat"],
            "longitude": location["lon"],
            "start_date": "2014-11-01",
            "end_date": "2024-11-02",
            "daily": ["sunshine_duration", "wind_speed_10m_max", "shortwave_radiation_sum"],
            "timezone": "auto"
        }
        
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        daily = response.Daily()

        daily_data = {
            "location": location["name"],
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
        all_daily_data.append(daily_dataframe)

    combined_daily_data = pd.concat(all_daily_data, ignore_index=True)
    return combined_daily_data

def plot_weather_data(data):
    fig = make_subplots(
        rows=2, cols=1, vertical_spacing=0.1,
        subplot_titles=("Shortwave Radiation (kWh/m²)", "Maximum Wind Speed (m/s)")
    )

    color_palette = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3", "#FF6692"]
    
    for i, location in enumerate(data['location'].unique()):
        location_data = data[data['location'] == location]
        
        fig.add_trace(
            go.Scatter(
                x=location_data['date'], y=location_data['shortwave_radiation_sum'],
                mode='lines', name=f'{location} Shortwave Radiation',
                line=dict(color=color_palette[i % len(color_palette)], width=2)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=location_data['date'], y=location_data['wind_speed_10m_max'],
                mode='lines', name=f'{location} Max Wind Speed', line=dict(color=color_palette[i % len(color_palette)], width=2)
            ),
            row=2, col=1
        )

    fig.update_xaxes(
        title_text="Date", tickformat="%Y-%m", ticks="outside", showgrid=True, tickangle=45, row=2, col=1
    )

    fig.update_layout(
        title="Weather Data Visualization",
        template="plotly_white",
        legend=dict(
            title="Locations",
            orientation="h",
            yanchor="top", y=1.1, xanchor="center", x=0.5
        ),
        hovermode="x unified"
    )

    fig.update_yaxes(title_text="Radiation (kWh/m²)", row=1, col=1)
    fig.update_yaxes(title_text="Wind Speed (m/s)", row=2, col=1)

    fig.show()

# Fetch the weather data
weather_data = fetch_weather_data()

# Plot the weather data
plot_weather_data(weather_data)
