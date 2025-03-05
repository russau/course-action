FROM python:3.12-bookworm

COPY entrypoint.py requirements.txt /

RUN apt update && \
    apt install zip && \
    pip3 install -r /requirements.txt

ENTRYPOINT ["python", "/entrypoint.py"]