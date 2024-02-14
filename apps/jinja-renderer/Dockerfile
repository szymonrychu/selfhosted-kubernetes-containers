FROM python:3.12.2-bookworm@sha256:d443b31b2bf41559518eedaf62a3f798423c2c2ca348dcc5dd826353473add4d

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]