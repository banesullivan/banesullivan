"""
Stuff
-----

This is some stuff, yo!

"""
import pyvista as pv
from pyvista import examples

mesh = examples.download_nefertiti()
###############################################################################
p = pv.Plotter()
p.add_mesh(mesh, color=True)
p.show()
