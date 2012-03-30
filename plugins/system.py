import os
import re
import time
import psutil
import platform
from util import hook

def replace(text, wordDic):
    rc = re.compile('|'.join(map(re.escape, wordDic)))

    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub(translate, text)

def checkProc(checked_stats):
        status_file = open("/proc/%d/status" % os.getpid()).read()
        line_pairs = re.findall(r"^(\w+):\s*(.*)\s*$", status_file, re.M)
        status = dict(line_pairs)
        checked_stats = checked_stats.split()
        stats = '\x02, '.join(key + ': \x02' + status[key] for key in checked_stats)
        return stats

@hook.command("memory", autohelp=False)
@hook.command(autohelp=False)
def mem(inp):
    ".mem -- Displays the bot's current memory usage."
    if os.name == 'posix':
        checked_stats = 'Threads VmRSS VmSize VmPeak VmStk VmData'
        stats = checkProc(checked_stats)
        pretty_names = {'Threads': 'Active Threads', 'VmRSS': 'Real Memory', 'VmSize': 'Allocated Memory', 'VmPeak': 'Peak Allocated Memory', 'VmStk': 'Stack Size', 'VmData': 'Heap Size'}
        stats = replace(stats, pretty_names)
        return stats

    elif os.name == 'nt':
        cmd = "tasklist /FI \"PID eq %s\" /FO CSV /NH" % os.getpid()
        out = os.popen(cmd).read()
        total = 0
        for amount in re.findall(r'([,0-9]+) K', out):
            total += int(amount.replace(',', ''))
        return 'Memory Usage: \x02%s kB\x02' % total
    return 'error: operating system not currently supported'


@hook.command("up", autohelp=False)
@hook.command(autohelp=False)
def uptime(inp):
    proc = psutil.Process(os.getpid())
    up_time = proc.create_time
    up_time = time.time() - up_time
    up_time = time.localtime(up_time)
    up_time = time.strftime("Uptime: \x02%M:%S\x02", up_time)
    return up_time



@hook.command("system", autohelp=False)
@hook.command(autohelp=False)
def sys(inp):
    ".sys -- Retrieves information about the host system."
    python_version = platform.python_version()
    os = platform.platform(aliased=True)
    cpu = platform.machine()
    return "Platform: \x02%s\x02, Python Version: \x02%s\x02, CPU: \x02%s\x02" % (os, python_version, cpu)