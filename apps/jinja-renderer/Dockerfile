FROM python:3.12.6-bookworm@sha256:096c49cf57695962d6d5e2998d0d23640b4234dfffcd8472d48adceb518582de

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]