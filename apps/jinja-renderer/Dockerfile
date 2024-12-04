FROM python:3.13.0-bookworm@sha256:91a40c9db8e53aa8c4cae96c24dc7135835e07c8140de233826ece4442ca8e29

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]