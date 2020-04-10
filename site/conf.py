# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config
import datetime
import sphinx_bootstrap_theme

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import make_news
make_news.make_news_gallery()


import pyvista
import numpy as np
# Manage errors
pyvista.set_error_output_file('errors.txt')
# Ensure that offscreen rendering is used for docs generation
pyvista.OFF_SCREEN = True # Not necessary - simply an insurance policy
# Preferred plotting style for documentation
pyvista.set_plot_theme('document')
pyvista.rcParams['window_size'] = np.array([1024, 768]) * 2


import warnings
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message='Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.',
)


# -- Project information -----------------------------------------------------
year = datetime.date.today().year
project = 'Bane Sullivan'
copyright = '{:d}, Bane Sullivan'.format(year)
author = 'Bane Sullivan'

# The full version, including alpha/beta/rc tags
release = '0.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_gallery.gen_gallery',
    'sphinx.ext.mathjax',
    'notfound.extension'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_title = project
html_short_title = ""
html_favicon = "_static/favicon.jpg"
html_extra_path = [".nojekyll"] #TODO: "CNAME",
html_use_smartypants = True
pygments_style = "friendly"
html_add_permalinks = ""

# Theme config
html_theme = "bootstrap"
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_theme_options = {
    "bootswatch_theme": "flatly",
    "navbar_title": "",
    "navbar_site_name": "Site",
    "navbar_links": [
        ("Home", "index"),
        ("About", "about"),
        ("Python", "python-blog/index"),
        ("News", "news"),
        ("Publications", "publications"),
    ],
    # Render the next and previous page links in navbar. (Default: true)
    "navbar_sidebarrel": False,
    # Render the current pages TOC in the navbar. (Default: true)
    "navbar_pagenav": False,
    # Tab name for the current pages TOC. (Default: "Page")
    "navbar_pagenav_name": "This page",
    # Global TOC depth for "site" navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    "globaltoc_depth": 1,
    # Include hidden TOCs in Site navbar?
    # Note: If this is "false", you cannot have mixed ``:hidden:`` and
    # non-hidden ``toctree`` directives in the same page, or else the build
    # will break.
    # Values: "true" (default) or "false"
    "globaltoc_includehidden": "false",
    # HTML navbar class (Default: "navbar") to attach to <div> element.
    # For black navbar, do "navbar navbar-inverse"
    "navbar_class": "navbar navbar-default",
    # Fix navigation bar to top of page?
    # Values: "true" (default) or "false"
    "navbar_fixed_top": "false",
    # Location of link to source.
    # Options are "nav" (default), "footer" or anything else to exclude.
    "source_link_position": "footer",
    "bootstrap_version": "3",
}
html_context = {
    "social_links": [
        (
            '<i class="fab fa-github fa-lg"></i>',
            "GitHub",
            "https://github.com/banesullivan",
        ),
        (
            '<i class="fas fa-envelope"></i>',
            "Email",
            "mailto:banesullivan@gmail.com",
        ),
        (
            '<i class="fab fa-twitter"></i>',
            "Twitter",
            "https://twitter.com/banesullivan",
        ),
    ],
    "url": "https://www.pyvista.org",
    "last_updated": str(datetime.date.today()),
    "repository": "pyvista/website",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Sphinx Gallery Options
from sphinx_gallery.sorting import FileNameSortKey

sphinx_gallery_conf = {
    # path to your examples scripts
    "examples_dirs": [
        "../python-blog/",
    ],
    # path where to save gallery generated examples
    "gallery_dirs": ["python-blog"],
    # Patter to search for example files
    "filename_pattern": r"\.py",
    # Remove the "Download all examples" button from the top level gallery
    "download_all_examples": False,
    # Sort gallery example by file name instead of number of lines (default)
    "within_subsection_order": FileNameSortKey,
    # directory where function granular galleries are stored
    "backreferences_dir": None,
    # Modules for which function level galleries are created.  In
    "doc_module": "pyvista",
    "image_scrapers": ('pyvista', 'matplotlib'),
    'first_notebook_cell': ("%matplotlib inline\n"
                            "from pyvista import set_plot_theme\n"
                            "set_plot_theme('document')"),
    "expected_failing_examples": "*",
}



# -- Custom 404 page
notfound_no_urls_prefix = True


# Load the custom CSS files (needs sphinx >= 1.6 for this to work)
def setup(app):
    app.add_css_file("style.css")
    app.add_css_file("fontawesome/css/all.css")
