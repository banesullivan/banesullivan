# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config
import datetime

import numpy as np
import pyvista

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
#
# sys.path.insert(0, os.path.abspath("."))
#
# import make_news
#
# make_news.make_news_gallery()


# Manage errors
pyvista.set_error_output_file("errors.txt")
# Ensure that offscreen rendering is used for docs generation
pyvista.OFF_SCREEN = True  # Not necessary - simply an insurance policy
pyvista.BUILDING_GALLERY = True
# Preferred plotting style for documentation
pyvista.set_plot_theme("document")
pyvista.rcParams["window_size"] = np.array([1024, 768]) * 2


import warnings

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.",
)


# -- Project information -----------------------------------------------------
year = datetime.date.today().year
project = "Bane Sullivan"
copyright = "2018-{:d}, Bane Sullivan".format(year)
author = "Bane Sullivan"

# The full version, including alpha/beta/rc tags
release = "0.0.0"

master_doc = 'source/index'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_gallery.gen_gallery",
    "sphinx.ext.mathjax",
    "notfound.extension",
    "sphinx_panels",
    "sphinxcontrib.bibtex",
]

bibtex_bibfiles = ["refs.bib"]

numfig = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_title = project
html_short_title = ""
html_favicon = "_static/favicon.jpg"
html_extra_path = [".nojekyll"]  # TODO: "CNAME",
html_use_smartypants = True
pygments_style = "friendly"
html_permalinks = False

# Theme config

html_theme = "pydata_sphinx_theme"
html_logo = None
# html_theme_path = [pydata_sphinx_theme.get_html_theme_path()]
html_context = {
    "github_user": "banesullivan",
    "github_repo": "mywebsite",
    "github_version": "main",
    "doc_path": "site",
    "last_updated": str(datetime.date.today()),
}
html_theme_options = {
    "google_analytics_id": "UA-115959679-2",
    "show_prev_next": False,
    "navigation_with_keys": False,
    "github_url": "https://github.com/banesullivan",
    "icon_links": [
        {
            "name": "Email",
            "url": "mailto:banesullivan@gmail.com",
            "icon": "fas fa-envelope",
        },
        {
            "name": "Twitter",
            "url": "https://twitter.com/banesullivan",
            "icon": "fab fa-twitter",
        },
    ],
}

html_sidebars = {
    "index": ["home-sidebar.html"],
    "about": ["home-sidebar.html"],
    "publications": ["home-sidebar.html"],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Sphinx Gallery Options
from sphinx_gallery.sorting import FileNameSortKey

sphinx_gallery_conf = {
    # path to your examples scripts
    "examples_dirs": [
        # "../python-blog/",
        "../pyvista-examples/",
    ],
    # path where to save gallery generated examples
    "gallery_dirs": [
        # "python-blog",
        "source/pyvista/examples",
    ],
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
    "image_scrapers": ("pyvista", "matplotlib"),
    "first_notebook_cell": (
        "%matplotlib inline\n" "from pyvista import set_plot_theme\n" "set_plot_theme('document')"
    ),
}


# -- Custom 404 page
notfound_no_urls_prefix = True


# Load the custom CSS files (needs sphinx >= 1.6 for this to work)
def setup(app):
    app.add_css_file("fontawesome/css/all.css")
