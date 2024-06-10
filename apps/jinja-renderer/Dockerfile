FROM python:3.12.4-bookworm@sha256:23155f230e6f43ecb0670dc680feb3271d96b9ce99fe82b051bf7b668755e2ef

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]