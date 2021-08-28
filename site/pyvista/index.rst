PyVista
=======

This section of my website provides a guide to PyVista for geoscientists.
This content was adopted from sections of my graduate thesis and provides an
interactive way to learn PyVista from a geoscientist's perspective.



.. toctree::
   :hidden:

   tldr
   overview
   intro
   workflows
   wrapup
   examples/index
   The Paper <https://doi.org/10.21105/joss.01450>
   The Documentation <https://docs.pyvista.org>
   references


.. panels::

    Want the TL;DR?
    +++++++++++++++

    .. link-button:: tldr
        :type: ref
        :text: Read the Summary
        :classes: btn-outline-primary btn-block stretched-link

    ---

    Don't miss the included gallery of examples
    +++++++++++++++++++++++++++++++++++++++++++

    .. link-button:: examples/index
        :type: ref
        :text: See Gallery of Examples
        :classes: btn-outline-primary btn-block stretched-link


Abstract
--------

There is a wide range of data types present in typical hydrogeophysical studies; being able to gather all data types for a given project into a single framework is challenging and often unachievable at an affordable cost for hydrological researchers. Steep licensing fees for commercial software and complex user interfaces in existing open software have limited the accessibility of tools to build, integrate, and make decisions with diverse types of 3D geospatial data and models. In earth science research, particularly in hydrology, restricted budgets exacerbate these limitations, creating barriers for using software to manage, visualize, and exchange 3D data in reproducible workflows. In response to these challenges, I have created the PyVista software as an open-source framework for 3D geospatial data management, fusion, and visualization. The PyVista Python package provides an accessible and intuitive interface back to a robust and established visualization library, the Visualization Toolkit (VTK), to facilitate rapid analysis and visual integration of spatially referenced datasets. This interface implements spatial data structures encompassing a majority of subsurface applications to make creating, managing, and analyzing spatial data more streamlined for domain scientists. PyVista’s data management approach to 3D visualization furthers researchers’ ability to work across existing and emerging Python-based software while offering streamlined routines for creating publication-quality, integrated 3D visualizations. Example code to produce visualizations of 3D subsurface models, surface topography, sparse data, and other geospatial information are provided. These examples demonstrate how PyVista enables researchers to gather all of their spatial data into a single framework to rapidly visualize, explore, and gain insight from spatial data. PyVista is breaking down barriers for novice programmers hoping to use powerful, open-source, 3D software in reproducible geocomputing workflows.
