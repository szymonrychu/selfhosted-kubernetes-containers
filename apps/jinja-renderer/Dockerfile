FROM python:3.13.1-bookworm@sha256:1db5e06d95506e4470e17024d56557acc2db62ae7fa4da3e638bf5fe6b0939b5

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]