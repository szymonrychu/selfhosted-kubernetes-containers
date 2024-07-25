FROM python:3.12.4-bookworm@sha256:3d87cd922e0349f0c19676f492091cce77d79bf9bc9507e42e03bdb8e51126e1

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]