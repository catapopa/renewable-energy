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
    {"name": "Sibiu", "lat": 45.7988, "lon": 24.1548},
    {"name": "Pitesti", "lat": 44.8577, "lon": 24.8711},
    {"name": "Bacau", "lat": 46.5820, "lon": 26.9113},
    {"name": "Targu Mures", "lat": 46.5455, "lon": 24.5579},
    {"name": "Baia Mare", "lat": 47.6576, "lon": 23.5832},
    {"name": "Deva", "lat": 45.8730, "lon": 22.9115},
    {"name": "Focsani", "lat": 45.6980, "lon": 27.1837},
    {"name": "Resita", "lat": 45.3075, "lon": 21.8924},
]

def fetch_weather_data(location):
    api_key = "YOUR_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lon']}&appid={api_key}&exclude=minutely,hourly,alerts"
    response = requests.get(url)
    data = response.json()
    wind_speed = data.get('wind', {}).get('speed')
    clouds = data.get('clouds').get('all')

    return wind_speed, clouds

def build_dataframe(locations):
    data = []
    for loc in locations:
        wind_speed, clouds = fetch_weather_data(loc)
        if wind_speed is not None and clouds is not None:
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
            
            if distance < 10 and wind_diff < 5:  # Consider more nodes based on distance and wind difference
                G.add_edge(node_a['name'], node_b['name'], weight=1 / (distance + 1))  # Adding 1 to avoid division by zero
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
    df = build_dataframe(locations)
    G = create_network(df)
    G = analyze_network(G)
    top_wind, top_solar, avg_wind, avg_solar = calculate_statistics(df)

    statistics = {
        "top_wind": top_wind.to_dict(orient='records'),
        "top_solar": top_solar.to_dict(orient='records'),
        "average_wind": avg_wind,
        "average_solar": avg_solar,
    }
    save_statistics_to_json(statistics)

if __name__ == "__main__":
    main()
