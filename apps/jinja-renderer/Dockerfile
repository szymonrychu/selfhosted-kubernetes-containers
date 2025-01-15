FROM python:3.13.1-bookworm@sha256:12e9e8924a63a19ae9508f5c36f436de4d724db87cbb846b5cf4c95e35b41080

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]