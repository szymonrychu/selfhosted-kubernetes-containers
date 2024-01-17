FROM python:3.12.1-bookworm@sha256:8b26b07158e2d95bf59bac794d648787ba365d92cdc3b31924600fef532d40ce

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]