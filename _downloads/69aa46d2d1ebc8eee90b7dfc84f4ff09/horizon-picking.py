"""
Picking Horizons
~~~~~~~~~~~~~~~~

Pick a horizon along a 2.5D cross section of GPR imagery.

"""
import pyvista as pv
from pyvista import examples

path, _ = examples.downloads._download_file("gpr-line.vtu")
mesh = pv.read(path)

###############################################################################
p = pv.Plotter()
p.add_mesh(mesh)
p.enable_horizon_picking()
p.camera_position = [
    (-212.30873550953538, 359.730172722682, 59.10289856114311),
    (9.6039882161056, 8.329846888337428, -0.5391548951008538),
    (0.08754214189159452, -0.1127058489834577, 0.9897644997664596),
]
p.show()


###############################################################################
# .. image:: ../images/gpr-line.gif


###############################################################################
# Then you can access the picked surface via ``p.picked_horizon``


###############################################################################
# See `enable_horizon_picking` for more details
help(p.enable_horizon_picking)
