FROM python:3.12.1-bookworm@sha256:10a128c2d04fbc4c10f078fe27015517fc92c91347eeab6aeaefce26c0df7122

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]