# coding=utf-8
import re
import time
from remoterun import SshClient


class LServer(SshClient):
    top = None
    conns = None
    diskusage = None
    topproc = None
    statusdic = {}
    keylist = {}
    # process_info = []

    def __init__(self,sshclient):
        self.sshclient = sshclient
        self.keylist = ['task_total', 'task_running', 'task_sleeping', 'task_stopped', 'task_zombie',
                        'cpu_us', 'cpu_sy', 'cpu_id',
                        'memtotal', 'memused', 'memusage',
                        'swaptotal', 'swapused', 'swapusage',
                        'diskusagedic',
                        'conns', 'processinfo']
        for i in self.keylist:
            self.statusdic[i] = ""

    def getstatus(self):
        """
        获得cpu,内存信息
        """
        out, err = self.sshclient.excute("/usr/bin/top -bcn 1|head -5")
        #self.top = out
        l = out.split("\n")
        # print 'l=',l
        rawstr = "Tasks:[\s]*?([\d]*?) total,[\s]*?([\d]*?) running,[\s]*?([\d]*?) sleeping,[\s]*?([\d]*?) stopped,[\s]*?([\d]*?) zombie"
        match_obj = re.search(rawstr, l[1].strip())
        all_groups = match_obj.groups()
        task_total, task_running, task_sleeping, task_stopped, task_zombie = all_groups
        rawstr = "Cpu\(s\):\s*?([\w\W]*?)[%\s]+us,[\s]*?([\w\W]*?)[%\s]+sy,[\s]*?([\w\W]*?)[%\s]+ni,[\s]*?([\w\W]*?)[%\s]+id,[\s]*?([\w\W]*?)[%\s]+wa,[\s]*?([\w\W]*?)[%\s]+hi,[\s]*?([\w\W]*?)[%\s]+si,[\s]*?([\w\W]*?)[%\s]+st"
        match_obj = re.search(rawstr, l[2].strip())
        cpu_us, cpu_sy, cpu_ni, cpu_id, cpu_wa, cpu_hi, cpu_si, cpu_st = match_obj.groups()
        rawstr = "Mem:[\s]*?([\w\W]*?)k? total,[\s]*([\w\W]*?)k? used,[\s]*([\w\W]*?)k? free,[\s]*?([\w\W]*?)k? buffers"
        match_obj = re.search(rawstr, l[3].strip())
        memtotal, memused, memfree, membuffer = match_obj.groups()

        rawstr = "Swap: ([\w\W]*?)k? total,[\s]*([\w\W]*?)k? used,[\s]*?([\w\W]*?)k? free[.,]+[\s]*?([\w\W]*?)k? cached"
        match_obj = re.search(rawstr, l[4].strip())
        swaptotal, swapused, swapfree, swapbuffer = match_obj.groups()



        # print "Task(total/run/sleep/stop/zombie): %s/%s/%s/%s/%s"%(total,running,sleeping,stopped,zombie)
        # print "CPU(user/system/idle): %s%%/%s%%/%s%%"%(us,sy,id)
        # print "Memory(total/used/usage): %sM/%sM/%s"%(int(memtotal)/1024/8,int(memused)/1024/8,str(float(memused)/float(memtotal)*100)[:4]+"%")
        # 可用内存 = mem_cache +mem_free + mem_buffer
        # 已用内存 = memtotal-membuffer- memfree - swapbuffer
        memtotal = int(memtotal) / 1024
        memused = int(memused) / 1024
        memfree = int(memfree) / 1024
        membuffer = int(membuffer) / 1024
        swapbuffer = int(swapbuffer) / 1024
        memusage = str(float(memtotal - membuffer - memfree- swapbuffer) / float(memtotal) * 100)[:4]
        # print "Swap(total/used/usage): %sM/%sM/%s"%(int(swaptotal)/1024/8,int(swapused)/1024/8,str(float(swapused)/float(swaptotal)*100)[:4]+"%")
        swaptotal = int(swaptotal) / 1024
        swapused = int(swapused) / 1024
        # swapusage = str(float(swapused) / float(swaptotal) * 100)[:4]
        for i in locals().keys():  
            if i in self.keylist:
                self.statusdic[i] = locals()[i]

    def getconnection(self):
        """
        获得连接数信息
        """
        out, err = self.sshclient.excute("netstat -anp|wc -l")
        conns = out.strip()
        for i in locals().keys():
            if i in self.keylist:
                self.statusdic[i] = locals()[i]

    def getdiskusage(self):
        """
        获得disk usage信息，实际上是照抄df -lh
        """
        out, err = self.sshclient.excute("df -lh")
        self.diskusage = out
        l = out.split("\n")
        # print l
        diskusagedic = {}
        count = 0
        tmpl = []
        for j in l[1:]:
            for i in j.split(" "):
                if i.strip() != "":
                    count += 1
                    tmpl.append(i.strip())
                    if count == 6:
                        mountpoint, total, used, free, usage, mounton = tmpl
                        diskusagedic[mounton] = [total, used, free, usage, mountpoint]
                        count = 0
                        tmpl = []
                        # print "Disk usage on %s: %s(total=%s,used=%s)" % (mounton.ljust(15, " "), usage.ljust(6, " "), total.ljust(6, " "), used)
        for i in locals().keys():
            if i in self.keylist:
                self.statusdic[i] = locals()[i]

    def getstatusdic(self):
        self.getstatus()
        self.getdiskusage()
        self.getconnection()
        return self.statusdic

    def getprocess(self,cmd):
        """
        获得进程信息
        """
        out, err = self.sshclient.excute(cmd)
        print out


if __name__ == "__main__":
    pass
