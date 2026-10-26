<h2 align="center">
		Coastal Emergency Risks Assessment (CERA) <br/>
		<img src="../logo/cera_150x150.png" width="90" height="90">  <br/><a target="_blank" href="https://cera.coastalrisk.live/">cera.coastalrisk.live</a>
</h2>
<br/>

[← Back to the tutorial index](../README.md)

# A Beginner's Guide to Analyzing ADCIRC NetCDF Data with Python

## About this tutorial

Scientific geospatial datasets like climatological or oceanographic model results can sometimes grow in complexity and data volume very quickly. It can become challenging to work with the huge amount of outputs if the data is simulated over large geographic regions or is generated multiple times per day. The NetCDF format provides a solution for efficient data management by storing the datasets in a well-organized manner that allows a successful data analysis in a user-friendly way. This tutorial explains the structure of a NetCDF file using the Python library NetCDF4.

## Getting Started

Requires the Conda environment in the repository's `environment.yml`.

### Jupyter Notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CERA-GROUP/Tutorials/blob/dev/Analyzing%20NetCDF%20Files/NetCDF_Tutorial/netCDF4.ipynb)

### Python standalone

* Direct python script [file](NetCDF_Tutorial/net_CDF4.py).
* Check the tutorial [instructions](NetCDF_Tutorial/netCDF4.ipynb).
* Example ADCIRC NetCDF file [input file](https://cloud.cera.lsu.edu/s/7PfqfzWDj285Afw/download/maxele.63.nc).

## Running the tutorial

From the repository root:

```bash
cd "Analyzing NetCDF Files/NetCDF_Tutorial"
wget -O maxele.63.nc https://cloud.cera.lsu.edu/s/7PfqfzWDj285Afw/download/maxele.63.nc
jupyter lab netCDF4.ipynb
python3 net_CDF4.py
```
