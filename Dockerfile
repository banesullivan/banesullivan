FROM ghcr.io/pyvista/pyvista:v0.37.0

COPY requirements.txt $HOME
RUN pip install -r requirements.txt

COPY notebooks $HOME
