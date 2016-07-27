# Histstat

Histstat is a command line tool for obtaining live, rudimentary network connection data on a computer system. This tool was designed for network and security engineers to easily view connections on a system as they occur. In a world filled with noisy computers, Histstat can help someone quickly understand network connections that are happening on a system without having to dig into heaps of packet capture data. It can used to troubleshoot network issues, profile traffic on a system, and potentially find malicious activity.

### Requirements
* `Python 2.7`
* `psutil`

### Install
```
pip install psutil
git clone https://github.com/vesche/histstat && cd histstat
```

### Example Usage
```
$ python histstat.py -h
Usage: histstat - history for netstat
       https://github.com/vesche/histstat

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INTERVAL, --interval=INTERVAL
                        specify update interval in seconds (default: 1 sec)
  -l LOG, --log=LOG     log output to a text file
  -v, --verbose         verbose output

$ sudo python histstat.py -v -l log.txt
laddr           lport raddr           rport status      pid   pname        time     date     user         command             
0.0.0.0         22    *               *     LISTEN      194   sshd         23:34:15 16-07-26 root         /usr/bin/sshd -D    
192.168.1.181   41626 54.192.39.188   443   ESTABLISHED 6055  firefox      23:34:15 16-07-26 vesche       /usr/lib/firefox/firefox
192.168.1.181   45892 216.58.218.238  443   TIME_WAIT   -     -            23:34:15 16-07-26 -            -                   
::              22    *               *     LISTEN      194   sshd         23:34:15 16-07-26 root         /usr/bin/sshd -D    
192.168.1.181   37470 52.88.118.150   443   ESTABLISHED 6055  firefox      23:34:15 16-07-26 vesche       /usr/lib/firefox/firefox
192.168.1.181   37760 54.192.36.129   443   ESTABLISHED 6055  firefox      23:34:15 16-07-26 vesche       /usr/lib/firefox/firefox
192.168.1.181   46732 216.58.218.238  80    ESTABLISHED 6055  firefox      23:34:15 16-07-26 vesche       /usr/lib/firefox/firefox
192.168.1.181   46734 216.58.218.238  80    TIME_WAIT   -     -            23:34:15 16-07-26 -            -                   
0.0.0.0         68    *               *     NONE        1117  dhcpcd       23:34:15 16-07-26 root         /usr/bin/dhcpcd -4 -q -t 30 -L wlp1s0
0.0.0.0         1337  *               *     LISTEN      6293  nc           23:34:21 16-07-26 vesche       /usr/bin/netcat -l -p 1337
0.0.0.0         8080  *               *     LISTEN      6315  python2      23:34:23 16-07-26 root         /usr/bin/python2.7 -m SimpleHTTPServer 8080
192.168.1.181   52354 192.168.1.179   22    ESTABLISHED 6553  ssh          23:34:50 16-07-26 vesche       /usr/bin/ssh vesche@192.168.1.179
192.168.1.181   37470 52.88.118.150   443   TIME_WAIT   -     -            23:35:10 16-07-26 -            -                   
192.168.1.181   8080  192.168.1.179   39364 TIME_WAIT   -     -            23:35:28 16-07-26 -            -                   
```

### Todo
* output to csv
* verbosity options

### Thanks
Huge thanks to Giampaolo Rodola' (giampaolo) and all the contributers of [psutil](https://github.com/giampaolo/psutil) for the amazing open source library that this project relies upon completely.
