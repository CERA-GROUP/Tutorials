<h2 align="center">
		Coastal Emergency Risks Assessment (CERA) <br/>
		<img src="../logo/cera_150x150.png" width="90" height="90">  <br/><a target="_blank" href="https://cera.coastalrisk.live/">cera.coastalrisk.live</a>
</h2>
<br/>

[← Back to the tutorial index](../README.md)

# Visualizing a Single NHC Track with Matplotlib

> **Status:** work in progress. The notebooks are in place; this README is still
> being written.

## About this tutorial

Render one ATCF best-track file into a publication-style map, optionally
overlaying validation stations.

## Notebooks

| Notebook | Purpose |
|---|---|
| [`plot_tracks_modified.ipynb`](plot_tracks_modified.ipynb) | Render one ATCF best-track `.dat` file into a map. |
| [`plot_tracks.orig.ipynb`](plot_tracks.orig.ipynb) | Original version of the notebook above. |
| [`plot_stations_tracks.ipynb`](plot_stations_tracks.ipynb) | One storm's best track with validation stations overlaid. |
| [`plot_stations_tracks_modified.ipynb`](plot_stations_tracks_modified.ipynb) | Revised version of the stations notebook. |

## Getting Started

Requires the Conda environment in the repository's `environment.yml`.

```bash
cd "Visualizing a Single NHC Track with Matplotlib"
jupyter lab plot_tracks_modified.ipynb
```
