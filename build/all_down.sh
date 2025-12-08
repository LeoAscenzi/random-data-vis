#!/usr/bin/env bash
docker compose -f "../deployments/docker-compose.yml" down -v
docker stop consumer
docker rm consumer
docker network rm backend