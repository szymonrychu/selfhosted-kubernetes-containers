FROM python:3.12.4-bookworm@sha256:5776cc99a5a2d461295034fca2a233a69f8e6a0a42cd3042f79f851075bebd2e

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]