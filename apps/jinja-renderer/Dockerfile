FROM python:3.12.2-bookworm@sha256:afd493c07c454f712fde8f71f019ca9d0fafef50f99fcb3fbddc8543af0f89e6

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]