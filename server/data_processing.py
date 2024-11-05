import networkx as nx
import pandas as pd
import requests
import json
import geopandas as gpd
from shapely.geometry import Point

locations = [
    {"name": "Bucharest", "lat": 44.4268, "lon": 26.1025},
    {"name": "Cluj-Napoca", "lat": 46.7712, "lon": 23.6236},
    {"name": "Iasi", "lat": 47.1585, "lon": 27.6014},
    {"name": "Constanta", "lat": 44.1598, "lon": 28.6348},
    {"name": "Timisoara", "lat": 45.7489, "lon": 21.2087},
    {"name": "Brasov", "lat": 45.6580, "lon": 25.6012},
    {"name": "Oradea", "lat": 47.0722, "lon": 21.9218},
]

def fetch_weather_data(location):
    api_key = "cff189176f46e0d3f187335d4acd082e"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lon']}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'wind' in data and 'speed' in data['wind']:
        return data['wind']['speed']
    else:
        print(f"Warning: 'wind' data not available for {location['name']}")
        return None  # Return None if data is unavailable

# Build a DataFrame with location and weather data
def build_dataframe(locations):
    data = []
    for loc in locations:
        wind_speed = fetch_weather_data(loc)
        if wind_speed is not None:  # Only add location if wind data is available
            data.append({"name": loc["name"], "lat": loc["lat"], "lon": loc["lon"], "wind_speed": wind_speed})
    return pd.DataFrame(data)



def create_network(df):
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_node(row['name'], pos=(row['lat'], row['lon']), wind_speed=row['wind_speed'])

    # Add edges based on distance and wind speed similarity without checking shortest path
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            node_a = df.iloc[i]
            node_b = df.iloc[j]
            distance = ((node_a['lat'] - node_b['lat']) ** 2 + (node_a['lon'] - node_b['lon']) ** 2) ** 0.5
            wind_diff = abs(node_a['wind_speed'] - node_b['wind_speed'])
            
            # Add an edge if nodes are geographically close and have similar wind speeds
            if distance < 1 and wind_diff < 2:  # Thresholds for edges
                G.add_edge(node_a['name'], node_b['name'], weight=1 / (distance + wind_diff))
    return G


# Perform PageRank and Community Detection
def analyze_network(G):
    pagerank_scores = nx.pagerank(G)
    communities = nx.algorithms.community.greedy_modularity_communities(G)
    community_dict = {node: i for i, comm in enumerate(communities) for node in comm}
    nx.set_node_attributes(G, pagerank_scores, 'pagerank')
    nx.set_node_attributes(G, community_dict, 'community')
    return G

df = build_dataframe(locations)
G = create_network(df)
G = analyze_network(G)

# Convert nodes and attributes to JSON for visualization
node_data = [
    {
        "name": node,
        "lat": G.nodes[node]["pos"][0],
        "lon": G.nodes[node]["pos"][1],
        "pagerank": G.nodes[node]["pagerank"],
        "community": G.nodes[node]["community"]
    } for node in G.nodes
]
with open("network_data.json", "w") as f:
    json.dump(node_data, f)
