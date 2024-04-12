FROM python:3.12.3-bookworm@sha256:c6751fa575260522ca11fbad88394e12cbe31d0d8951d3d29301192745a09aab

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]