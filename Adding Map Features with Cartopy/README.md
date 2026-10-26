<h2 align="center">
		Coastal Emergency Risks Assessment (CERA) <br/>
		<img src="../logo/cera_150x150.png" width="90" height="90">  <br/><a target="_blank" href="https://cera.coastalrisk.live/">cera.coastalrisk.live</a>
</h2>
<br/>

[← Back to the tutorial index](../README.md)

# Geospatial Data Visualization: Introduction to Cartopy

## About this tutorial

This tutorial focuses on the Cartopy library, a powerful tool for geospatial data visualization in Python. It guides you through the fundamentals of creating maps with varying projections, overlaying coordinate points on those maps, and customizing their appearance. It is a stepping stone for those interested in geospatial data visualization, providing a hands-on approach to the Cartopy library.

## Getting Started

Requires the Conda environment in the repository's `environment.yml`.

### Jupyter Notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CERA-GROUP/Tutorials/blob/dev/Adding%20Map%20Features%20with%20Cartopy/Cartopy.ipynb)

### Python standalone

* Direct python script [file](cera_cartopy.py).
* Check the tutorial [instructions](Cartopy.ipynb).
* Example station point data file [water_level_stations.csv](https://cloud.cera.lsu.edu/s/6qamYSWn2FarbLP/download/water_level_stations.csv).

Given the relative path to the repository and the name of the Python script, you can execute it from the terminal as follows:

```bash
cd "Adding Map Features with Cartopy"
wget -O water_level_stations.csv https://cloud.cera.lsu.edu/s/6qamYSWn2FarbLP/download/water_level_stations.csv
python3 cera_cartopy.py water_level_stations.csv
python3 cera_cartopy.py water_level_stations.csv --output station_map.png
python3 cera_cartopy.py water_level_stations.csv --output station_map.png --no-show
python3 cera_cartopy.py water_level_stations.csv --title "Water level stations"
```

The input CSV file must contain these columns:

```text
station_id, lat, lon
```
