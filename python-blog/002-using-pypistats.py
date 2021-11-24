"""
Using PyPIstats
---------------

Not too long ago, I made a `pull request <https://github.com/hugovk/pypistats/pull/74>`_
to `PyPIstats <https://github.com/hugovk/pypistats>`_ to be able to make Pandas
:class:`DataFrame` objects of the download stats for any given project on PyPI.
It's a nifty little tool!

This example is mostly so that I can remember how to use PyPIstats and to have
a place where my favorite Python projects' stats are reported whenever my
website is automatically rebuilt.

Not much to see here unless you're interested in how many downloads my favorite
projects are getting lately.

"""

# sphinx_gallery_thumbnail_number = 1
import pypistats
import matplotlib.pyplot as plt


def fetch_and_plot(name):
    """A little helper method to do it all and make it pretty."""
    data = pypistats.overall(name, total=True, format="pandas")
    data = data.groupby("category").get_group("without_mirrors").sort_values("date")

    data.plot(x="date", y="downloads", figsize=(15, 5), marker="o")
    plt.xticks(
        rotation=45,
        horizontalalignment="right",
        fontweight="light",
        fontsize="medium",
    )
    plt.title("Downloads for {}".format(name))
    plt.tight_layout()
    return plt.show()


###############################################################################

fetch_and_plot("pyvista")

###############################################################################

fetch_and_plot("scooby")

###############################################################################

fetch_and_plot("flask-tileserver")

###############################################################################

fetch_and_plot("SimPEG")

###############################################################################

fetch_and_plot("PVGeo")

###############################################################################

fetch_and_plot("itkwidgets")

###############################################################################

fetch_and_plot("gempy")

###############################################################################

fetch_and_plot("omf")

###############################################################################

fetch_and_plot("omfvista")
