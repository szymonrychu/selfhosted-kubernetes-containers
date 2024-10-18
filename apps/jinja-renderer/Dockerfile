FROM python:3.13.0-bookworm@sha256:0eb8d3feda44654b7bc3e6e21dd19b793ce9eda75bbd0cf16a2407a1f0a4448b

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]