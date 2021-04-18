"""
Voxelize Points
~~~~~~~~~~~~~~~

Create voxels/blocks for eavery point in a gridded point cloud

Originally posted: https://github.com/pyvista/pyvista-support/issues/178

Seee also https://pvgeo.org/examples/filters-general/voxelize-points.html#voxelize-points
"""

import pyvista as pv
import numpy as np
import PVGeo

points = np.loadtxt("data/points3d.txt")
pc = pv.PolyData(points)

###############################################################################
grid = PVGeo.filters.VoxelizePoints().apply(pc)

###############################################################################
p = pv.Plotter(notebook=0)
p.add_mesh(grid, opacity=0.5, show_edges=True)
p.add_mesh(pc, point_size=5, color="red")
p.show_grid()
p.camera_position = [
    (79.33386539265953, 67.31649454630514, 34.0649093635989),
    (35.68180551703578, 60.72062545602169, 29.136616698279703),
    (-0.11000016621558596, -0.014573551603326722, 0.9938247204744952),
]
p.show()
