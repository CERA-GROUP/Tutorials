# Geospatial data processing and producing maps
# CERA Group, Louisiana State University
# Website: https://cera.coastalrisk.live
# Github: https://github.com/CERA-GROUP
############################################################################################################
#
# Import libraries
import sys
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.image as image
from matplotlib.offsetbox import (AnnotationBbox, OffsetImage, TextArea)
import numpy as np
import pandas as pd
import urllib.request
from PIL import Image
import warnings
import os
# Checking if CSV file is provided
if len(sys.argv) < 2:
    warnings.warn("No CSV file provided. Please provide a CSV file as an argument.")
    sys.exit()

# Checking if the provided CSV file exists and is readable
csv_file = sys.argv[1]
if not os.path.isfile(csv_file) or not os.access(csv_file, os.R_OK):
    sys.exit("\033[91mThe provided CSV file does not exist or is not readable. Please provide a valid CSV file.\033[0m")
    
# Part 2: Map Visualization
# 2.1 - Understanding the Matplotlib Plot Structure
# Ignore warnings
warnings.filterwarnings('ignore')

# 2.2 - Creating a basic map with Cartopy
print("\033[92mCreating a basic map with Cartopy - Plate Carrée projection\033[0m")
# Creating a map with Plate Carrée projection and add coastline
ax = plt.axes(projection=ccrs.PlateCarree()) 
ax.add_feature(cfeature.COASTLINE)
plt.show()

print("\033[92mCreating a basic map with Cartopy - Mollweide projection\033[0m")
# Creating a map with Mollweide projection and add coastline
ax = plt.axes(projection=ccrs.Mollweide(central_longitude=-90))
ax.add_feature(cfeature.COASTLINE)
plt.show()

# 2.3 - Adding a background image and customize the coastline feature
print("\033[92mCreating a map with Plate Carrée projection, adding customized coastline and a background image\033[0m")
# Creating a map with Plate Carrée projection, add customized coastline and a background image
ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE, linestyle='dotted', linewidth=1, color='red')
ax.stock_img()
plt.show()

# Part 3: Overlaying Coordinate Points on Maps
# 3.1 - Importing the CSV file
csv_file = sys.argv[1]
df_stations = pd.read_csv(csv_file)

# 3.2 - Exploring the Pandas data frame
print("\033[92mPrinting the Pandas data frame\033[0m")
df_stations.info()

# 3.3 - Mapping the point data
lon = df_stations['lon'][:]
lat = df_stations['lat'][:]

plt.plot(lon, lat, marker='o', linewidth=0)
plt.show()

# 3.4 - Adding the points to the background map
print("\033[92mAdding the points to the background map\033[0m")
plt.figure(figsize=(12,6)) 
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-45, -120, 5, 50])

ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=.6)
ax.add_feature(cfeature.OCEAN.with_scale('50m'), color='#EDFBFF')
ax.add_feature(cfeature.LAND.with_scale('50m'), color='#FBF5EA')
ax.add_feature(cfeature.LAKES.with_scale('50m'), color='#EDFBFF')
ax.add_feature(cfeature.STATES.with_scale('50m'), linewidth=.5)

gls = ax.gridlines(draw_labels=True, linestyle='dotted', color='black')
gls.top_labels=False   
gls.right_labels=False 

ax.set_title('Background map with water level stations')

plt.plot(lon, lat, color='r', marker='o', markersize=10, linewidth=0)
plt.show()

# 3.5 - Limiting the map extent to the area of interest and add point labels
print("\033[92mLimiting the map extent to the area of interest and adding point labels\033[0m")
plt.figure(figsize=(12,6)) 
ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=.6)
ax.add_feature(cfeature.OCEAN.with_scale('10m'), color='#EDFBFF')
ax.add_feature(cfeature.LAND.with_scale('10m'), color='#FBF5EA')
ax.add_feature(cfeature.LAKES.with_scale('10m'), color='#EDFBFF')
ax.add_feature(cfeature.STATES.with_scale('10m'), linewidth=.5)

gls = ax.gridlines(draw_labels=True, linestyle='dotted', color='black')
gls.top_labels=False   
gls.right_labels=False 

ax.set_title('Background map with water level stations')

plt.plot(lon, lat, color='r', marker='o', markersize=10, linewidth=0)

station_id = df_stations['station_id'][:]
for i, txt in enumerate(station_id):
  ax.annotate(txt, (lon[i]+0.2, lat[i]))

plt.xlim((lon.min()-1, lon.max()+1))
plt.ylim((lat.min()-1, lat.max()+1))

with urllib.request.urlopen('https://coastalrisk.live/wp-content/uploads/2018/05/cera_50x50.png') as url:
    logo = np.array(Image.open(url))
imagebox = OffsetImage(logo, zoom = 0.5)
ab_img = AnnotationBbox(imagebox, (lon.min()-0.6,lat.max()+0.6), bboxprops =dict(edgecolor='None'), frameon=False)
ab_text = AnnotationBbox(TextArea("cera.coastalrisk.live"), (lon.min()+0.75,lat.max()+0.6)) 
ax.add_artist(ab_img)
ax.add_artist(ab_text)

plt.show()