#!/usr/bin/env bash
docker compose -f "../deployments/docker-compose.yml" build broker
docker compose -f "../deployments/docker-compose.yml" build generatedata
docker compose -f "../deployments/docker-compose.yml" build nginx
echo "Starting Kafka broker container and then waiting 3 seconds"
docker compose -f "../deployments/docker-compose.yml" up -d broker generatedata
sleep 2
echo "Kafka started, creating trade topics"
docker exec -it broker /opt/kafka/bin/kafka-topics.sh --create --topic trade-bids --bootstrap-server broker:29092
docker exec -it broker /opt/kafka/bin/kafka-topics.sh --create --topic trade-asks --bootstrap-server broker:29092
echo "Created trade topics, beginning producer loop in container"
sleep 3

docker build -t consumer:latest ../server/
docker run -d --network backend --name consumer consumer
sleep 3
docker compose -f "../deployments/docker-compose.yml" up -d nginx
