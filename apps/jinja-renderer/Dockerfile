FROM python:3.12.1-bookworm@sha256:8c284a84bc273b858725193c1ea53192aa8cad6ca0ce3fd90b4abcfcd3cef915

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]