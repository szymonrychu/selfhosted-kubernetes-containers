FROM python:3.13.1-bookworm@sha256:331d6556baf032897f36a9ef4b52688d7f4809d14927dab9fb2400651e4aaa89

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]