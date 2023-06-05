"""
Intro to PyVista
----------------

I don't have all that many posts in the gallery yet, so I thought I'd put this
very basic introduction to PyVista in here.

`PyVista <https://docs.pyvista.org>`_ is a 3D data management, visualization,
and mesh analysis framework in Python, and yours truly is one of its creators!
PyVista is capable of handling 3D spatial data structures with arbitrary
geometries. As such, it is able to represent just about any 3D spatially
referenced data set, geoscientific or not!

If you really want to learn more about PyVista, head over to its
`gallery <https://docs.pyvista.org/examples/index.html>`_
(I have created many of those examples).

In this brief demo, I'm going to load some example data and demonstrate how to
plot and filter the 3D meshes.

Getting to it
~~~~~~~~~~~~~

So what is a "3D spatially referenced data"?...

In PyVista, a "mesh" is a geometrical representation of a surface or volume
in 3D space that can have any information associated to those locations/regions
in space.
We commonly refer to any spatially referenced dataset as a mesh, so often the
distinction between a mesh, a grid, and a volume can get fuzzy - but that does
not matter in PyVista as we have worked really hard to make working with these
spatial data structures as simple as possible.
For more details, check out:
`What is a mesh? <https://docs.pyvista.org/getting-started/what-is-a-mesh.html>`_

Anyways, let's look at some code and especially some 3D visualizations!

"""
import pyvista as pv
from pyvista import examples

# Load OMF archive as PyVista MultiBlock dataset
model = examples.download_damavand_volcano()
model


###############################################################################
# Initial Inspection
# ~~~~~~~~~~~~~~~~~~
#
# Now we can go ahead and create a visualization of the 3D model of the region
# surrounding the Damavand Volcano.
# All we have to do is pass the mesh to the :class:`pyvista.Plotter`'s
# ``add_mesh`` method with keyword arguments for how we want it displayed
# (e.g. color, opacity, etc.).
#
# Below, I define an opacity mapping and colorbar limits:

opacity = [0, 0.75, 0, 0.75, 1.0]
clim = [0, 100]

###############################################################################
# Now I instantiate the ``Plotter`` and create the visualization.

p = pv.Plotter()
p.add_volume(
    model,
    cmap="magma",
    clim=clim,
    opacity=opacity,
    opacity_unit_distance=6000,
)
p.show()

###############################################################################
# And just like that, we have a 3D rendering of all that data!
# Isn't PyVista awesome?!

###############################################################################
# But hold on, that’s a big volume! We probably don’t want to volume render the
# whole thing. So let’s extract a region of interest under the volcano.
#
# The region we will extract will be between nodes 175 and 200 on the x-axis,
# between nodes 105 and 132 on the y-axis, and between nodes 98 and 170 on the
# z-axis.

voi = model.extract_subset([175, 200, 105, 132, 98, 170])

p = pv.Plotter()
p.add_mesh(model.outline(), color="k")
p.add_mesh(voi, cmap="magma")
p.show()

###############################################################################
# Let’s now volume render that region of interest!

p = pv.Plotter()
p.add_volume(voi, cmap="magma", clim=clim, opacity=opacity, opacity_unit_distance=2000)
p.camera_position = [
    (531554.5542909054, 3944331.800171338, 26563.04809259223),
    (599088.1433822059, 3982089.287834022, -11965.14728669936),
    (0.3738545892415734, 0.244312810377319, 0.8947312427698892),
]
p.show()


###############################################################################
pv.Report()
