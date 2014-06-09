#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-23
@description:serverpool
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from easypool import ThreadPool
import subprocess
import shlex
import threading
import string

server_list = ['127.0.0.1', '127.0.0.1', '127.0.0.1']
serverpool = ThreadPool(server_list, send_item=True)
threadlock = threading.RLock()


def get_uptime(server):
    ssh_cmd = "ssh " + str(server) + " 'uptime'"
    ssh_cmd_list = shlex.split(ssh_cmd)
    p = subprocess.Popen(ssh_cmd_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    threadlock.acquire()
    print("Server: %s :: %s" % (server, stdout.rstrip()))
    threadlock.release()
    return

for i in range(6):
    serverpool.add_task(get_uptime)

serverpool.wait_completion()
