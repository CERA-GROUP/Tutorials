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

Requires Python 3.15.2 and the shared packages in `requirements.txt`:

```bash
python3 -m pip install -r requirements.txt
```

### Jupyter Notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CERA-GROUP/Tutorials/blob/main/Analyzing%20NetCDF%20Files/cera_netcdf.ipynb)

### Python standalone

* Direct python script [file](cera_netcdf.py).
* Check the tutorial [instructions](cera_netcdf.ipynb).

### Input data

* Place `maxele.63.nc` next to the notebook.

Run the tutorial from this folder:

```bash
cd "Analyzing NetCDF Files"
python3 cera_netcdf.py
python3 cera_netcdf.py --output output_netcdf.txt
jupyter lab cera_netcdf.ipynb
```

### Command line options

    cera_netcdf.py [-i INFILE] [-o OUTPUT]

optional:

      -i | infile       NetCDF input file (default: maxele.63.nc)
      -o | output       text report output file (default: output_netcdf.txt)

## Example output

The script writes a text report to `output_netcdf.txt` containing the dataset structure, variable metadata, dimensions, shapes, sample values, and the `zeta_max` range.
