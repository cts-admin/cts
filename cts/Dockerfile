FROM python:3

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgeoip1 \
    python-gdal

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/

RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' myuser

ADD . /code/