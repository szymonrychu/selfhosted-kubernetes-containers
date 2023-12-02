FROM python:3.12.0-bookworm@sha256:5eba34eb667213abb09a4c470365180d5706076f76945e49b963ac15d428a684

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]