FROM ghcr.io/pyvista/pyvista:v0.33.2
MAINTAINER "Bane Sullivan"

COPY requirements.txt $HOME
RUN pip install -r requirements.txt

COPY notebooks $HOME