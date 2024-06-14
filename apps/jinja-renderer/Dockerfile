FROM python:3.12.4-bookworm@sha256:69b5ed7edb7c70b0175a5099eccc86ceb5c0fe39ff94384403ceebc26de7f80e

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]