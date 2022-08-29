"""
Mine Pit Imagery
~~~~~~~~~~~~~~~~

Triangulate a surface from a point cloud of points and overlay imagery of a
mine pit.

Originally posted: https://github.com/pyvista/pyvista-support/issues/159
"""
# sphinx_gallery_thumbnail_number = 2
import numpy as np
import pooch
import pyvista as pv
import rioxarray

###############################################################################
url = "https://raw.githubusercontent.com/pyvista/vtk-data/master/Data/Sio020320.csv"
file_path = pooch.retrieve(url=url, known_hash=None)

points = np.loadtxt(file_path, skiprows=1, delimiter=",")[:, 1:]
cloud = pv.PolyData(points)
# Plot the point cloud with a special rendering technique
cloud.plot(eye_dome_lighting=True)


###############################################################################
# Triangulate the points

# This will take a minute
surf = cloud.delaunay_2d(progress_bar=True)

###############################################################################
# Open the GeoTIFF
url = "https://dl.dropbox.com/s/pqgme8qsl95u9un/Sio020320_transparent_mosaic_group1.tif?dl=0"
path = pooch.retrieve(url=url, known_hash=None)
ds = rioxarray.open_rasterio(path)

# Fetch the texture as an image
image = np.moveaxis(ds.values, 0, -1)

# Create the ground control points for texture mapping
o = ds.x.min(), ds.y.min(), 0.0  # Bottom Left
u = ds.x.max(), ds.y.min(), 0.0  # Bottom Right
v = ds.x.min(), ds.y.max(), 0.0  # Lop left
# Note: Z-coordinate doesn't matter

###############################################################################
# Use the GCPs to map the tex coords
mapped_surf = surf.texture_map_to_plane(o, u, v)

# Associate the texture with the mapped mesh
mapped_surf.textures["aerial"] = pv.numpy_to_texture(image)

###############################################################################
# Plot it up in 3D and enjoy!
cpos = [
    (469735.37431312964, 1321523.2987377762, 5242.9129552423465),
    (469928.4268006842, 1321916.1316302174, 5171.6505267522025),
    (0.08372003361058433, 0.13788753708579846, 0.986903228836878),
]
mapped_surf.plot(texture="aerial", cpos=cpos)
