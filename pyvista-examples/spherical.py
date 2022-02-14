"""
Spherical Data
~~~~~~~~~~~~~~

Originally posted: https://github.com/pyvista/pyvista-support/issues/67

See also https://docs.pyvista.org/examples/02-plot/spherical.html
"""

import numpy as np
import pyvista as pv
from pyvista import examples
import xarray as xr

path, _ = examples.downloads._download_file("lsm_4x5.nc")

lsm = xr.open_dataarray(path)

xx, yy, zz = np.meshgrid(
    np.radians(
        np.arange(
            0,
            365,
            5,
        )
    ),
    np.radians(np.arange(-90, 94, 4)),
    [0],
)

###############################################################################
# Transform to spherical coordinates
radius = 6371.0e6
x = radius * np.cos(yy) * np.cos(xx)
y = radius * np.cos(yy) * np.sin(xx)
z = radius * np.sin(yy)

###############################################################################
# Create PyVista mesh
grid = pv.StructuredGrid(x, y, z)
grid.cell_data["lsm"] = np.array(lsm).ravel(order="F")

###############################################################################
# Visualize!
grid.plot()
