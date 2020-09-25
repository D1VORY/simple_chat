
FROM python:3.6.9
RUN apt-get update && \
    apt-get install -y gettext && \
    apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*
ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code


COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN pip install pipenv
RUN pipenv install --deploy --system
COPY . /code/
