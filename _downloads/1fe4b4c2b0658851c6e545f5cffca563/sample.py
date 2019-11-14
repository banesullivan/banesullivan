"""
Intro to PyVista
----------------

I don't have all that many posts in the gallery yet, so I thought I'd put this
very basic introduction to PyVista in here.

PyVista is 3D mesh analysis and visualizaton library in Python. It is capable
of handle 3D finite difference/volume spatial data strucutres with arbitrary
geometries. As such, it is capable of representing just about any 3D spatially
referenced data set.

In this brief example, I'm going to load a few example meshes, maybe create
one from scratch, and visualize them in 3D. (at the moment, this is super
basic - I'll get back to updating this later!).

If you really want to learn more about PyVista, head over to its
`gallery <https://docs.pyvista.org/examples/index.html>`_
(I have created many of those examples).

"""
import pyvista as pv
from pyvista import examples

mesh = examples.download_st_helens()
mesh

###############################################################################
mesh.plot(cpos='xy')

###############################################################################
# Here we can apply a filter to alter the mesh: warp it by a scalar attribute,
# elevation in this case:
topo = mesh.warp_by_scalar()

p = pv.Plotter()
p.add_mesh(topo)
p.show()
