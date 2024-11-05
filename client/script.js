async function loadData() {
  const response = await fetch("/data");
  const data = await response.json();

  const traces = [
    {
      type: "scattergeo",
      mode: "markers+text",
      text: data.map(
        (d) => `${d.name}: PR ${d.pagerank.toFixed(3)} | Comm ${d.community}`
      ),
      lon: data.map((d) => d.lon),
      lat: data.map((d) => d.lat),
      marker: {
        size: data.map((d) => d.pagerank * 100), // Scale size by PageRank
        color: data.map((d) => d.community),
        colorscale: "Viridis",
        line: { color: "black", width: 0.5 },
      },
    },
  ];

  const layout = {
    title: "Optimal Renewable Sites",
    geo: {
      scope: "europe",
      projection: { type: "mercator" },
      showland: true,
      landcolor: "rgb(217, 217, 217)",
      countrywidth: 1,
      countrycolor: "rgb(255, 255, 255)",
    },
  };

  Plotly.newPlot("map", traces, layout);
}
loadData();
