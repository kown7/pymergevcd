#!/bin/bash

docker build -t sltoo:latest .
docker run sltoo:latest -name templateproject doit
docker cp templateproject:/app/artifacts .
docker rm templateproject

