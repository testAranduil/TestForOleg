#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
import websrvr
from daemon import Daemon

class MyDaemon(Daemon):
    def run(self):
        websrvr.start()

if __name__ == "__main__": 
    my_daemon = MyDaemon('/var/run/webserver.pid')

    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            print 'starting webserver'
            my_daemon.start()
        elif 'stop' == sys.argv[1]:
            print 'stoping webserver'
            my_daemon.stop()
        elif 'restart' == sys.argv[1]:
            print 'restarting webserver'
            my_daemon.restart()
    else:
        print "Unknown command"
        sys.exit(2)
    sys.exit(0)