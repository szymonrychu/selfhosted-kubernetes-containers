FROM python:3.13.0-bookworm@sha256:a680a0edc77501edf235bcc10e81b23269b7320bbf6067b457534cf199007601

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]