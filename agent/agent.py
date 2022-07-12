#!/usr/bin/python3
# This runs on the computer(s) you want to read the file from
# Make sure to change out the HOST and PORT variables
HOST = '0.0.0.0'
PORT = 8000

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import os

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

def CreateServer():
   # Create server
   server = SimpleXMLRPCServer((HOST, PORT),
                               requestHandler=RequestHandler)

# register functions
   server.register_function(tail, 'tail')
   server.register_function(GetSize, 'GetSize')

   # Run the server's main loop
   server.serve_forever()

# start server
CreateServer()
