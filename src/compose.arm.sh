#!/bin/sh

docker compose -p tmpl -f docker-compose.yml -f docker-compose.arm.override.yml up --build
