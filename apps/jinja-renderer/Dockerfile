FROM python:3.12.4-bookworm@sha256:08ac6c57f123d1ca5dd6c786cd7ceb4251733f98efe1697042e5d28b069916e7

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]