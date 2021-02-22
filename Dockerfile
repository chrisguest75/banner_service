FROM ubuntu:20.04

RUN apt update && apt install jp2a python3.9 python3-pip -y

#FROM python:3.9.1-buster
#RUN apt update && apt install jp2a -y
#FROM python:3.9.1-alpine3.13
#RUN apk add --update --no-cache jp2a
#RUN apk update && apk add jp2a

RUN pip3 install pipenv

ARG USERID=1000
ARG GROUPID=1000
RUN addgroup --system --gid $GROUPID appuser
RUN adduser --system --uid $USERID --gid $GROUPID appuser


RUN mkdir -p /workbench/app

WORKDIR /workbench
RUN mkdir -p /workbench/out
COPY ./static /workbench/static
COPY ./Pipfile /workbench/Pipfile
COPY ./Pipfile.lock /workbench/Pipfile.lock 
RUN pipenv install --deploy --system --dev
COPY ./logging_config.yaml /workbench/logging_config.yaml
COPY ./fonts /workbench/fonts

COPY ./main.py /workbench/main.py
COPY ./app /workbench/app


# set to no debugger.
ENV DEBUGGER=False
ENV WAIT=False

#USER appuser
EXPOSE 8080
CMD ["python3", "-u", "./main.py"]