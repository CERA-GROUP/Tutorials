# This script uses the python library matplotlib (http://matplotlib.org/)
# to create contours from a single ADCIRC netcdf file.
# If multiple time steps are given in the ADCIRC netcdf file,
# the first time step will be extracted.

# Copyright (C): Carola Kaiser 2014-2023, Louisiana State University
# Based on an idea by Rusty Holleman. With special thanks to Ian Thomas 
# from the matplotlib developer team for helping us create clean geometries.

# This script is part of the Coastal Emergency Risks Assessment (CERA),
# a real-time visualization system for ADCIRC storm surge guidance.
# See https://cera.coastalrisk.live.
# Thus CERA script is Open Source software; distributed under the Boost Software
# License, Version 1.0. (See accompanying file LICENSE_1_0.txt or copy
# at http://www.boost.org/LICENSE_1_0.txt)

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

import os, sys
import optparse
import netCDF4
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib import path
from shapely.geometry import geo, Polygon, Point, MultiPolygon
import numpy
from operator import itemgetter

###############################################################################
def create_command_line_parser():
  parser = optparse.OptionParser(
    description='Extract contours from an ADCIRC netcdf file.',
    add_help_option=False)

  parser.add_option('-a', dest='attrname',
    help='attribute name of the NetCDF data array')
  parser.add_option('-g', dest='grid',
    help='optional: name of the NetCDF file containing the ADCIRC mesh (default: input file)')
  parser.add_option('-i', dest='infile',
    help='name of the NetCDF input file containing the ADCIRC data')
  parser.add_option('-m', dest='maxlevel',
    help='maximum data value to be used for contouring [default:highest value in data array]')
  parser.add_option('-n', dest='intervals',
    help='number of contour intervals in output file [default:30]')
  parser.add_option('-?', action='help',
    help='print this message and exit')

  return parser

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
def signed_area(ring):
  v2 = numpy.roll(ring, -1, axis=0)
  return numpy.cross(ring, v2).sum() / 2.0

def classify_polygons(polys):
  exteriors = []
  interiors = []
  for p in polys:
    if signed_area(p) >= 0:
      exteriors.append(p)
    else:
      interiors.append(p)

  return exteriors, interiors

def points_inside_poly(points, polygon):
  p = path.Path(polygon)
  return p.contains_points(points)

def reverse_geometry(p):
  return numpy.flipud(p)

###############################################################################
def extract_geometries(contour, data_min, data_max):
  geoms = []
  vars = []

  # create list of tuples (geom, vmin, vmax)
  num_collections = len(contour.collections)
  for colli, coll in enumerate(contour.collections):

    # tricontourf generates extra collections for all geometries below
    # and above the given levels
    if colli == 0:
      vmin, vmax = data_min, contour.levels[colli]
    elif colli == num_collections-1:
      vmin, vmax = contour.levels[colli-1], data_max
    else:
      vmin, vmax = contour.levels[colli-1:colli+1]

    for p in coll.get_paths():
      p.simplify_threshold = 0.0
      polys = p.to_polygons()

      # don't append an empty polygon to the geometry or it will mess up
      # the indexing
      if polys:
        # remove all geometries with less than 3 points
        polys = [p for p in polys if p.shape[0] >= 3]

        # exteriors and interiors can be in any order (an exterior is not
        # necessarily followed by its interiors - test it!)
        exteriors, interiors = classify_polygons(polys)
        if len(interiors) > 0:
          interior_points = [pts[0] for pts in interiors]

        overall_inout = numpy.zeros((len(interiors),), dtype=bool)

        for exterior in exteriors:
          if len(interiors) > 0:
            inout = points_inside_poly(interior_points, exterior)
            overall_inout = numpy.logical_or(overall_inout, inout)

            my_interiors = [g for i, g in enumerate(interiors) if inout[i]]
            poly = Polygon(exterior, my_interiors)

          else:
            poly = Polygon(exterior)

          # clean-up polygons (remove intersections)
          if not poly.is_valid:
            poly = poly.buffer(0.0)

          geoms.append(poly)
          vars.append((vmin, vmax))

        # collect all interiors which do not belong to any of the exteriors
        outer_interiors = [interior for i, interior in enumerate(interiors) if not overall_inout[i]]
        for geom in outer_interiors:
          poly = Polygon(reverse_geometry(geom))

          # clean-up polygons (remove intersections)
          if not poly.is_valid:
            poly = poly.buffer(0.0)

          geoms.append(poly)
          vars.append((vmin, vmax))

  return geoms, vars

###############################################################################
# cera_contour_matplotlib.py -i [infile] -a [attrname] <-g [gridfile] -n [intervals] -m [maxlevel]>"
def create_contours(argv):

  # analyse command line
  parser = create_command_line_parser()
  try:
    options, args = parser.parse_args(argv)
  except optparse.OptionError as e:
    print("*** ERROR *** %s\n\n" % str(e))
    sys.exit(-1)

  # command line sanity checks
  if (options.infile is None):
    print("*** ERROR *** Missing option -i [infile]")
    sys.exit(-1)
  infile = options.infile

  if (options.attrname is None):
    print("*** ERROR *** Missing option -a [attrname]")
    sys.exit(-1)
  attrname = options.attrname

  if (options.grid is None):
    gridfile = infile
  else:
    gridfile = options.grid

  if options.intervals is None:
    intervals = 31
  else:
    intervals = int(options.intervals) + 1

  ###############################
  # get grid data from netcdf grid or input file
  x, y, elems = get_netcdf_grid(gridfile)

  # get data from 'attrname' array in netcdf input file
  data = get_netcdf_data(infile, attrname)

  if options.maxlevel is None:
    # highest value in data array is used
    maxlevel = data.max()
  else:
    maxlevel = float(options.maxlevel)

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
      tri_mask = numpy.any(numpy.in1d(elems, point_mask_indices).reshape(-1, 3), axis=1)
      triang.set_mask(tri_mask)

  except AttributeError:
    # the "mask" attribute was not found, assume that no -99999 values are in the dataset
    print("No 'mask' attribute found in file '%s'" % infile)

  levels = numpy.linspace(0, maxlevel, num=intervals)
  # print("levels: %s\n" % levels)

  #############################################################################
  print('Making contours ...\n')
  contour = plt.tricontourf(triang, data, levels=levels, extend='both')

  # extracting contour shapes from tricontourf object
  print('Extracting contour geometries ...')
  geoms, vars = extract_geometries(contour, data.min(), data.max())

  # pyplot color plot
  c = plt.tricontourf(triang, data, levels=levels, cmap=plt.cm.jet, extend='both')
  c.cmap.set_under("#000066")
  c.cmap.set_over("#880066")
  plt.colorbar(c, ticks=levels)
  plt.show()

###############################################################################
def main(argv):
  if len(argv) < 5:
    print("Usage: cera_contour_matplotlib.py -i [input datafile] -a [netcdf attribute name] <optional: -g [gridfile] -n [intervals] -m [maxlevel]>")
    sys.exit(-1)

  # create contours with matplotlib
  return create_contours(argv)

if __name__ == "__main__":
  sys.exit(main(sys.argv))
