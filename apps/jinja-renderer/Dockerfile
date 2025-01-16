FROM python:3.13.1-bookworm@sha256:1320ae67bdc123c78ba664edf1b66faf94d6cc151e512676e457892dc047af71

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]