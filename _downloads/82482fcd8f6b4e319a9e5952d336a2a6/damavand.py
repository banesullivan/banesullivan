"""
Damavand Volcano
~~~~~~~~~~~~~~~~

Visualize 3D models of Damavand Volcano, Alborz, Iran.

This is an adaption of `Alexey Pechnikov <https://orcid.org/0000-0001-9626-8615>`_ and `A.V.Durandin <https://orcid.org/0000-0001-6468-9757>`_'s `ParaView-MoshaFault <https://github.com/mobigroup/ParaView-MoshaFault>`_.

See LinkedIn posts for more details:

- `The slices of the 3D model of the density on the Mosha fault area, North Iran <https://www.linkedin.com/posts/activity-6610080454911631360-97-V/>`_

- `Comparing Magnetic and Gravity Data to the Mosha Fault Area <https://www.linkedin.com/posts/activity-6609736436344201216-Kxls/>`_

- `North Iran, Mosha fault <https://www.linkedin.com/posts/activity-6609681862937853952-2BPG/>`_

- `North Iran <https://www.linkedin.com/posts/activity-6609486793676996608-ZF-J/>`_


Originally posted: https://github.com/banesullivan/damavand-volcano
"""
import numpy as np

# sphinx_gallery_thumbnail_number = 6
import pyvista as pv
from pyvista import examples

###############################################################################
a, _ = examples.downloads._download_file("gebco7510_49cl.stl")
b, _ = examples.downloads._download_file("gebco7510_55cl.stl")
c, _ = examples.downloads._download_file("AOI.Damavand.32639.vtp")

gebco = examples.download_damavand_volcano()
gebco_a = pv.read(a)
gebco_b = pv.read(b)
aoi = pv.read(c)

###############################################################################
opacity = [0, 0.75, 0, 0.75, 1.0]
clim = [0, 100]

p = pv.Plotter()
p.add_volume(
    gebco,
    cmap="magma",
    clim=clim,
    opacity=opacity,
    opacity_unit_distance=6000,
)
p.show()

###############################################################################
voi = gebco.extract_subset([175, 200, 105, 132, 98, 170])

p = pv.Plotter()
p.add_mesh(gebco.outline(), color="k")
p.add_mesh(voi, cmap="magma")
p.show()

###############################################################################
p = pv.Plotter()
p.add_volume(voi, cmap="magma", clim=clim, opacity=opacity, opacity_unit_distance=2000)
p.camera_position = [
    (531554.5542909054, 3944331.800171338, 26563.04809259223),
    (599088.1433822059, 3982089.287834022, -11965.14728669936),
    (0.3738545892415734, 0.244312810377319, 0.8947312427698892),
]
p.show()

###############################################################################
contours = voi.contour(np.arange(5, 55, 5))
contours

###############################################################################
contours.plot(cmap="nipy_spectral", opacity=0.15)

###############################################################################
roi = [*voi.bounds[0:4], *aoi.bounds[4:6]]
aoi_clipped = aoi.clip_box(roi, invert=False)
pv.plot([aoi, pv.Box(roi).outline()], cpos="xy")

###############################################################################
p = pv.Plotter(window_size=np.array([1024, 768]) * 2)

# Add all the data we want to see
p.add_mesh(contours, cmap="nipy_spectral", opacity=0.15)
p.add_mesh(gebco_a, color="#ff0000")
p.add_mesh(gebco_b, color="#ff0000")
p.add_mesh(aoi_clipped, cmap="coolwarm", opacity=0.7)

# Add a title
p.add_text("Vent and Magma Chambers\nDamavand Volcano, Alborz")

# A nice perspective
p.camera_position = [
    (544065.5831913119, 3924518.576093113, 24324.3096344195),
    (597885.1732914157, 3982998.0900773173, -12587.537450058662),
    (0.33162714740718435, 0.26609487244915314, 0.9051060456978746),
]
p.show()
