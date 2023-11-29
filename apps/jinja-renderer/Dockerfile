FROM python:3.12.0-bookworm@sha256:ef2762997ab0a4b280dd3e30ab9ab97ae22170602b4f5358ee9a67ff7724968e

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]