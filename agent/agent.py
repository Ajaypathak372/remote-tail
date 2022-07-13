#!/usr/bin/python3

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import argparse
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

def get_size(filename):
    # get file size
    return os.stat(filename)[6]

def tail(filename, seek):
    #Set the filename and open the file
    with open(filename,'r', encoding="utf-8") as file:
        #Find the size of the file and move to the end
        file.seek(seek)
        return file.read()

def create_server(hostname, port):
    # Create server
    server = SimpleXMLRPCServer((hostname, port),
                               requestHandler=RequestHandler)

    # register functions
    server.register_function(tail, 'tail')
    server.register_function(get_size, 'get_size')

    # Run the server's main loop
    print(f"Running at {hostname} on port {port}")
    server.serve_forever()

# start server
def main():
    args = get_args()
    try:
        create_server(args.hostname, args.port)
    except KeyboardInterrupt:
        print("\nStopped")

if __name__ == "__main__":
    main()
