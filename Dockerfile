FROM python:3.7-alpine
MAINTAINER Lotus Village Engineers

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /backend
WORKDIR /backend
COPY ./backend /backend

RUN adduser -D user
USER user