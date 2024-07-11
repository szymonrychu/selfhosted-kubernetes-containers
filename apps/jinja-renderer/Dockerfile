FROM python:3.12.4-bookworm@sha256:2c532e649905326835c73b86c89e1cbb3d1572c5331402d1013559058a22c33f

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]