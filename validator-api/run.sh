#!/bin/bash

set -e

docker build -f ../gpu-pipeline/Dockerfile -t wombo-subnet:gpu-pipeline ../
docker build -f Dockerfile -t wombo-subnet:validator-api ../

docker run \
  --network="host" \
  --gpus=all \
  -v ~/.cache:/root/.cache/ \
  -it \
  --rm \
  wombo-subnet:validator-api \
