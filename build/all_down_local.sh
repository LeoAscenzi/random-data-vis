#!/usr/bin/env bash
docker compose -f "../deployments/docker-compose.local.yml" down -v
docker stop consumer
docker rm consumer