#!/bin/bash

COAP_BIN=$(which coap-client)
MY_IP=$(cat /proc/net/fib_trie | grep -B 1 '32 host LOCAL' | grep '|-- ' | sort | uniq | grep -v 127.0.0.1 | awk '{print $2}')

# generate /config if it does not exist (only for testing locally without the generator)
mkdir -p /config
echo $MY_IP >> /config/coap-udp.log

while $(/bin/true)
do
  $COAP_BIN -m get "coap://$TARGET_HOST/time"
  sleep $SEND_INTERVAL
done
