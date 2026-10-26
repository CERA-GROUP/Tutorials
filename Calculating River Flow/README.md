<h2 align="center">
		Coastal Emergency Risks Assessment (CERA) <br/>
		<img src="../logo/cera_150x150.png" width="90" height="90">  <br/><a target="_blank" href="https://cera.coastalrisk.live/">cera.coastalrisk.live</a>
</h2>
<br/>

[← Back to the tutorial index](../README.md)

# Stage-Discharge Curve Fitting for River Flow

> **Status:** work in progress. The notebook is in place; this README is still
> being written.

## About this tutorial

Extracts the flow-stage relationship for the Baton Rouge station from Figure 3
of a published rating curve and fits a stage-discharge curve.

## Notebooks

| Notebook | Purpose |
|---|---|
| [`river_flow_calculation.ipynb`](river_flow_calculation.ipynb) | Digitize the rating curve and fit the stage-discharge relationship. |

## Data

| File | Purpose |
|---|---|
| [`stage_input.png`](stage_input.png) | Source figure used to digitize the curve. |

## Getting Started

Requires the Conda environment in the repository's `environment.yml`.

```bash
cd "Calculating River Flow"
jupyter lab river_flow_calculation.ipynb
```
