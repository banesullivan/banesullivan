"""
Geological Cross Section
~~~~~~~~~~~~~~~~~~~~~~~~

Plot a geological cross section in 3D space.

We have a cross section PNG image and we know three coordinates along that section:

* This section goes from +200m to -2000m in vertical extent
* Coordinates of the start point: 32362837 5769796
* Coordinates of the bend: 32368424 5765456 (the bending point is indicated with a * "K" at around half the section)
* Coordinates of the end point: 32374114 5763507


Originally posted: https://github.com/pyvista/pyvista-support/issues/272
"""

import numpy as np
import pyvista as pv
from pyvista import examples

###############################################################################
# Parameters for cross section
zrng = [-2000, 200]
start = [32362837, 5769796]
bend = [
    32368424,
    5765456,
]  # (the bending point is indicated with a "K" at around half the section)
end = [32374114, 5763507]

###############################################################################
# Make a surface mesh representing that coverage/ This mesh consists of 6
# points. Generate them:

#   a-----b-----e
#   |     |     |
#   |     |     |
#   d-----c-----f
a = start + [
    zrng[1],
]
b = bend + [
    zrng[1],
]
c = bend + [
    zrng[0],
]
d = start + [
    zrng[0],
]
e = end + [
    zrng[1],
]
f = end + [
    zrng[0],
]

###############################################################################
# Now make a poly data mesh of these points
points = np.array([a, b, c, d, e, f]).astype(float)
faces = np.array([4, 0, 1, 2, 3, 4, 1, 4, 5, 2])
surface = pv.PolyData(points, faces)

###############################################################################
# Map the texture to the mesh.
# - We know the tcoords of a, d, e, & f, but not necessarily b & c
# - to find them, scale by cell sizes:
# - Get the width of the two cells to find those coords
w = surface.compute_cell_sizes()["Area"] / np.ptp(zrng)
tw = (w / np.sum(w))[0]

# Generate Tcoords now!
t_coords = np.array(
    [
        [0, 1],
        [tw, 1],
        [tw, 0],
        [0, 0],
        [1, 1],
        [1, 0],
    ]
)
surface.active_t_coords = t_coords

###############################################################################
# Load the texture image
path, _ = examples.downloads._download_file("geo-cross-section.png")
texture = pv.Texture(path)

###############################################################################
# Plot it up!
cpos = [
    (32361897.379640546, 5777033.66791174, 341.48314909204873),
    (32366747.758752592, 5766374.637744438, -1142.521946006218),
    (0.047926147231751065, -0.11631040130754997, 0.9920559333823861),
]
surface.plot(texture=texture, cpos=cpos, show_edges=True)
