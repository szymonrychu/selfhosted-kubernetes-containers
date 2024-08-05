FROM python:3.12.4-bookworm@sha256:40eb6aea06bc8f9f1bb1f8467dd1f06f57cb7eba38a70e65e2d26effeaf737e8

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]