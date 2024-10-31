FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -U pip && \
    pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./src /app

CMD guincorn main:app --workers 4 -- worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
