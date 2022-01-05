"""A helper script to generate the News gallery"""
import os


def format_icon(title, description, link, image):
    under = "+" * len(title)
    body = f"""

    ---
    :img-top: _static/news/{image}

    {description}

    .. link-button:: {link}
        :type: url
        :text: {title}
        :classes: btn-outline-primary btn-block stretched-link

"""
    return body


class News:
    def __init__(self, title, description, link, image):
        self.title = title
        self.description = description
        self.link = link
        self.image = image

    def format(self):
        return format_icon(self.title, self.description, self.link, self.image)


###############################################################################

articles = dict(
    radiant_earth=News(
        title="Radiant Earth Foundation's ML4EO Market News",
        description="My hobby project, localtileserver, was featured in Radiant Earth Foundation's ML4EO Market News.",
        link="https://www.radiant.earth/2022/01/04/december-2021-ml4eo-market-news/",
        image="radiant-earth.png",
    ),
    transform_2021=News(
        title="Transform 2021 Workshop",
        description="I instructed a workshop introducing PyVista as a visualization toolkit for geoscientists.",
        link="https://www.youtube.com/watch?v=FmNmRBsEBHE",
        image="transform-2021.png",
    ),
    mendenhall=News(
        title="Mendenhall Prize",
        description="I received the Mendenhall Prize for outstanding MSc Student in Geophysics (May 2020).",
        link="http://online.anyflip.com/vsibo/nqih/mobile/index.html",
        image="csm-geophysics.png",
    ),
    seequent=News(
        title="Future of geovisualization: discussion with Seequent",
        description="I recently sat down with Seequent to discuss the future of "
        "geovisualization and how I became involved in the 3D "
        "visualization and open-source software space.",
        link="https://www.seequent.com/blog/modern-geovisualisation",
        image="presenting-b.jpg",
    ),
    subsurface_frontiers=News(
        title="Introducing the Subsurface Frontiers Project",
        description="Here I appear in an informative video about the new Subsurface Frontiers Project.",
        link="https://youtu.be/5zrFU2-cgPo",
        image="subsurface-frontiers.png",
    ),
    undersampled=News(
        title="Featured on Undersampled Radio",
        description="I joined Matt and Gram on Undersampled Radio to talk about my work building next generation geoscience visualization technology. Tune in to the episode to hear us discuss viz, and more specifically geoviz.",
        link="https://youtu.be/FRHMDy37MPc",
        image="undersampled.png",
    ),
    gmg=News(
        title="Interview with Global Mining Guidelines Group",
        description="The Global Mining Guidelines Group recently interviewed me about efforts around the Open Mining Format. It's a neat article highlighting my work and the importance of open-source software in the geosciences!",
        link="https://gmggroup.org/omf-viewer-bane-sullivan/",
        image="omfvista-demo.gif",
    ),
    gdc=News(
        title="2019 Geothermal Student Competition",
        description="I lead a team that placed 2nd in the U.S. Department of Energy’s 2019 Geothermal Student Competition.",
        link="https://www.energy.gov/eere/articles/and-winners-2019-geothermal-student-competition-are",
        image="gsc_banner.jpg",
    ),
    agu_profile=News(
        title="AGU Profile on the Mines Geophysics Department",
        description="I briefly share some of my work bringing geophysical data into Virtual Reality for communication of findings.",
        link="https://youtu.be/IKYfCoTBA0E",
        image="agu-profile.png",
    ),
    simpeg=News(
        title="SimPEG Meeting, 6 Nov. 2018",
        description="I share my work on PVGeo, an open-source platform for visualizing geoscientific information and demo how this software is interoperable with the SimPEG projects.",
        link="https://youtu.be/35w1IWJtRAw",
        image="simpeg-meeting.png",
    ),
    senior_reflections=News(
        title="Mines 2018 Undergraduate Reflections",
        description="As a Colorado School of Mines senior, I reflect on my time at Mines, and give some insight into where I will go next.",
        link="https://youtu.be/m_wH_lK1FpE",
        image="senior-reflections.png",
    ),
)


###############################################################################


def make_news_gallery():
    filename = "./news.rst"
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "w") as f:
        f.write(
            """
News
====

Keep up with with my latest activities! I use this as a place to archive articles, features, awards, and more.


.. panels::

"""
        )
        for news in articles.values():
            f.write(news.format())

        f.write(
            """

A few extra
-----------

* `A Call to Accelerate Geothermal Innovation <https://www.innovationchallenge.com/challenges/from-the-us-department-of-energys-idaho-national-labs-a-call-to-accelerate-geothermal-innovation>`_

* `GMG’s Open Mining Format gaining traction in 2019 <https://im-mining.com/2019/02/01/gmgs-open-mining-format-gaining-traction-2019/>`_

"""
        )

    return
