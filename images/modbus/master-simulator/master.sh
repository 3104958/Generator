#!/bin/bash

DIG_BIN=$(which dig)
TEST_BIN="/modpoll/x86_64-linux-gnu/modpoll"
SLAVE_HOST=$($DIG_BIN +short $TARGET_HOST)

$TEST_BIN -m tcp $SLAVE_HOST
