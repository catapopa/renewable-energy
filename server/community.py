import pandas as pd
import numpy as np
import networkx as nx
import plotly.express as px
from sklearn.metrics.pairwise import euclidean_distances

from analysis import fetch_weather_data
from map import calculate_yearly_averages

def create_similarity_network(yearly_avg):
    # Filter the DataFrame to only include numeric columns
    numeric_df = yearly_avg.select_dtypes(include=[np.number])
    correlation_matrix = numeric_df.corr()  # Compute correlation matrix
    G = nx.Graph()

    for loc1 in correlation_matrix.index:
        for loc2 in correlation_matrix.columns:
            if loc1 != loc2:
                weight = correlation_matrix.loc[loc1, loc2]
                if weight != 0:  # Only add edges with non-zero weight
                    G.add_edge(loc1, loc2, weight=weight)

    return G


def community_detection(G):
    """Detects communities in the network using Louvain method."""
    import community as community_louvain
    partition = community_louvain.best_partition(G)
    nx.set_node_attributes(G, partition, 'community')
    return partition

def calculate_centrality_measures(G):
    """Calculates centrality measures for the graph."""
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)
    
    # Store centrality as node attributes
    nx.set_node_attributes(G, betweenness, 'betweenness')
    nx.set_node_attributes(G, closeness, 'closeness')

def visualize_network(G):
    """Visualizes the network using Plotly."""
    pos = nx.spring_layout(G)  # Spring layout for plotting

    # Extract data for plotting
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node} - Betweenness: {G.nodes[node]['betweenness']:.2f}, "
                         f"Closeness: {G.nodes[node]['closeness']:.2f}")
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            color=[G.nodes[node]['community'] for node in G.nodes()],  # Color by community
            colorbar=dict(
                thickness=15,
                title='Community',
                xanchor='left',
                titleside='right'
            ),
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Weather Similarity Network',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))
    fig.show()

# Fetch weather data and calculate yearly averages
data = fetch_weather_data()
yearly_avg = calculate_yearly_averages(data)

# Create the similarity network
G = create_similarity_network(yearly_avg)

# Detect communities
community_detection(G)

# Calculate centrality measures
calculate_centrality_measures(G)

# Visualize the network
visualize_network(G)
