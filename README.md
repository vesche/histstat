# histstat

This is a cross-platform command-line tool for obtaining live, rudimentary network connection data on a computer system. This tool was designed for network and security analysts to easily view connections on a system **as they occur**. It will display useful information about network connections that utilities like netstat typically won't give you such as what time the connection was made, the exact command that created the connection, and the user that connection was made by.

**Note for Windows users:** Detailed process information will not display unless you're running as `NT AUTHORITY\SYSTEM`. An easy way to drop into a system-level command prompt is to use PsExec from [SysInternals](https://technet.microsoft.com/en-us/sysinternals/bb842062.aspx). Run `psexec -i -s cmd.exe` as Administrator and then run histstat.

### Install

`pip install histstat`

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
date     time     proto laddr           lport raddr           rport status      user                 pid   pname                command
19-06-18 21:18:44 tcp   0.0.0.0         22    *               *     LISTEN      root                 650   sshd                 /usr/bin/sshd -D
19-06-18 21:18:44 udp   0.0.0.0         68    *               *     -           root                 647   dhcpcd               /usr/bin/dhcpcd -q -b
19-06-18 21:18:51 tcp   0.0.0.0         8000  *               *     LISTEN      vesche               5435  python               python -m http.server
19-06-18 21:19:11 tcp   0.0.0.0         1337  *               *     LISTEN      vesche               5602  ncat                 ncat -l -p 1337
19-06-18 21:19:26 tcp   127.0.0.1       39246 *               *     LISTEN      vesche               5772  electron             /usr/lib/electron/electron --nolazy --inspect=39246 /usr/lib/code/out/bootstrap-fork --type=extensionHost
19-06-18 21:19:28 tcp   10.13.37.114    43924 13.107.6.175    443   ESTABLISHED vesche               5689  code-oss             /usr/lib/electron/electron /usr/lib/code/code.js
...
```

### Thanks

Huge thanks to Giampaolo Rodola' (giampaolo) and all the contributers of [psutil](https://github.com/giampaolo/psutil) for the amazing open source library that this project relies upon completely.

Also, thanks to gleitz and his project [howdoi](https://github.com/gleitz/howdoi), in my refactor of histstat I modeled my code around his command line tool as the code is exceptionally clean and readable.
