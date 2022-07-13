#!/bin/bash

if [ -z "$HOSTIP" ] && [ -z "$FILEPATH" ]; then
    python client.py
elif ! [ -z "$PORT" ]; then
    python client.py -host ${HOSTIP} -f ${FILEPATH} -p ${PORT}
else
    python client.py -host ${HOSTIP} -f ${FILEPATH}
fi