#!/usr/bin/python3

from xmlrpc import client
from argparse import RawTextHelpFormatter
import argparse
import time
import sys

def get_args():

    parser = argparse.ArgumentParser(description="Tail logs from remote server",
                                    formatter_class=RawTextHelpFormatter)
    parser.add_argument("-p", "--port",
                  dest="port",
                  default="8000",
                  help="Agent Port number, defaults to 8000")

    required = parser.add_argument_group("required arguments")
    required.add_argument("-host", "--hostname",
                  dest="hostname",
                  required=True,
                  help="Host IP Address")
    required.add_argument("-f", "--filepath",
                  dest="filepath",
                  required=True,
                  help="Path where the file is located.\nIt should be the full path from the root directory, or relative path \nfor example /var/log/syslog")

    return parser.parse_args()

def tail(filename, hostname, port):
    # connect to server
    location = "http://" + hostname + ":" + port
    s = client.ServerProxy(location)

    # get starting length of file
    curSeek = s.GetSize(filename)

    # constantly check
    while True:
        time.sleep(1) # make sure to sleep

        # get a new length of file and check for changes
        prevSeek = curSeek

        # some times it fails if the file is being writter to,
        # we'll wait another second for it to finish
        try:
            curSeek = s.GetSize(filename)
        except:
            pass

        # if file length has changed print it
        if prevSeek != curSeek:
            print(s.tail(filename, prevSeek))

def main():

    args = get_args()
    try:
        tail(args.filepath, args.hostname, args.port)
    except KeyboardInterrupt:
        print("\nStopped")
        sys.exit(0)
    except ConnectionError:
        print(f"[ERROR]: Connection refused, failed to connect to agent at {args.hostname}")
        sys.exit(111)
    except client.Fault as err:
        if err.faultString.find('FileNotFoundError'):
            print("[ERROR]: File not found, please enter a valid file path")
            sys.exit(2)
        else:
            print(err)
            sys.exit(1)

if __name__ == "__main__":
    main()
