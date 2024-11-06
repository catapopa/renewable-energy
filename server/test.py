import matplotlib.pyplot as plt
import networkx as nx
from data_processing import create_network, build_dataframe, analyze_network

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

def plot_network(G):
    pos = nx.spring_layout(G)

    # Get PageRank scores
    pagerank_scores = nx.pagerank(G)
    
    # Get communities
    communities = nx.algorithms.community.greedy_modularity_communities(G)
    community_dict = {node: i for i, comm in enumerate(communities) for node in comm}
    nx.set_node_attributes(G, pagerank_scores, 'pagerank')
    nx.set_node_attributes(G, community_dict, 'community')
    # Map colors based on community
    color_map = [community_dict[node] for node in G.nodes()]

    node_sizes = [5000 * pagerank_scores[node] for node in G.nodes()]  # Scale size for better visibility
    labels = {node: f"{node}\n\nPageRank: {pagerank_scores[node]:.4f}" for node in G.nodes()}

    nx.draw(G, pos, with_labels=False, node_color=color_map, node_size=node_sizes, font_size=8, cmap=plt.cm.Set3, font_color='black')
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

    plt.title("Network Graph of Renewable Sites with PageRank and Communities")
    plt.show()

df = build_dataframe(locations)
G = create_network(df)

plot_network(G)
