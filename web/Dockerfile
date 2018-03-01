# base container image
FROM python:3.6.1-alpine

# update system packages
RUN apk add --no-cache tzdata

# set environment variables for system
ENV TZ America/Los_Angeles

# set environment variables for application
ENV FLASK_CONFIG development

# setup working directory within container
RUN mkdir -p /web
WORKDIR /web

# copy requirements.txt for pip install
COPY requirements.txt /web/requirements.txt

# setup python environment, import required modules
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy code from current directory into working directory
COPY . /web
