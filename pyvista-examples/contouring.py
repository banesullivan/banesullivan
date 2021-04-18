"""
Creating a Contour Map
~~~~~~~~~~~~~~~~~~~~~~

Creating a contour map from a DEM mesh

"""
# sphinx_gallery_thumbnail_number = 2
import pyvista as pv
from pyvista import examples
import numpy as np
import matplotlib.pyplot as plt

###############################################################################
path, _ = examples.downloads._download_file("Sio020320.vtp")
mesh = pv.read(path).elevation()
mesh

###############################################################################
# Get a min/max range of the elevation
z = mesh["Elevation"]
mi, ma = round(min(z), ndigits=-2), round(max(z), ndigits=-2)
mi, ma

###############################################################################
# create values to contour at
step = 10
cntrs = np.arange(mi, ma + step, step)
cntrs

###############################################################################
# Run the contouring filter
contours = mesh.contour(cntrs, scalars="Elevation")

###############################################################################
p = pv.Plotter()
p.add_mesh(mesh)
p.add_mesh(contours, line_width=5, color="black")
p.camera_position = [
    (469978.85959530954, 1322266.5229163894, 5293.630545897349),
    (469956.03091019404, 1321834.8498636105, 5194.622946764996),
    (0.0037194010444579987, -0.2237385074834842, 0.9746421119184896),
]
p.show()

###############################################################################
# Create a 2D contour map
x, y = contours.points[:, 0], contours.points[:, 1]

plt.scatter(x, y, s=1, marker=".")
