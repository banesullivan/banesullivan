"""
Vertical Exaggeration
~~~~~~~~~~~~~~~~~~~~~

Originally posted: https://github.com/pyvista/pyvista-support/issues/8
"""
import PVGeo

# sphinx_gallery_thumbnail_number = 2
import pooch
import pyvista as pv

###############################################################################
# Load data files using PVGeo
url = "https://raw.githubusercontent.com/pyvista/vtk-data/master/Data/gravi.txt"
gpath = pooch.retrieve(url=url, known_hash=None)
url = "https://raw.githubusercontent.com/pyvista/vtk-data/master/Data/surf.txt"
ppath = pooch.retrieve(url=url, known_hash=None)

gravi = PVGeo.ubc.GravObsReader().apply(gpath)
psurf = PVGeo.ubc.TopoReader().apply(ppath)

# Filter points of topo to a surface
surf = psurf.delaunay_2d()

###############################################################################
gargs = dict(
    point_size=5.0,
    render_points_as_spheres=True,
    cmap="bwr",
    clim=[-50, 110],
    scalar_bar_args={"title": "Residuals"},
)
sargs = dict(cmap="gist_earth")


p = pv.Plotter()
p.add_mesh(gravi, **gargs)
p.add_mesh(surf)
p.camera_position = [
    (259020.43748942937, 5129530.509280042, 13023.703775334989),
    (270665.9132071607, 5119041.602718343, -837.0133710551552),
    (0.39114802616415034, -0.5453684907934401, 0.7413342234630576),
]
p.show()

###############################################################################
p = pv.Plotter()
p.add_mesh(gravi, **gargs)
p.add_mesh(surf, **sargs)
p.set_scale(zscale=5)
p.show()
