# This script uses the python library matplotlib (http://matplotlib.org/)
# to create contours from a single ADCIRC netcdf file.
# If multiple time steps are given in the ADCIRC netcdf file,
# the first time step will be extracted.

# Copyright (C): Carola Kaiser 2006-2026, Louisiana State University.
# This script is part of the Coastal Emergency Risks Assessment (CERA), a real-time visualization system for storm surge guidance.
# See https://cera.coastalrisk.live. This CERA script is Open Source software; distributed under the MIT License.

# script specifics and bugfixes:
# Matplotlib 'tricontourf' expects a data array, but does not support
# masked arrays. If a masked array will be passed, it will be ignored.
# The triangulation should only contain triangles with valid data at all
# three vertices. The solution is to either remove invalid triangles from
# your 'element' array before creating the triangulation, or set a mask on
# the triangulation once it has been created.
# The created contours will contain one or more polygon exteriors and
# zero or more interiors. They can be in any order (an exterior is not
# necessarily followed by its interiors). This has to be explicitly tested
# in your own script.

import sys
import argparse
from pathlib import Path

import netCDF4
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib import path
#from shapely.geometry import geo, Polygon, Point, MultiPolygon
import numpy
from operator import itemgetter

###############################################################################
def create_command_line_parser():
  parser = argparse.ArgumentParser(
    description='Extract contours from an ADCIRC NetCDF file.')

  parser.add_argument('-i', '--infile', required=True,
    help='name of the NetCDF input file containing the ADCIRC data')
  parser.add_argument('-a', '--attrname', required=True,
    help='attribute name of the NetCDF data array')
  parser.add_argument('-g', '--grid',
    help='optional: name of the NetCDF file containing the ADCIRC mesh (default: input file)')
  parser.add_argument('-n', '--intervals', type=int, default=30,
    help='number of contour intervals in the output plot (default: 30)')
  parser.add_argument('-m', '--maxlevel', type=float,
    help='maximum data value to be used for contouring (default: highest value in data array)')
  parser.add_argument('-o', '--output', type=Path,
    help='save the contour map to this image file')
  parser.add_argument('--dpi', type=int, default=300,
    help='resolution for saved images (default: 300)')
  parser.add_argument('--no-show', action='store_true',
    help='do not open the interactive plot window')

  return parser

###############################################################################
def validate_output_path(output):
  if output is None:
    return None
  if output.parent and not output.parent.exists():
    raise ValueError("Output directory does not exist: %s" % output.parent)
  return output

###############################################################################
# read x,y from the grid file or the input file if grid is not given
def get_netcdf_grid(gridfile):

  gridvars = netCDF4.Dataset(gridfile).variables

  # get variable names for x, y depending on grid
  if 'x' in gridvars:
    var_x = 'x'
    var_y = 'y'
    var_element = 'element'
  else:
    var_x = 'lon'
    var_y = 'lat'
    var_element = 'ele'

  x = gridvars[var_x][:]
  y = gridvars[var_y][:]
  elems = gridvars[var_element][:,:]-1  # Move to 0-indexing by subtracting 1, elements indexing starts with '1' in netcdf file

  if x is None or y is None or elems is None:
    print("*** ERROR *** No 'x (lon)', 'y (lat)', or 'element (ele)' data array given in file '%s'" % gridfile)
    sys.exit(-1)

  return x, y, elems

#############################################################
# read the 'attribute name' data array from the input file
def get_netcdf_data(infile, attrname):

  vars = netCDF4.Dataset(infile).variables
  data = vars[attrname][:]

  if data is None:
    print("*** ERROR *** No '%s' data array given in file '%s'" % (attrname, infile))
    sys.exit(-1)

  # timesteps layer
  if len(data.shape) > 1:
    print("*** The data file contains multiple time steps. The first time step (0) will be extracted.")
    return data[0]

  return data

###############################################################################
# cera_contour_matplotlib.py -i [infile] -a [attrname] <-g [gridfile] -n [intervals] -m [maxlevel]>
def create_contours(argv=None):

  # analyse command line
  args = create_command_line_parser().parse_args(argv)

  infile = args.infile
  attrname = args.attrname
  gridfile = args.grid if args.grid is not None else infile

  # tricontourf draws one fewer band than the number of levels
  intervals = args.intervals + 1

  try:
    output = validate_output_path(args.output)
  except ValueError as exc:
    raise SystemExit("Error: %s" % exc) from exc

  ###############################
  # get grid data from netcdf grid or input file
  x, y, elems = get_netcdf_grid(gridfile)

  # get data from 'attrname' array in netcdf input file
  data = get_netcdf_data(infile, attrname)

  if args.maxlevel is None:
    # highest value in data array is used
    maxlevel = data.max()
  else:
    maxlevel = args.maxlevel

  ###############################
  # matplotlib: triangulation
  print('\nTriangulating ...\n')
  triang = tri.Triangulation(x, y, triangles=elems)

  ###############################
  # Mask out triangles containing masked data (data == -99999)
  # Do this after the triangulation.

  # check if data array is masked
  try:
    if data.mask.any():
      # -99999 entries in 'data' array are usually masked, mask all corresponding triangles
      point_mask_indices = numpy.where(data.mask)
      tri_mask = numpy.isin(elems, point_mask_indices).reshape(-1, 3).any(axis=1)
      triang.set_mask(tri_mask)

  except AttributeError:
    # the "mask" attribute was not found, assume that no -99999 values are in the dataset
    print("No 'mask' attribute found in file '%s'" % infile)

  levels = numpy.linspace(0, maxlevel, num=intervals)
  # print("levels: %s\n" % levels)

  #############################################################################
  print('Making contours ...\n')

  # pyplot color plot
  c = plt.tricontourf(triang, data, levels=levels, cmap=plt.cm.jet, extend='both')
  c.cmap.set_under("#000066")
  c.cmap.set_over("#880066")
  plt.colorbar(c, ticks=levels)

  if output is not None:
    plt.savefig(output, dpi=args.dpi, bbox_inches='tight')
    print("Saved contour map to %s" % output)

  if args.no_show:
    plt.close()
  else:
    plt.show()

###############################################################################
def main(argv=None):
  if argv is None:
    argv = sys.argv[1:]

  # create contours with matplotlib
  return create_contours(argv)

if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
