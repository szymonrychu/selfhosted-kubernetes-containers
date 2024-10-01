FROM python:3.12.6-bookworm@sha256:78409b7acdc408ff1dbdc936e246edcb07bba423581db47399f7db3ecad68852

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]