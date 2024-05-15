FROM python:3.12.3-bookworm@sha256:25dee7f137aa44c4962d21346385737eb81954b6f06f519fcc348b67f6483d3c

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]