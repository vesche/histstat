#!/usr/bin/env python

"""
histstat, history for netstat
https://github.com/vesche/histstat
"""

import os
import sys
import time
import psutil
import hashlib
import argparse
import datetime

from socket import AF_INET, AF_INET6, SOCK_DGRAM, SOCK_STREAM

__version__ = '1.2.0'

PROTOCOLS = {
    (AF_INET,  SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET,  SOCK_DGRAM):  'udp',
    (AF_INET6, SOCK_DGRAM):  'udp6'
}
FIELDS = [
    'date', 'time', 'proto', 'laddr', 'lport', 'raddr', 'rport', 'status',
    'user', 'pid', 'pname', 'command'
]
P_FIELDS = '{:<8} {:<8} {:<5} {:<15.15} {:<5} {:<15.15} {:<5} {:<11} ' \
           '{:<20.20} {:<5} {:<20.20} {}'
BUF_SIZE = 65536

if sys.platform.startswith('linux') or sys.platform == 'darwin':
    PLATFORM = 'nix'
    from os import geteuid
elif sys.platform.startswith('win'):
    PLATFORM = 'win'
    from ctypes import *
else:
    print('Error: Platform unsupported.')
    sys.exit(1)


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
        except:
            pass # if process closes during processing
    if c.status != 'NONE':
        status = c.status

    return [
        date[2:], time[:8], proto, laddr, lport, raddr, rport, status,
        user, pid, pname, command
    ]


def hash_file(path):
    """Hashes a file using MD5 and SHA256."""

    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5_hash.update(data)
            sha256_hash.update(data)
    return md5_hash.hexdigest(), sha256_hash.hexdigest()


class Output:
    """Handles all output for histstat."""

    def __init__(self, log, json_out, prettify, quiet, hash_mode):
        self.log = log
        self.json_out = json_out
        self.prettify = prettify
        self.quiet = quiet
        self.hash_mode = hash_mode

        if self.quiet and not self.log:
            print('Error: Quiet mode must be used with log mode.')
            sys.exit(1)

        if self.prettify and self.json_out:
            print('Error: Prettify and JSON output cannot be used together.')
            sys.exit(1)

        if self.log:
            self.file_handle = open(self.log, 'a')
            if quiet:
                print(f'Quiet mode enabled, see log file for results: {self.log}')

        if self.hash_mode:
            global FIELDS, P_FIELDS
            FIELDS = FIELDS[:-1] + ['md5', 'sha256', 'command']
            P_FIELDS = ' '.join(
                P_FIELDS.split()[:-1] + ['{:<32}', '{:<64}', '{}']
            )

    def preflight(self):
        root_check = False

        if PLATFORM == 'nix':
            euid = geteuid()
            if euid == 0:
                root_check = True
            elif sys.platform == 'darwin':
                print('Error: histstat must be run as root on macOS.')
                sys.exit(1)
        elif PLATFORM == 'win':
            if windll.shell32.IsUserAnAdmin() == 0:
                root_check = True

        # display netstat-esque privilege level header warning
        if not root_check:
            print('(Not all process information could be determined, run' \
                  ' at a higher privilege level to see everything.)\n')

        # display column names
        if not self.json_out:
            self.process(FIELDS)

    def process(self, cfields):
        if self.hash_mode:
            path = cfields[-1].split()[0]
            if os.path.isfile(path):
                md5_hash, sha256_hash = hash_file(path)
            else:
                md5_hash, sha256_hash = str(), str()
            cfields = cfields[:-1] + [md5_hash, sha256_hash, cfields[-1]]

        if self.prettify:
            line = P_FIELDS.format(*cfields)
        elif self.json_out:
            line = dict(zip(FIELDS, cfields))
        else:
            line = '\t'.join(map(str, cfields))

        # stdout
        if not self.quiet:
            print(line)
        if self.log:
            self.file_handle.write(str(line) + '\n')


def get_parser():
    parser = argparse.ArgumentParser(description='history for netstat')
    parser.add_argument(
        '-i', '--interval',
        help='specify update interval in seconds',
        default=1, type=float
    )
    parser.add_argument(
        '-j', '--json',
        help='json output',
        default=False, action='store_true'
    )
    parser.add_argument(
        '-l', '--log',
        help='log output to a file',
        default=None, type=str
    )
    parser.add_argument(
        '-p', '--prettify',
        help='prettify output',
        default=False, action='store_true'
    )
    parser.add_argument(
        '-q', '--quiet',
        help='quiet mode, do not output to stdout (for use when logging)',
        default=False, action='store_true'
    )
    parser.add_argument(
        '-v', '--version',
        help='display the current version',
        default=False, action='store_true'
    )
    parser.add_argument(
        '--hash',
        help='takes md5 and sha256 hashes of process files (warning: slow!)',
        default=False, action='store_true'
    )
    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return 0

    interval = args['interval']

    global output
    output = Output(
        log=args['log'],
        json_out=args['json'],
        prettify=args['prettify'],
        quiet=args['quiet'],
        hash_mode=args['hash']
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
