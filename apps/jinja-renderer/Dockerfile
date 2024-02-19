FROM python:3.12.2-bookworm@sha256:a313e31ad26f3d8e6fb14dd0c6e2f181fa9c5bc099b21d93583035d04a3cc308

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]