FROM python:3.10-slim
ENV PYTHONBUFFERED 1
WORKDIR /code
COPY requirements.txt /code/requirements.txt
COPY . /code/
RUN apt-get update && apt-get -y install python-dev libpq-dev build-essential postgresql-client &&\
    pip install -r requirements.txt
RUN chmod +x wait-for-postgres.sh
