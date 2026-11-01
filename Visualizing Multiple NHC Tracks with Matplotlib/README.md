<h2 align="center">
		Coastal Emergency Risks Assessment (CERA) <br/>
		<img src="../logo/cera_150x150.png" width="90" height="90">  <br/><a target="_blank" href="https://cera.coastalrisk.live/">cera.coastalrisk.live</a>
</h2>
<br/>

[← Back to the tutorial index](../README.md)

# Visualizing Multiple NHC Tracks with Matplotlib

> **Status:** work in progress. The notebooks are in place; this README is still
> being written.

## About this tutorial

Load a catalog of Atlantic ATCF best-track files, color each track segment by
maximum sustained wind, and export one overview map per region.

## Notebooks

| Notebook | Region |
|---|---|
| [`plot_all_tracks.ipynb`](plot_all_tracks.ipynb) | All Atlantic storms |
| [`plot_all_tracks_ck.ipynb`](plot_all_tracks_ck.ipynb) | Chesapeake |
| [`plot_all_tracks_egom.ipynb`](plot_all_tracks_egom.ipynb) | East Gulf of Mexico |
| [`plot_all_tracks_la.ipynb`](plot_all_tracks_la.ipynb) | Louisiana |
| [`plot_all_tracks_nac.ipynb`](plot_all_tracks_nac.ipynb) | North Atlantic |
| [`plot_all_tracks_ngom.ipynb`](plot_all_tracks_ngom.ipynb) | Northern Gulf |
| [`plot_all_tracks_sab.ipynb`](plot_all_tracks_sab.ipynb) | South Atlantic Bight |
| [`plot_all_tracks_sabnac.ipynb`](plot_all_tracks_sabnac.ipynb) | South Atlantic Bight + North Atlantic |
| [`plot_all_tracks_stofs.ipynb`](plot_all_tracks_stofs.ipynb) | STOFS |
| [`plot_all_tracks_tx.ipynb`](plot_all_tracks_tx.ipynb) | Texas |

## Getting Started

Requires the Conda environment in the repository's `environment.yml`.

```bash
cd "Visualizing Multiple NHC Tracks with Matplotlib"
jupyter lab plot_all_tracks.ipynb
```
