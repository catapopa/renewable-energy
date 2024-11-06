import pandas as pd
import plotly.graph_objects as go
import networkx as nx
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

def plot_map_with_edges_and_betweenness(yearly_avg, year):
    """Plots the yearly averages on a map for a given year with edges based on betweenness centrality."""
    # Filter data for the specified year
    year_data = yearly_avg[yearly_avg['year'] == year]

    # Define location coordinates
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

    # Create a network graph based on weather similarity
    G = nx.Graph()
    for i, loc1 in enumerate(year_data['location']):
        for j, loc2 in enumerate(year_data['location']):
            if i != j:
                # Calculate edge weight based on some criteria, e.g., difference in shortwave radiation
                weight = abs(year_data.iloc[i]['shortwave_radiation_sum'] - year_data.iloc[j]['shortwave_radiation_sum'])
                G.add_edge(loc1, loc2, weight=weight)

    # Calculate betweenness centrality
    betweenness = nx.betweenness_centrality(G, weight='weight')

    # Draw nodes and edges
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = location_coords[edge[0]]
        x1, y1 = location_coords[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)  # None to break the line
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)  # None to break the line

    # Create scatter plot for locations
    node_x = [location_coords[loc][1] for loc in year_data['location']]
    node_y = [location_coords[loc][0] for loc in year_data['location']]
    
    # Create the plot
    fig = go.Figure()
    
    # Add edges to the figure
    fig.add_trace(go.Scattergeo(
        mode='lines',
        lon=edge_x,
        lat=edge_y,
        line=dict(width=1, color='blue'),
        hoverinfo='none'
    ))
    
    # Add nodes to the figure, with size based on betweenness centrality
    node_sizes = [betweenness[loc] * 1000 for loc in year_data['location']]  # Scale for visibility
    fig.add_trace(go.Scattergeo(
        mode='markers+text',
        lon=node_x,
        lat=node_y,
        text=year_data['location'],
        textposition="bottom center",
        marker=dict(size=node_sizes, color='red'),
        hoverinfo='text'
    ))

    # Update layout
    fig.update_layout(
        title=f"Average Yearly Weather Data for {year} with Betweenness Centrality - UV",
        showlegend=False,
        geo=dict(
            scope='europe',
            showland=True,
            landcolor="lightgray",
            subunitcolor="blue",
            countrycolor="black",
        )
    )
    
    fig.show()

# Fetch weather data
data = fetch_weather_data()

# Calculate yearly averages
yearly_avg = calculate_yearly_averages(data)

# Plot the map for a specific year with edges based on betweenness centrality
plot_map_with_edges_and_betweenness(yearly_avg, year=2024)
