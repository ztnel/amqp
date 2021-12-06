#!/bin/bash
HOST="$(cut -d':' -f1<<<"$RABBITMQ_ADDR")"
PORT="$(cut -d':' -f2<<<"$RABBITMQ_ADDR")"
# wait for rabbitmq container
./wfi.sh -h "$HOST" -p "$PORT" -t 30

python3 -m p2