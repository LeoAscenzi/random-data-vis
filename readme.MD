# Order Book Sim

Visit the live site here: https://www.random-data-vis.xyz/

## Usage
- Specify the Count of data you want to send in a burst, and the Delay (seconds) between generating each message (approximately)
  - For maximum generation speed, use "-1" for the Delay
- Then click "Submit" and watch data be populated
  - Data is generated in a generator loop and send to Kafka
  - Consumer loop reads from Kafka
  - Web socket receives latest data

## Tech Specs
App consists of a few dockerized services running on an AWS t3.micro (so running these containers on your local machine will likely improve performance)
Use the [Docker Compose](https://github.com/LeoAscenzi/order-book-sim/blob/main/infra/deployments/docker-compose.yml) and [All Up](https://github.com/LeoAscenzi/order-book-sim/blob/main/infra/build/all_up.sh)/All Down scripts as templates to run the local version

The dockerized services are 
- Backend/Generate-Data -> Fast API app with confluent kafka connection
- Broker -> Apache Kafka's latest image
- Consumer -> Fast API with aiokafka/asyncio for queueing and consuming, uses websockets
- Nginx -> Reverse proxy and routing for domain name

The front end is react and hosted on Vercel
