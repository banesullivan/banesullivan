"""
Intro to PyVista
----------------

I don't have all that many posts in the gallery yet, so I thought I'd put this
very basic introduction to PyVista in here.

`PyVista <https://www.pyvista.org>`_ is a 3D data management, visualization,
and mesh analysis framework in Python, and yours truly is one of its creators!
PyVista is capable of handling 3D spatial data structures with arbitrary
geometries. As such, it is able to represent just about any 3D spatially
referenced data set, geoscientific or not!

If you really want to learn more about PyVista, head over to its
`gallery <https://docs.pyvista.org/examples/index.html>`_
(I have created many of those examples).

In this brief demo, I'm going to load data from the
`FORGE Geothermal Research Site <https://utahforge.com/>`_ using a companion
package, `omfvista <https://opengeovis.github.io/omfvista/>`_ for reading
`Open Mining Format (OMF) <https://omf.readthedocs.io/en/latest/>`_ archives.

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
import omfvista

# Load OMF archive as PyVista MulitBlock dataset
project = omfvista.download_forge_example()
project


###############################################################################
# Initial Inspection
# ~~~~~~~~~~~~~~~~~~
#
# Now we can go ahead and create an integrated visualization of all of the
# data available to in the ``project`` :class:`pyvista.MultiBlock` container.
# All we have to do is index the ``project`` container by the name of the
# dataset that we want to acess. We can then pass those meshes to the
# :class:`pyvista.Plotter`'s ``add_mesh`` method with keyword arguments for how
# we want it displayed (e.g. color, opacity, etc.).

p = pv.Plotter()
p.add_mesh(project["Site Boundary"],
           color="yellow", render_lines_as_tubes=True)
p.add_mesh(project["Terrain"],
           texture="geo_aer", opacity=0.7, lighting=False)
p.add_mesh(project["Opal Mound Fault"],
           color="brown", opacity=0.7)
p.add_mesh(project["Negro Mag Fault"],
           color="lightblue", opacity=0.7)
p.add_mesh(project["Observed Temperature"],
           cmap="coolwarm", clim=[10,270], point_size=10,
           render_points_as_spheres=True)

p.enable_anti_aliasing()
p.enable_depth_peeling()
p.camera_position = [(315661.9406719345, 4234675.528454831, 15167.291249498076),
                     (337498.00521202036, 4260818.504034578, -1261.5688408692681),
                     (0.2708862567924439, 0.3397398234107863, 0.9006650255615491)]
p.show()

###############################################################################
# And just like that, we have a 3D rendering of all that data!
# Isn't PyVista awesome?!
