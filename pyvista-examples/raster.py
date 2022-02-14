"""
Read a raster using xarray
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use xarray and rasterio to load a raster into a StructuredGrid.
"""

import numpy as np
import pyvista as pv
from pyvista import examples
from rasterio.warp import transform
import rioxarray

##############################################################################
# The following is a function you can use to load just about any geospatial
# raster.


def read_raster(filename, out_crs="EPSG:3857", use_z=False):
    """Read a raster to a ``pyvista.StructuredGrid``.

    This will handle coordinate transformations.
    """
    # Read in the data
    filename = path
    data = rioxarray.open_rasterio(filename)
    values = np.asarray(data)
    data.rio.nodata
    nans = values == data.rio.nodata
    if np.any(nans):
        # values = np.ma.masked_where(nans, values)
        values[nans] = np.nan
    # Make a mesh
    xx, yy = np.meshgrid(data["x"], data["y"])
    if use_z and values.shape[0] == 1:
        # will make z-comp the values in the file
        zz = values.reshape(xx.shape)
    else:
        # or this will make it flat
        zz = np.zeros_like(xx)
    mesh = pv.StructuredGrid(xx, yy, zz)
    pts = mesh.points
    lon, lat = transform(data.rio.crs, out_crs, pts[:, 0], pts[:, 1])
    mesh.points[:, 0] = lon
    mesh.points[:, 1] = lat
    mesh["data"] = values.reshape(mesh.n_points, -1, order="F")
    return mesh


##############################################################################
# Download a sample GeoTiff to demonstrate
path, _ = examples.downloads._download_file("Elevation.tif")

##############################################################################
# Use the utility function to load that file.
topo = read_raster(path, use_z=True)
topo

##############################################################################
topo.plot()
