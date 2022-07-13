# Tails logs from Remote servers

## Overview

A client-server CLI program to tail(or fetch) logs from remote servers in real-time.

### Features

- Based on XML-RPC that's a is a Remote Procedure Call method that uses XML passed via HTTP as a transport. See more [here](https://docs.python.org/3/library/xmlrpc.html).
- An agent(or server) program that runs in the remote server and sends logs in real-time as requested by client.
- A client program that takes remote server IP and File path as parameters and display logs.

## Pre-requisites

- [Python 3](https://www.python.org/downloads/)
- [git](https://git-scm.com/downloads)
- [docker](https://docs.docker.com/engine/)

## Usage

First clone this repository using git

```text
git clone https://github.com/Ajaypathak372/remote-tail.git
cd remote-tail/
```

### Agent(or Server)

This program runs in the remote server and sends logs in real-time to the client program via RPC. This cannot be containerized as we need logs of the remote server not docker container.

```text
usage: agent.py [-h] [-host HOSTNAME] [-p PORT]

Tail logs from remote server

optional arguments:
  -h, --help            show this help message and exit
  -host HOSTNAME, --hostname HOSTNAME
                        Server Host, defaults to 127.0.0.1
  -p PORT, --port PORT  Server Port number, defaults to 8000
```

You can run this using `python` command or as a command-line tool. To run using python, do the following:

```text
cd agent/
python agent.py
```

By default, it runs on `localhost` and port 8000 but you can change them according to you own config by using `-host` and `-p` flags.

Best way is to use hostname as `0.0.0.0`, while running on remote servers.

```text
python agent.py -host 0.0.0.0
```

To use it as CLI, first update the python interpretor location at line 1 in `agent/agent.py`, then do the following:

```text
cd agent/
chmod +x agent.py
./agent.py -host 0.0.0.0
```

### Client

This will be used by the user to fetch logs from remote servers. User needs to proivde the remote server IP and File path, then it will asks agent to send real-time contents of the file as given by user.
To see running client using docker, skip to [this](#running-client-using-docker) section.

```text
usage: client.py [-h] [-p PORT] -host HOSTNAME -f FILEPATH

Tail logs from remote server

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Agent Port number, defaults to 8000

required arguments:
  -host HOSTNAME, --hostname HOSTNAME
                        Host IP Address
  -f FILEPATH, --filepath FILEPATH
                        Path where the file is located.
                        It should be the full path from the root directory, or relative path 
                        for example /var/log/syslog

```

> **Note:** Ensure Agent is up and running on remote servers.

It can also be used as command-line tool, same as done for the agent.

To run using `python`

```text
cd client/
python client.py -host <HOST IP> -f <File Path>
```

The above command will start displaying the logs in real-time.

## Running Client using Docker

You can also run client program using docker. So first, create the docker image of client program.

```text
cd remote-tail/
sudo docker build -t rtail-client:v1 .
```

For docker, you can use `HOSTIP`, `FILEPATH` and `PORT` as environmental variables to give arguments.
Now, run the docker container using the image create above as follows:

```text
sudo docker run -it -e HOSTIP="192.168.1.10" -e FILEPATH="/var/log/syslog" rtail-client:v1 
```
