FROM python:3.12.2-bookworm@sha256:20a673f2c7f7f895595f56c43cb8258681d939f65f62709b154190abeb8ae7e7

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]