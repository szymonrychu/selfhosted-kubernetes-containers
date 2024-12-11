FROM python:3.13.1-bookworm@sha256:3b1b63f17c5197411ee572be110333dae4b9d6f2fbc4f84c790f644e791d356b

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]