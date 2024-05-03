#!/bin/bash

docker compose down -v
docker rmi my_image
docker rmi docker_image
