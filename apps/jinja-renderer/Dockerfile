FROM python:3.12.0-bookworm@sha256:80279fe4e7c4911e633ac5555b046e3afdcc7986e1c7d83d53dd3261e9f6f04c

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]