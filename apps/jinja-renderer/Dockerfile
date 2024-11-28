FROM python:3.13.0-bookworm@sha256:ecd27b6c43d8d84b0058e7db4aaa06a1bfe970d0fb9bb7cf39f9536850f71510

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]