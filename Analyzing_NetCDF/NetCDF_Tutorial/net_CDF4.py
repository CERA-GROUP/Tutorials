# Reading and parsing NetCDF data
# CERA Group, Louisiana State University
# Website: https://cera.coastalrisk.live
# Github: https://github.com/CERA-GROUP
############################################################################################################

# importing libraries
import netCDF4
import numpy as np
import sys
from datetime import datetime
# Get the current date and time
now = datetime.now()
# Format the current date and time as a string
timestamp = now.strftime('%Y%m%d_%H%M%S')
# Open the file in write mode
sys.stdout = open(f'output_{timestamp}.txt', 'w')
############################################################################################################

# reading in the NetCDF file
mynetcdf = netCDF4.Dataset('maxele.63.nc')

# getting the attributes (metadata) of the file
print(mynetcdf)

# getting all variables names as contained in the file by printing the dictionary ’keys’
all_variable_names = mynetcdf.variables.keys()
print(all_variable_names)

# getting a list of all variable attributes (metadata) in the file
# note, this does not print any data but just the attributes
for attrs in mynetcdf.variables.values():
   print(attrs)

# accessing the attributes (metadata) of the variable ’x’ (longitudes) and  the variable ’y’ (latitudes)
print(mynetcdf.variables['x'], mynetcdf.variables['y'])


# getting a list of all dimensions(size) dictionary's keys in the file
for dims in mynetcdf.dimensions.values():
   print(dims)

# accessing the dimension of the variable ’x’ (longitudes)
print(mynetcdf.dimensions['node'])	

# Printing the List of all variable attributes in the file or the
# Attributes of a specific variable, the attribute section also
# contains the information of the dimension of the particular variable.
for attrs in mynetcdf.variables.values():
   print(attrs)
print(mynetcdf.variables['time'])

# getting the variable dimension size with the NumPy functionality ’shape’
print("Array Dimension x = ", (mynetcdf.variables['x'].shape) )
print("Array Dimension element = ", (mynetcdf.variables['element'].shape))

# Or even bettter if you want every variable size
for dims in mynetcdf.variables:
   #print (dims)
   print("Array Dimension", dims , " = ", (mynetcdf.variables[dims].shape) )


# getting all data values from an one-dimensional array
x = mynetcdf.variables['x'][:]
print(x)
print("number of values: %s " % len(x)) 

# getting all data values from a two-dimensional array
elems = mynetcdf.variables['element'][:,:]
print(elems)

# getting the first value from the ‘x’ data array
x = mynetcdf.variables['x'][0] # NumPy arrays are 0-indexed
print(x)

# getting the first entry of the second value from the ‘element’ data array
# zero-indexed (second row, first column)
elem = mynetcdf.variables['element'][1,0]
print(elem) 

# from the second row in the ‘element’ array, getting the first two entries 
elems = mynetcdf.variables['element'][1,0:2] #zero-indexed 
print(elems)

# getting the first value from the ‘time’ data array
z = mynetcdf.variables['zeta_max'][:]
z_slice = np.intersect1d(np.where(np.array(z)<0.6),np.where(np.array(z)>0.5))                              
print(z_slice)
print("number of returned values: %s " % len(z_slice))   


# Close the file
sys.stdout.close()





