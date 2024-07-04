FROM python:3.12.4-bookworm@sha256:70b2e244053eca39a645f0479619cbfb706ed5b4812bb4e94f9e94d9e0daff88

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]