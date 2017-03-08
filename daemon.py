#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, atexit
from signal import SIGTERM
import syslog

class Daemon:
    def __init__(self, pidfile, stdin='/dev/null',  stdout='/dev/null', stderr='/dev/null'):
        """ Init method"""
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
  
    def daemonize(self):
        """creating a daemon here"""             
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            syslog.syslog(syslog.LOG_INFO, "Fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
  
        os.chdir(".")
        os.setsid()
        os.umask(0)
  
        # делаем второй fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            syslog.syslog(syslog.LOG_ERR, "Fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        
        syslog.syslog(syslog.LOG_INFO, "Webserver daemon start was successful")
        
            
        # перенаправление стандартного ввода/вывода
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
  
        # записываем pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
  
    def delpid(self):
        """removing pidfile"""
        os.remove(self.pidfile)

    def start(self):
        """ Starting a daemon """
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError, e:
            pid = None
            sys.stderr.write("IOerror" + e.strerror)
  
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
      
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stopping daemon
        """
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
  
        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return

        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        """restart daemon"""
        self.stop()
        self.start()

    def run(self):
        """ override it at the object """
