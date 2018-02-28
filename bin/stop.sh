#!/bin/bash

BASEDIR=/Library/WebServer/docker-hub/flaskapp
docker-compose -f ${BASEDIR}/docker-compose.yml down
