FROM python:3.12.1-bookworm@sha256:ac2923eabdbe9ded711688588d865139e69ecd73676da2618b6363700a80f242

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY renderer.py /renderer.py

ENTRYPOINT ["/usr/local/bin/python3", "/renderer.py"]