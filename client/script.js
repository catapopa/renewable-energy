// document.addEventListener("DOMContentLoaded", async function () {
//   const response = await fetch("../assets/statistics.json");
//   const stats = await response.json();

//   const topWindList = document.getElementById("top-wind");
//   stats.top_wind.forEach((location) => {
//     const li = document.createElement("li");
//     li.textContent = `${location.name}: ${location.wind_speed} m/s`;
//     topWindList.appendChild(li);
//   });

//   const topSolarList = document.getElementById("top-solar");
//   stats.top_solar.forEach((location) => {
//     const li = document.createElement("li");
//     li.textContent = `${location.name}: ${location.clouds} W/m²`;
//     topSolarList.appendChild(li);
//   });

//   document.getElementById("average-wind").textContent =
//     stats.average_wind.toFixed(2) + " m/s";
//   document.getElementById("average-solar").textContent =
//     stats.average_solar.toFixed(2) + " W/m²";
// });

document.addEventListener("DOMContentLoaded", async function () {
  try {
    const response = await fetch("/stat"); // Fetch from the /stat route instead of directly from the JSON file
    if (!response.ok) {
      throw new Error("Network response was not ok: " + response.statusText);
    }
    const stats = await response.json();

    const topWindList = document.getElementById("top-wind");
    stats.top_wind.forEach((location) => {
      const li = document.createElement("li");
      li.textContent = `${location.name}: ${location.wind_speed} m/s`;
      topWindList.appendChild(li);
    });

    const topSolarList = document.getElementById("top-solar");
    stats.top_solar.forEach((location) => {
      const li = document.createElement("li");
      li.textContent = `${location.name}: ${location.clouds} W/m²`;
      topSolarList.appendChild(li);
    });

    document.getElementById("average-wind").textContent =
      stats.average_wind.toFixed(2) + " m/s";
    document.getElementById("average-solar").textContent =
      stats.average_solar.toFixed(2) + " W/m²";
  } catch (error) {
    console.error("Error fetching statistics:", error);
  }
});

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

// insights.js

// Fetch statistics data
fetch("../assets/statistics.json")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    return response.json();
  })
  .then((statistics) => {
    // Process statistics data
    const topWindList = document.getElementById("top-wind");
    statistics.top_wind.forEach((location) => {
      const li = document.createElement("li");
      li.textContent = `${location.name}: ${location.wind_speed} m/s`;
      topWindList.appendChild(li);
    });

    const topCloudList = document.getElementById("top-solar");
    statistics.top_solar.forEach((location) => {
      const li = document.createElement("li");
      li.textContent = `${location.name}: ${location.clouds} W/m²`;
      topCloudList.appendChild(li);
    });

    document.getElementById("average-wind").textContent =
      statistics.average_wind.toFixed(2) + " m/s";
    document.getElementById("average-solar").textContent =
      statistics.average_solar.toFixed(2) + " W/m²";
  })
  .catch((error) => {
    console.error("Error fetching statistics:", error);
  });
