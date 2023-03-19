FROM python:3.9 as base

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random

WORKDIR /code

###

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.3.2

RUN apt-get update && apt-get install -y gcc libffi-dev g++


RUN pip install --no-cache-dir "poetry==1.3.2"

RUN python -m venv /venv

COPY ./poetry.lock ./pyproject.toml ./

RUN poetry export -f requirements.txt --without-hashes | sed 's/; python.*$//' > requirements.txt

###

FROM base as final

ENV DEBIAN_FRONTEND noninteractive

COPY --from=builder /code/requirements.txt /code/requirements.txt 

RUN pip install ipython  # Not really a development dependency but good in the docker container
RUN apt-get update && apt-get install -y libgeos++-dev libgeos-c1v5 libgeos-dev libgeos-doc binutils libproj-dev gdal-bin proj-bin

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

EXPOSE 10200
