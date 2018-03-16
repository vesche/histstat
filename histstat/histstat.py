#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# histstat - history for netstat
# https://github.com/vesche/histstat
#

from . import __version__

import argparse
import datetime
import psutil
import time
import sys

from socket import AF_INET, AF_INET6, SOCK_DGRAM, SOCK_STREAM

if sys.platform.startswith('linux') or sys.platform == 'darwin':
    PLATFORM = 'nix'
    from os import geteuid
elif sys.platform.startswith('win'):
    PLATFORM = 'win'
    from ctypes import *
else:
    print('Error: Platform unsupported.')
    sys.exit(1)


PROTOCOLS = {
    (AF_INET,  SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET,  SOCK_DGRAM):  'udp',
    (AF_INET6, SOCK_DGRAM):  'udp6'
}
FIELDS = [ 'proto', 'laddr', 'lport', 'raddr', 'rport', 'status', 'pid',
           'pname', 'time', 'date', 'user', 'command' ]
P_FIELDS = '{:<5} {:<15.15} {:<5} {:<15.15} {:<5} {:<11} {:<5} {:<20.20} ' \
           '{:<8} {:<8} {:<20.20} {}'


def histinit():
    header = ''
    root_check = False

    if PLATFORM == 'nix':
        if geteuid() == 0:
            root_check = True
    elif PLATFORM == 'win':
        if windll.shell32.IsUserAnAdmin() == 0:
            root_check = True

    if not root_check:
        header += '(Not all process information could be determined, run' \
                  ' at a higher privilege level to see everything.)\n'

    if prettify:
        header += P_FIELDS.format(*FIELDS)
    else:
        header += '\t'.join(FIELDS)
    histlog(header)


def histmain(interval):
    connections_A = psutil.net_connections()
    for c in connections_A:
        histlog(process_conn(c))

    while True:
        time.sleep(interval)

        connections_B = psutil.net_connections()
        for c in connections_B:
            if c not in connections_A:
                histlog(process_conn(c))

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
            user = psutil.Process(c.pid).username()
            command = ' '.join(psutil.Process(c.pid).cmdline())
        except: # if process closes too quickly
            pass
    if c.status != 'NONE':
        status = c.status

    cfields = [ proto, laddr, lport, raddr, rport, status, pid, pname,
                time[:8], date[2:], user, command ]

    if prettify:
        line = P_FIELDS.format(*cfields)
    else:
        line = '\t'.join(map(str, cfields))
    return line


def histlog(line):
    print(line)

    if log:
        with open(log, 'a') as f:
            f.write(line + '\n')


def get_parser():
    parser = argparse.ArgumentParser(description='history for netstat')
    parser.add_argument('-i', '--interval',
                        help='specify update interval in seconds',
                        default=1, type=float)
    parser.add_argument('-l', '--log', help='log output to a text file',
                        default=False, type=str)
    parser.add_argument('-p', '--prettify', help='prettify output',
                        default=False, action='store_true')
    parser.add_argument('-v', '--version', help='display the current version',
                        default=False, action='store_true')

    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())

    interval = args['interval']

    if args['version']:
        print(__version__)
        return

    global log
    log = args['log']

    global prettify
    prettify = args['prettify']

    histinit()

    try:
        histmain(interval)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
