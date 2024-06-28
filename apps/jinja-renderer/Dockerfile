FROM python:3.12.4-bookworm@sha256:83f5f8714b6881d3e0e91023d9fe9e43aa6ad5a04e9f9a94ee180b18b021c72a

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]