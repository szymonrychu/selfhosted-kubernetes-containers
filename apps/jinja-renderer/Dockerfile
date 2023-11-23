FROM python:3.12.0-bookworm@sha256:439500d970f175a6df0fe92789fb8bb1f19cc1b806e6487f74a1d4e4c7beb63c

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]