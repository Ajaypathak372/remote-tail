#!/bin/bash

if [ -z "$HOSTIP" ] && [ -z "$FILEPATH" ]; then
    python client.py
else
    python client.py -host ${HOSTIP} -f ${FILEPATH}
fi