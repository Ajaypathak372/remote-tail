#!/usr/bin/python3

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import argparse
import sys
import os

def get_args():
    parser = argparse.ArgumentParser(description="Tail logs from remote server")

    parser.add_argument("-host", "--hostname",
                  dest="hostname",
                  default="127.0.0.1",
                  help="Server Host, defaults to 127.0.0.1")
    parser.add_argument("-p", "--port",
                  dest="port",
                  default=8000,
                  type=int,
                  help="Server Port number, defaults to 8000")

    return parser.parse_args()

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2')

def GetSize(filename):
    # get file size
    return os.stat(filename)[6]

def tail(filename, seek):
    #Set the filename and open the file
    f = open(filename,'r')

    #Find the size of the file and move to the end
    f.seek(seek)
    return f.read()

def CreateServer(hostname, port):
    # Create server
    server = SimpleXMLRPCServer((hostname, port),
                               requestHandler=RequestHandler)

    # register functions
    server.register_function(tail, 'tail')
    server.register_function(GetSize, 'GetSize')

    # Run the server's main loop
    print(f"Running at {hostname} on port {port}")
    server.serve_forever()

# start server
def main():
    args = get_args()
    try:
        CreateServer(args.hostname, args.port)
    except KeyboardInterrupt:
        print("\nStopped")
        sys.exit(0)

if __name__ == "__main__":
    main()
