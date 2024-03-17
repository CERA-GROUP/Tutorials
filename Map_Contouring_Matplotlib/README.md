<h2 align="center">
		Coastal Emergency Risks Assessment (CERA) <br/>
		<img src="https://github.com/CERA-GROUP/Tutorials/blob/main/logo/cera_150x150.png" width="90" height="90">  <br/><a target="_blank" href="https://cera.coastalrisk.live/">cera.coastalrisk.live</a> 
</h2>
<br/>

# CERA Storm Analysis Tutorials Repository - Unveiling the Storm
## CERA Matplotlib Contouring for NetCDF Data

## About this tutorial

This tutorial presents a Python script utilizing the Matplotlib library to generate contour plots from ADCIRC NetCDF data, focusing on storm surge and wave guidance for the Northern Gulf and the Atlantic Coast. Developed as part of the Coastal Emergency Risks Assessment (CERA) software package, this script serves as a crucial component for real-time visualization of storm surge guidance.

Utilizing Matplotlib's capabilities, the script converts ADCIRC NetCDF format data into contours, facilitating the creation of various GIS file formats and map plots. It addresses specific challenges encountered by the CERA team to ensure the production of clean geometries, essential for seamless integration into GIS workflows and effective utilization by GIS specialists and emergency managers.

Key highlights of this tutorial include:

- Overview of the CERA software package and its role in providing storm surge and wave guidance.
- Explanation of how Matplotlib is employed to convert NetCDF data into contours.
- Discussion on the importance of clean geometries and the specific challenges addressed by the script.
  
By following this tutorial, users can gain insights into the process of contour generation from ADCIRC NetCDF data using Matplotlib, ensuring compatibility with GIS systems and enhancing the utility of storm surge guidance for emergency preparedness and response efforts.


## Getting Started

### Jupiter Notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CERA-GROUP/Tutorials/blob/main/Map_Contouring_Matplotlib/Contouring_Tutorial/cera_contour_matplotlib.ipynb) 

### Python standalone

* Direct python script [file](https://github.com/CERA-GROUP/Tutorials/blob/main/Map_Contouring_Matplotlib/Contouring_Tutorial/cera_contour_matplotlib.py).

* Check the tutorial [instructions](https://github.com/CERA-GROUP/Tutorials/blob/main/Map_Contouring_Matplotlib/Contouring_Tutorial/cera_contour_matplotlib.ipynb).

* Example ADCIRC NetCDF file [input file](https://cloud.cera.lsu.edu/s/frcZtNgANgdgCXP/download/maxele_contouring.63.nc).


        cera_contour_matplotlib.py -i (input datafile) -a (netcdf attribute name) -g (mesh file) -n (intervals) -m (maxlevel)

always use:

      -i | infile       name of the NetCDF input file containing the ADCIRC data
      -a | attrname     attribute name of the NetCDF data array
      
      The option -g is only required if the ADCIRC mesh information is not included in the data 
      input file.
      -g | grid         name of the NetCDF file containing the ADCIRC mesh (default: input file)

optional:

      -n | intervals    number of contour intervals in output file (default:30)
      -m | maxlevel     maximum data value to be used for contouring (default:highest value 
                        in data array)

## Example usage

Download the test data file (maxele.63.nc) in your script directory.

    [1] cera_contour_matplotlib.py -i maxele.63.nc -a zeta_max
![Example 1](https://github.com/CERA-GROUP/cera_contour/blob/master/example_1_plot.png)

In this example, no optional parameters (-n intervals or -m maxlevel) are specified. The default values for these options will be applied. The maxlevel uses always the original units from the input file (here: meters). The output contours will be classified as 30 levels and stretched between zero and and the maximum data value in the input file (here: 10.62 meters).

    [2] cera_contour_matplotlib.py -i maxele.63.nc -a zeta_max -m 2
![Example 2](https://github.com/CERA-GROUP/cera_contour/blob/master/example_2_plot.png)

In this example, the maxlevel is given with the option -m as 2 (meters). The output contours will be classified as 
30 levels (default value for the missing option -n (intervals). The levels will be limited to 0-2m. 

    [3] cera_contour_matplotlib.py -i maxele.63.nc -a zeta_max -n 10 -m 1
![Example 3](https://github.com/CERA-GROUP/cera_contour/blob/master/example_3_plot.png)

In this example, the output contours will be classified as 10 levels (option -n intervals) between 0-1m 
(option -m maxlevel). 

---
### Contact Us
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
