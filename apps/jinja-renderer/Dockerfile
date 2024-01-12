FROM python:3.12.1-bookworm@sha256:64951f09b95e30651b929cfdb57a33593a427a69e604d4a5b8582c2469380093

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]