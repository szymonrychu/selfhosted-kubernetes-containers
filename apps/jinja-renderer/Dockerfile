FROM python:3.13.2-bookworm@sha256:2e9b5da7a9c053568b33a47e3dc99798b4b9cc7b763be4e35f452262bd57703a

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]