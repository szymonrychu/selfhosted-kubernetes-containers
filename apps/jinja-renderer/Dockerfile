FROM python:3.12.1-bookworm@sha256:603627dd8ce050329bce7741338ee9053e8004775d013603dd4ceefe42f99a82

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]