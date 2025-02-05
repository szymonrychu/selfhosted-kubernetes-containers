FROM python:3.13.1-bookworm@sha256:328c5f9961773bd097e9a7a095f51ed8828d8ac04723fa6f389f9e46f10294f7

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]