"""
Read a raster using xarray
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use xarray and rasterio to load a raster into a StructuredGrid.
"""

import pyvista as pv
import xarray as xr
import numpy as np


def read_raster(filename):
    """
    Helpful: http://xarray.pydata.org/en/stable/auto_gallery/plot_rasterio.html
    """
    # Read in the data
    data = xr.open_rasterio(filename)
    values = np.asarray(data)
    nans = values == data.nodatavals
    if np.any(nans):
        # values = np.ma.masked_where(nans, values)
        values[nans] = np.nan
    # Make a mesh
    xx, yy = np.meshgrid(data["x"], data["y"])
    zz = values.reshape(xx.shape)  # will make z-comp the values in the file
    # zz = np.zeros_like(xx) # or this will make it flat
    mesh = pv.StructuredGrid(xx, yy, zz)
    mesh["data"] = values.ravel(order="F")
    return mesh


# TODO: find raster we can use
# topo = read_raster('topography.tif')
