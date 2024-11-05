import networkx as nx
import pandas as pd
import requests
import json

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
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lon']}&appid={api_key}&exclude=minutely,hourly,alerts"
    response = requests.get(url)
    data = response.json()
    print(data)
    wind_speed = data.get('wind', {}).get('speed')
    clouds = data.get('clouds').get('all')  # Placeholder for solar radiation

    return wind_speed, clouds

def build_dataframe(locations):
    data = []
    for loc in locations:
        wind_speed, clouds = fetch_weather_data(loc)
        if wind_speed is not None and clouds is not None:  # Only add location if wind data is available
            data.append({
                "name": loc["name"],
                "lat": loc["lat"],
                "lon": loc["lon"],
                "wind_speed": wind_speed,
                "clouds": clouds,
            })
    return pd.DataFrame(data)

def create_network(df):
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_node(row['name'], pos=(row['lat'], row['lon']), wind_speed=row['wind_speed'], clouds=row['clouds'])

    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            node_a = df.iloc[i]
            node_b = df.iloc[j]
            distance = ((node_a['lat'] - node_b['lat']) ** 2 + (node_a['lon'] - node_b['lon']) ** 2) ** 0.5
            wind_diff = abs(node_a['wind_speed'] - node_b['wind_speed'])
            
            # Add an edge if nodes are geographically close and have similar wind speeds
            if distance < 1 and wind_diff < 2:
                G.add_edge(node_a['name'], node_b['name'], weight=1 / (distance + wind_diff))
    return G

def analyze_network(G):
    pagerank_scores = nx.pagerank(G)
    communities = nx.algorithms.community.greedy_modularity_communities(G)
    community_dict = {node: i for i, comm in enumerate(communities) for node in comm}
    nx.set_node_attributes(G, pagerank_scores, 'pagerank')
    nx.set_node_attributes(G, community_dict, 'community')
    return G

def calculate_statistics(df):
    top_wind = df.nlargest(5, 'wind_speed')[['name', 'wind_speed']]
    top_solar = df.nlargest(5, 'clouds')[['name', 'clouds']]
    
    average_wind = df['wind_speed'].mean()
    average_solar = df['clouds'].mean()

    return top_wind, top_solar, average_wind, average_solar

def save_statistics_to_json(statistics, filename='../assets/statistics.json'):
    with open(filename, 'w') as f:
        json.dump(statistics, f)

def main():
    # Step 1: Build the DataFrame
    df = build_dataframe(locations)

    # Step 2: Create the network from the DataFrame
    G = create_network(df)

    # Step 3: Analyze the network
    G = analyze_network(G)

    # Step 4: Calculate statistics
    top_wind, top_solar, avg_wind, avg_solar = calculate_statistics(df)

    # Step 5: Save statistics to JSON
    statistics = {
        "top_wind": top_wind.to_dict(orient='records'),
        "top_solar": top_solar.to_dict(orient='records'),
        "average_wind": avg_wind,
        "average_solar": avg_solar,
    }
    save_statistics_to_json(statistics)

if __name__ == "__main__":
    main()
