FROM python:3.12.2-bookworm@sha256:d68ff32657b444379b92c02db11934fe3e56556602662bc2981fc119a8b8b0cc

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]