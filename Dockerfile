FROM python:3.11-alpine
RUN apk update && apk add bash
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
ADD . .