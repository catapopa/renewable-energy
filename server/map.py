import pandas as pd
import plotly.express as px
from analysis import fetch_weather_data

def calculate_yearly_averages(data):
    """Calculates yearly averages for each location and each weather variable."""
    # Extract year from the date and calculate the mean per year and location
    data['year'] = data['date'].dt.year
    yearly_avg = data.groupby(['location', 'year']).agg({
        'wind_speed_10m_max': 'mean',
        'sunshine_duration': 'mean',
        'shortwave_radiation_sum': 'mean'
    }).reset_index()
    
    # Round the values for cleaner display
    yearly_avg['wind_speed_10m_max'] = yearly_avg['wind_speed_10m_max'].round(2)
    yearly_avg['sunshine_duration'] = yearly_avg['sunshine_duration'].round(2)
    yearly_avg['shortwave_radiation_sum'] = yearly_avg['shortwave_radiation_sum'].round(2)
    
    return yearly_avg

def plot_map(yearly_avg, year):
    """Plots the yearly averages on a map for a given year."""
    # Filter data for the specified year
    year_data = yearly_avg[yearly_avg['year'] == year]

    # Add latitude and longitude to the data
    location_coords = {
        "Bucharest": (44.4268, 26.1025),
        "Cluj-Napoca": (46.7712, 23.6236),
        "Iasi": (47.1585, 27.6014),
        "Constanta": (44.1598, 28.6348),
        "Timisoara": (45.7489, 21.2087),
        "Brasov": (45.6580, 25.6012),
        "Oradea": (47.0722, 21.9218)
    }
    
    year_data['latitude'] = year_data['location'].apply(lambda x: location_coords[x][0])
    year_data['longitude'] = year_data['location'].apply(lambda x: location_coords[x][1])

    # Create a scatter mapbox plot
    fig = px.scatter_mapbox(
        year_data,
        lat="latitude",
        lon="longitude",
        size="shortwave_radiation_sum",
        color="wind_speed_10m_max",
        hover_name="location",
        hover_data={
            "shortwave_radiation_sum": True,  # Solar Radiation (kWh/m²)
            "wind_speed_10m_max": True,  # Max Wind Speed (m/s)
            "sunshine_duration": True,  # Sunshine Duration (hours)
            "year": False,              
            "latitude": False,          
            "longitude": False     
        },
        color_continuous_scale="Viridis",
        size_max=15,
        zoom=5,
        title=f"Yearly Weather Averages for {year}"
    )

    # Update labels for readability
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br><br>" +
                      "Solar Radiation: %{customdata[0]} kWh/m²<br>" +
                      "Max Wind Speed: %{customdata[1]} m/s<br>" +
                      "Sunshine Duration: %{customdata[2]} hours"
    )

    # Customize map layout
    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":50,"l":0,"b":0},
        title={
            'text': f"Average Yearly Weather Data for {year}",
            'x':0.5,
            'xanchor': 'center'
        }
    )
    
    fig.show()

# Fetch weather data
data = fetch_weather_data()

# Calculate yearly averages
yearly_avg = calculate_yearly_averages(data)

# Plot the map for a specific year
plot_map(yearly_avg, year=2024)