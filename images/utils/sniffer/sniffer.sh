#!/bin/bash

TCPDUMP_BIN=$(which tcpdump)
TCPDUMP_FILENAME=$(date -u +%s)-${SIM_NAME}_${INTERFACE_NAME}.pcap

$TCPDUMP_BIN -s0 -U -w /pcaps/$TCPDUMP_FILENAME  -i ${INTERFACE_NAME}
