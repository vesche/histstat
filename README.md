# histstat

This is a cross-platform command-line tool for obtaining live, rudimentary network connection data on a computer system. This tool was designed for network and security analysts to easily view connections on a system **as they occur**. It will display useful information about network connections that utilities like netstat typically won't give you such as what time the connection was made, the exact command that created the connection, and the user that connection was made by.

**Note for Windows users:** Detailed process information will not display unless you're running as `NT AUTHORITY\SYSTEM`. An easy way to drop into a system-level command prompt is to use PsExec from [SysInternals](https://technet.microsoft.com/en-us/sysinternals/bb842062.aspx). Run `psexec -i -s cmd.exe` as Administrator and then run histstat.

### Install
Linux: `$ sudo pip install histstat`

Windows: `C:\>python -m pip install histstat`

### Example Usage
```
$ histstat --help
usage: histstat [-h] [-i INTERVAL] [-l LOG] [-p] [-j] [-v]

history for netstat

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        specify update interval in seconds
  -l LOG, --log LOG     log output to a text file
  -p, --prettify        prettify output
  -j, --json            json output
  -v, --version         display the current version

$ sudo histstat -p -l log.txt
proto laddr           lport raddr           rport status      pid   pname        time     date     user         command
tcp   192.168.1.137   58822 172.217.1.206   443   ESTABLISHED 14896 firefox      10:41:45 16-07-28 vesche       firefox
tcp   192.168.1.137   60176 192.30.253.124  443   ESTABLISHED 14896 firefox      10:41:45 16-07-28 vesche       firefox
tcp   192.168.1.137   59798 45.58.74.36     443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
tcp   192.168.1.137   40994 108.160.173.132 443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
tcp   192.168.1.137   40986 108.160.173.132 443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
tcp   192.168.1.137   41752 173.194.206.155 443   ESTABLISHED 14896 firefox      10:41:45 16-07-28 vesche       firefox
tcp   192.168.1.137   48396 198.41.209.142  443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
tcp   192.168.1.137   40978 108.160.173.132 443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
tcp   192.168.1.137   60130 192.30.253.124  443   ESTABLISHED 14896 firefox      10:41:45 16-07-28 vesche       firefox
tcp   192.168.1.137   40194 45.58.70.36     443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
tcp   192.168.1.137   32894 198.41.209.151  443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
tcp   192.168.1.137   60154 192.30.253.124  443   ESTABLISHED 14896 firefox      10:41:45 16-07-28 vesche       firefox
tcp   192.168.1.137   57808 45.58.70.4      443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
tcp   0.0.0.0         22    *               *     LISTEN      198   sshd         10:41:45 16-07-28 root         /usr/bin/sshd -D
tcp   192.168.1.137   39732 199.16.156.6    443   ESTABLISHED 14896 firefox      10:41:45 16-07-28 vesche       firefox
tcp   192.168.1.137   57816 45.58.70.4      443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
tcp   192.168.1.137   35508 104.16.107.25   443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
tcp   192.168.1.137   49674 198.41.208.122  443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
tcp   192.168.1.137   34076 162.125.4.1     443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
udp   0.0.0.0         68    *               *     -           362   dhcpcd       10:41:45 16-07-28 root         dhcpcd -4 -q -t 30 -L wlp1s0
tcp   192.168.1.137   49752 104.16.2.9      443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
tcp   192.168.1.137   40182 45.58.70.36     443   TIME_WAIT   -     -            10:41:45 16-07-28 -            -
tcp   0.0.0.0         2002  *               *     LISTEN      31327 nc           10:42:03 16-07-28 vesche       nc -l -p 2002
tcp   192.168.1.137   39600 10.4.0.11       22    ESTABLISHED 31975 ssh          10:42:59 16-07-28 vesche       ssh root@10.4.0.11
tcp   192.168.1.137   39600 10.4.0.11       22    TIME_WAIT   -     -            10:43:05 16-07-28 -            -
tcp   0.0.0.0         8080  *               *     LISTEN      32490 python2      10:43:49 16-07-28 root         python2 -m SimpleHTTPServer 8080
tcp   192.168.1.137   8080  192.168.1.137   45162 TIME_WAIT   -     -            10:44:12 16-07-28 -            -
```

### Thanks
Huge thanks to Giampaolo Rodola' (giampaolo) and all the contributers of [psutil](https://github.com/giampaolo/psutil) for the amazing open source library that this project relies upon completely.

Also, thanks to gleitz and his project [howdoi](https://github.com/gleitz/howdoi), in my refactor of histstat I modeled my code around his command line tool as the code is exceptionally clean and readable.
