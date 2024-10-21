FROM python:3.13.0-bookworm@sha256:feee4734fdc44cc09a3c9cdb72e05bb8ff7e964f64766bc1a68638b2c667cf35

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]