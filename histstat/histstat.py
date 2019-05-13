#!/usr/bin/env python

"""
histstat, history for netstat
https://github.com/vesche/histstat
"""

import sys
import time
import psutil
import argparse
import datetime

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

__version__ = '1.1.1'

PROTOCOLS = {
    (AF_INET,  SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET,  SOCK_DGRAM):  'udp',
    (AF_INET6, SOCK_DGRAM):  'udp6'
}
FIELDS = ['proto', 'laddr', 'lport', 'raddr', 'rport', 'status', 'pid',
          'pname', 'time', 'date', 'user', 'command']
P_FIELDS = '{:<5} {:<15.15} {:<5} {:<15.15} {:<5} {:<11} {:<5} {:<20.20} ' \
           '{:<8} {:<8} {:<20.20} {}'


def histmain(interval):
    """Primary execution function for histstat."""

    # ladies and gentlemen this is your captain speaking
    output.preflight()

    # get initial connections
    connections_A = psutil.net_connections()
    for c in connections_A:
        output.process(process_conn(c))

    # primary loop
    while True:
        time.sleep(interval)

        connections_B = psutil.net_connections()
        for c in connections_B:
            if c not in connections_A:
                output.process(process_conn(c))

        connections_A = connections_B


def process_conn(c):
    """Process a psutil._common.sconn object into a list of raw data."""

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
        except: pass # if process closes during processing
    if c.status != 'NONE':
        status = c.status

    cfields = [proto, laddr, lport, raddr, rport, status, pid, pname,
               time[:8], date[2:], user, command]
    return cfields


class Output:
    """Handles all output for histstat."""

    def __init__(self, log, json_out, prettify):
        self.log = log
        self.json_out = json_out
        self.prettify = prettify

        if self.prettify and self.json_out:
            print('Error: Prettify output and JSON output cannot be used together.')
            sys.exit(2)

        if self.log:
            self.file_handle = open(self.log, 'a')

    def preflight(self):
        header = ''
        root_check = False

        if PLATFORM == 'nix':
            euid = geteuid()
            if euid == 0:
                root_check = True
            elif sys.platform == 'darwin':
                print('Error: histstat must be run as root on macOS.')
                sys.exit(3)
        elif PLATFORM == 'win':
            if windll.shell32.IsUserAnAdmin() == 0:
                root_check = True

        if not root_check:
            header += '(Not all process information could be determined, run' \
                    ' at a higher privilege level to see everything.)\n'

        if header:
            print(header)
        if not self.json_out:
            self.process(FIELDS)

    def process(self, cfields):
        if self.prettify:
            line = P_FIELDS.format(*cfields)
        elif self.json_out:
            line = dict(zip(FIELDS, cfields))
        else:
            line = '\t'.join(map(str, cfields))

        # output
        print(line)
        if self.log:
            self.file_handle.write(str(line) + '\n')


def get_parser():
    parser = argparse.ArgumentParser(description='history for netstat')
    parser.add_argument('-i', '--interval', help='specify update interval in seconds',
                        default=1, type=float)
    parser.add_argument('-l', '--log', help='log output to a text file',
                        default=None, type=str)
    parser.add_argument('-p', '--prettify', help='prettify output',
                        default=False, action='store_true')
    parser.add_argument('-j', '--json', help='json output',
                        default=False, action='store_true')
    parser.add_argument('-v', '--version', help='display the current version',
                        default=False, action='store_true')
    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    interval = args['interval']

    global output
    output = Output(
        log=args['log'],
        json_out=args['json'],
        prettify=args['prettify'],
    )

    try:
        histmain(interval)
    except KeyboardInterrupt:
        pass

    # gracefully stop histstat
    if output.log:
        output.file_handle.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
