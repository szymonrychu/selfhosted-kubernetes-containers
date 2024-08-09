FROM python:3.12.5-bookworm@sha256:ece3e93bb15459b7683aa1b205ab43086750cc64a088a948cf0a176f2166712c

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]