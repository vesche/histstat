#!/usr/bin/env python
# -*- coding: utf-8 -*-

# histstat - history for netstat
# https://github.com/vesche/histstat

from datetime import datetime
from optparse import OptionParser
from psutil import net_connections, Process
from socket import AF_INET, AF_INET6, SOCK_DGRAM, SOCK_STREAM
from time import sleep
try:
    from os import geteuid
except ImportError:
    from ctypes import *


class Histstat(object):
    def __init__(self, interval=1, log=False, verbose=False):
        super(Histstat, self).__init__()
        self.interval = interval
        self.log = log
        self.verbose = verbose
        self.log_format = "{:<5} {:<15.15} {:<5} {:<15.15} {:<5} {:<11} " \
        "{:<5} {:<12.12} {:<8} {:<8}"
        self.fields = ["proto", "laddr", "lport", "raddr", "rport", "status",
        "pid", "pname", "time", "date"]
        self.protocols = {
            (AF_INET, SOCK_STREAM): 'tcp',
            (AF_INET6, SOCK_STREAM): 'tcp6',
            (AF_INET, SOCK_DGRAM): 'udp',
            (AF_INET6, SOCK_DGRAM): 'udp6',
        }
        self.root_check = False

        if self.verbose:
            self.log_format += " {:<12.12} {}"
            self.fields += ["user", "command"]

    def histinit(self):
        header = ''
        try:
            if geteuid() == 0:
                self.root_check = True
        except NameError:
            if windll.shell32.IsUserAnAdmin() == 0:
                self.root_check = True
        if not self.root_check:
            header += "(Not all process information could be determined, run" \
            " as root to see everything.)\n"
        header += self.log_format.format(*self.fields)
        print header

        if self.log:
            with open(self.log, 'w') as f:
                f.write(header + '\n')

    def histout(self):
        connections_A = net_connections()
        for c in connections_A:
            self.process_conn(c)

        while True:
            sleep(self.interval)

            connections_B = net_connections()
            for c in connections_B:
                if c not in connections_A:
                    self.process_conn(c)

            connections_A = connections_B

    def process_conn(self, c):
        date, time = str(datetime.now()).split()

        proto = self.protocols[(c.family, c.type)]
        raddr = rport = '*'
        status = pid = pname = user = command = '-'
        laddr, lport = c.laddr
        if c.raddr:
            raddr, rport = c.raddr
        if c.pid:
            pname, pid = Process(c.pid).name(), str(c.pid)
        if c.pid and self.verbose:
            try:
                user = Process(c.pid).username()
                command = ' '.join(Process(c.pid).cmdline())
            except:
                pass
        if c.status != "NONE":
            status = c.status

        cfields = [proto, laddr, lport, raddr, rport, status, pid, pname,
        time[:8], date[2:]]
        if self.verbose:
            cfields += [user, command]
        line = self.log_format.format(*cfields)
        print line

        if self.log:
            with open(self.log, 'a') as f:
                f.write(line + '\n')


def main():
    help_text = "histstat - history for netstat\n\t\b" \
                "https://github.com/vesche/histstat"
    parser = OptionParser(usage=help_text, version="0.1")
    parser.add_option(
        "-i", "--interval", type="float", default=1,
        help="specify update interval in seconds (default: 1 sec)")
    parser.add_option(
        "-l", "--log", type="string", default=False,
        help="log output to a text file")
    parser.add_option(
        "-v", "--verbose", action="store_true", default=False,
        help="verbose output")

    options, _ = parser.parse_args()
    h = Histstat(interval=options.interval, verbose=options.verbose,
    log=options.log)

    h.histinit()
    h.histout()


if __name__ == "__main__":
    main()
