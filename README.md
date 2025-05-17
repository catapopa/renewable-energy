# Romania Renewable Sites Network Analysis

This project analyzes and visualizes optimal renewable energy sites in Romania using network science and weather data. It features a web-based dashboard, network analysis, and interactive maps.

## Features

- **Weather Data Collection:** Fetches historical weather data (wind speed, sunshine duration, solar radiation) for major Romanian cities.
- **Network Analysis:** Builds a network of locations, computes PageRank and community detection to identify key sites.
- **Visualization:** Interactive maps and network graphs using Plotly and Mapbox.
- **Web Dashboard:** Flask-based web app with insights, statistics, and visualizations.

## Project Structure

```
assets/
  network_data.json        # Network nodes with PageRank and community info
  statistics.json          # Top wind/solar locations and averages
client/
  index.html               # Main dashboard page
  script.js                # Frontend logic for fetching and displaying data
  styles.css               # Dashboard styling
  weather.html             # Weather data/statistics page
server/
  app.py                   # Flask web server
  analysis.py              # Weather data fetching and plotting
  community.py             # Community detection and network visualization
  data_processing.py       # Data processing, network building, statistics
  map.py                   # Map visualization (main)
  map_bw_uv.py             # Map with betweenness centrality (UV)
  map_bwc_w.py             # Map with betweenness centrality (wind)
  test.py                  # NetworkX/Matplotlib test script
```

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/romania-renewable-sites.git
cd romania-renewable-sites
```

### 2. Install Python Dependencies

Recommended to use a virtual environment.

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Required packages:**
- flask
- pandas
- networkx
- plotly
- openmeteo-requests
- requests-cache
- retry-requests
- community (python-louvain)
- matplotlib

You can create a `requirements.txt` with:

```
flask
pandas
networkx
plotly
openmeteo-requests
requests-cache
retry-requests
community
matplotlib
```

### 3. Fetch and Process Data

Run the data processing scripts to generate statistics and network data:

```sh
cd server
python data_processing.py
```

This will create/update `assets/statistics.json` and `assets/network_data.json`.

### 4. Run the Web Server

```sh
python app.py
```

The dashboard will be available at [http://localhost:5000](http://localhost:5000).

## Usage

- **Main Dashboard:** Shows the network map, top wind/solar locations, and averages.
- **Weather Data:** Visit `/weather` for detailed weather statistics.
- **Network Analysis:** Explore community structure and centrality using the scripts in `server/`.

## Customization

- To add more locations, update the `locations` list in [`server/data_processing.py`](server/data_processing.py) and [`server/analysis.py`](server/analysis.py).
- To change the analysis or visualizations, modify the relevant scripts in `server/`.

## License

MIT License

---

**Authors:**  
Your Name  
University Project for Complex Networks
