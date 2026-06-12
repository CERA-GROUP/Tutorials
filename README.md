<h2 align="center">
		Coastal Emergency Risks Assessment (CERA) <br/>
		<img src="https://github.com/CERA-GROUP/Tutorials/blob/main/logo/cera_150x150.png" width="100" height="100">  <br/><a target="_blank" href="https://cera.coastalrisk.live/">cera.coastalrisk.live</a> 
</h2>
<br/>

# Welcome to the CERA Storm Analysis Tutorials

#### Overview
This repository is maintained by the LSU CERA-Group, a team of scientists, researchers, and developers dedicated to studying the potential impacts of storm surge and inland flooding caused by landfalling tropical cyclones. We focus on providing accurate and timely information to decision-makers and first responders to support their preparedness efforts and ultimately save lives and properties.

#### Objective
Our objective is to simulate and visualize storm surge using advanced computer models like ADCIRC and the cutting-edge CERA visualization technology. By this tutorial series we are trying to open our knowledge to the research community for the post-proscesing and visualization of storm surge data. 

<br/>

---

## Environment setup
The tutorials use Python, Jupyter, NumPy, pandas, Matplotlib, netCDF4, Cartopy, Pillow, and ipywidgets.

The recommended setup uses Conda/Mamba with packages from conda-forge:

```bash
conda env create -f environment.yml
conda activate cera-tutorials
python -m ipykernel install --user --name cera-tutorials --display-name "Python (cera-tutorials)"
```

Alternatively, with pip:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Cartopy and netCDF4 depend on compiled libraries, so Conda/Mamba is recommended if pip installation fails.

---

## Tutorials
### [A Beginner's Guide to Analyzing ADCIRC NetCDF Data with Python](Analyzing_NetCDF)
The NetCDF format stores large datasets in a well-organized manner that allows a successful data analysis in a user-friendly way. This tutorial explains the structure of a NetCDF file using the Python library NetCDF4.

```bash
cd Analyzing_NetCDF/NetCDF_Tutorial
wget -O maxele.63.nc https://cloud.cera.lsu.edu/s/7PfqfzWDj285Afw/download/maxele.63.nc
jupyter lab netCDF4.ipynb
python3 net_CDF4.py
```

### [Matplotlib Contouring for ADCIRC NetCDF Data](Map_Contouring_Matplotlib)
The Coastal Emergency Risks Assessment (CERA) tutorial leverages Matplotlib to visualize NetCDF data, offering insights into coastal phenomena for the Northern Gulf and the Atlantic Coast regions. 

### [Geospatial Data Visualization: Introduction to Cartopy](Cartopy)

The CERA Storm Analysis Tutorials, maintained by the LSU CERA-Group, provide guides for simulating and visualizing storm surge using advanced computer models and technologies, with tutorials on analyzing ADCIRC NetCDF data with Python, Matplotlib contouring, and geospatial data visualization using Cartopy.

```bash
cd Cartopy
wget -O water_level_stations.csv https://cloud.cera.lsu.edu/s/6qamYSWn2FarbLP/download/water_level_stations.csv
jupyter lab Cartopy.ipynb
python3 cera_cartopy.py water_level_stations.csv --output station_map.png --no-show
```

---
#### Contact Us
If you have any questions, suggestions, or would like to get in touch with our team, please feel free to reach out to us. Together, we can make a significant impact in enhancing our preparedness and resilience to storm-related challenges.
<p align="center">
</a>
<a href="https://github.com/CERA-GROUP">
	<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>
<a href="https://www.linkedin.com/company/coastal-emergency-risks-assessment/">
	<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
<a href="mailto:info@coastalrisk.live">
    <img src="https://img.shields.io/badge/Email-info@coastalrisk.live-green?style=for-the-badge" alt="Email">
</a>
</p>
<br/>

---

<p align="center">
  CENTER FOR COMPUTATION AND TECHNOLOGY, LOUISIANA STATE UNIVERSITY
</p>
