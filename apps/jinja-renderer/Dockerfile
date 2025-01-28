FROM python:3.13.1-bookworm@sha256:0a2cf88c3aa4ddafc15f7f0104d27fab3bd9f1468dc9e311ce056c857e540a06

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]