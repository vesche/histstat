#!/usr/bin/env python
# -*- coding: utf-8 -*-

# histstat - history for netstat
# https://github.com/vesche/histstat

import argparse
import datetime
import psutil
import time

from socket import AF_INET, AF_INET6, SOCK_DGRAM, SOCK_STREAM

try:
    from os import geteuid
except ImportError:
    from ctypes import *


PROTOCOLS = {
    (AF_INET,  SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET,  SOCK_DGRAM):  'udp',
    (AF_INET6, SOCK_DGRAM):  'udp6'
}
FIELDS = [ "proto", "laddr", "lport", "raddr", "rport", "status", "pid",
           "pname", "time", "date" ]
PRETTIFY = "{:<5} {:<15.15} {:<5} {:<15.15} {:<5} {:<11} {:<5} {:<20.20} " \
           "{:<8} {:<8}"


def histinit():
    header = ''
    root_check = False
    
    try:
        if geteuid() == 0:
            root_check = True
    except NameError:
        if windll.shell32.IsUserAnAdmin() == 0:
            root_check = True
            
    if not root_check:
        header += "(Not all process information could be determined, run" \
        " at a higher privilege level to see everything.)\n"        
    header += PRETTIFY.format(*FIELDS)

    print header


def histout(interval):
    connections_A = psutil.net_connections()
    for c in connections_A:
        process_conn(c)

    while True:
        time.sleep(interval)

        connections_B = psutil.net_connections()
        for c in connections_B:
            if c not in connections_A:
                process_conn(c)

        connections_A = connections_B


def process_conn(c):
    date, time = str(datetime.datetime.now()).split()

    proto = PROTOCOLS[(c.family, c.type)]
    raddr = rport = '*'
    status = pid = pname = user = command = '-'
    laddr, lport = c.laddr
    
    if c.raddr:
        raddr, rport = c.raddr
    if c.pid:
        try:
            pname, pid = psutil.Process(c.pid).name(), str(c.pid)
        except:
            pass
    if c.status != "NONE":
        status = c.status

    cfields = [proto, laddr, lport, raddr, rport, status, pid, pname,
    time[:8], date[2:]]
    
    line = PRETTIFY.format(*cfields)
    print line


def get_parser():
    parser = argparse.ArgumentParser(description='history for netstat')
    parser.add_argument('-i', '--interval', help='specify update interval in seconds (default: 1 sec)', default=1, type=float)
    # parser.add_argument('-l', '--log', help='log output to a text file', type=string)
    # parser.add_argument('-v', '--verbose', help='verbose output')
    return parser


def command_line_runner():
    interval = 1
    # log = False
    # verbose = False
    
    parser = get_parser()
    args = vars(parser.parse_args())
    
    if args['interval']:
        interval = args['interval']
    
    #if args['log']:
    #    log = True
    
    #if args['verbose']:
    #    verbose = True
    
    histinit()
    histout(interval)
    

if __name__ == "__main__":
command_line_runner()