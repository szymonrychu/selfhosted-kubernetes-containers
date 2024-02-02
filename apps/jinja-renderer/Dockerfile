FROM python:3.12.1-bookworm@sha256:0ca7e92b1ed169c62683b131f49830fa198a2b9829e4741589bed83656ea7434

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]