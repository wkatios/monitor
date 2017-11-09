"""
 run shell script on remote linux server via ssh

"""
__author__ = 'Administrator'

import paramiko
import time
import sys
import os
import logging
LOG = logging.getLogger('main')
# LOG.setLevel(logging.DEBUG)

class SshClient():
    sshclient = None
    sftpclient = None
    t = None

    def __init__(self, host, port, user, passwd):
        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        LOG.info("Connecting to %s" % host)
       # self.sshclient.connect(host, int(port), user, passwd)
        self.sshclient.connect(host, port, user, passwd)
        LOG.info("Now connected to %s" % host)
       # self.t = paramiko.Transport((host, int(port)))
  #      self.t = paramiko.Transport((host, port))
   #     self.t.connect(username=user, password=passwd)
  #      self.sftpclient = paramiko.SFTPClient.from_transport(self.t)

    def excute(self, cmd):
        # this doesnt work when executing shell script, no output got after the execution.
    #    print '[pyshell] excute command on server: %s' % cmd
        stdin, stdout, stderr = self.sshclient.exec_command(cmd)
        # print "[pyshell] returns:"
        out = stdout.read().strip()
        err = stderr.read().strip()
        # print "<"+"="*30
      #  print out
      #  print err,type(err),len(err)
        # print "="*30+">"
        return out, err

    def getfile(self, remotepath, localpath):
        now = time.time()
        print "[pyshell] download file %s to %s" % (remotepath, localpath)
        self.sftpclient.get(remotepath, localpath)
        print "[pyshell] download file finished. timecost = %s" % (time.time() - now)

    def putfile(self, remotepath, localpath):
        now = time.time()
        print "[pyshell] upload file %s to %s" % (localpath, remotepath)
        self.sftpclient.put(localpath, remotepath)
        print "[pyshell] upload file finished. timecost = %s" % (time.time() - now)

    def killprocess(self, process_keyword):
        # print sys._getframe().f_code.co_name, process_keyword
        channel = self.sshclient.get_transport().open_session()
        channel.exec_command("kill -9 `ps -fu root|grep /root/sock/UE.py|grep -v grep|awk '{print $2}'`")
        # cmd = "kill -9 `pgrep -f %s`" % process_keyword
        # self.excute(cmd)
        # print sys._getframe().f_code.co_name, " finished."

    def destroy(self):
       # self.close()
        self.sshclient.close()

    def exec_cmd(self, cmd):
        cmd_l = cmd.split(';')
        for i in cmd_l:
            a, b = self.excute(i)
        print "[pyshell]Excution Finished."

    def sftp_put(self, remotepath, localpath):
        self.putfile(remotepath, localpath)

    def sftp_get(self, remotepath, localpath):
        self.getfile(remotepath, localpath)


def run(argvs):
    try:
        tmp, host, port, user, passwd, mode, cmd, remotepath, localpath = argvs
        client = SshClient(host, port, user, passwd)
        if mode == "cmd":
            client.exec_cmd(cmd)
        elif mode == "put":
            client.sftp_put(remotepath, localpath)
        elif mode == "get":
            client.sftp_get(remotepath, localpath)
        else:
            print "unknown mode: %s" % mode
        client.destroy()
    except Exception, e:
        print e


if __name__ == "__main__":
    import sys

    argvs = sys.argv
    run(argvs)