FROM python:3.12.1-bookworm@sha256:15a21aaeed99c218b600b9e01a99ccdbec7ffb57de00a445228fea18f04d7fbb

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]