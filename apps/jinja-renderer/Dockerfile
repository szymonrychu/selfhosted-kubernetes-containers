FROM python:3.12.7-bookworm@sha256:c7e6862f608cc58149ed6900a3f27ea3424661819cd610d010526ec6fc2e52a6

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]