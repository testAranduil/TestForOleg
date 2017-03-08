#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from time import gmtime, strftime

import syslog


path = '/home/webserver/webserver.log'

file = open(path, 'a+')
syslog.syslog(syslog.LOG_INFO, "Webserver process started")
file.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' -- process started' + "\n")
file.close()
file = open(path, 'a+')

output = ''

for line in file:
    output += line


class Handler(BaseHTTPRequestHandler):
    """ HTTP call """
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(output)
  
      
def start():
    """Start function"""
    server = HTTPServer(('',8080), Handler)
    server.serve_forever()
    syslog.syslog("Webserver process started")

if __name__ == '__main__':
    start()
