#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from monitor.models import Server, Server_latest, Topo
from utils import getinfo
import os
import ast
import json
import time
import requests
import logging
import ConfigParser
from utils import getinfo
from utils import remoterun

LOG = logging.getLogger('main')


conf = ConfigParser.ConfigParser()
conf_path = os.path.dirname(__file__) + '/config.ini'
conf.read(conf_path)
conf.hosttoip = json.loads(conf.get("DEFAULT", "nametoip"))
conf.physicalhost = list(set(conf.hosttoip.values()))
conf.iptohost = dict((value,[]) for key,value in conf.hosttoip.iteritems())
for key,value in conf.hosttoip.iteritems():
    conf.iptohost[value].append(key)
# print conf.iptohost

conf.user = conf.get("DEFAULT", "user")
conf.password = conf.get("DEFAULT", "password")

@csrf_exempt
def infomations(request):
    try:
        if request.method == 'POST':
            result = post_info(request)
        elif request.method == 'GET':
            result = get_info(request)
        return  HttpResponse(result)
    except Exception, e:
        LOG.error(e)
        return HttpResponse(json.dumps({'result': 'error', 'resmsg': 'requests method is not supported'}),
                                content_type='application/json')

def post_info(request):
    try:
        data = json.loads(request.body)
        ip = data['serverip']
        # save the latest data
        serverip = Server_latest.objects.filter(serverip = ip)
        if serverip.count() == 0:
            Server_latest.objects.create(serverip=ip, serverinfo = data)
        if serverip.count() == 1:
            serverip = Server_latest.objects.get(serverip=ip)
            serverip.serverinfo= data
            serverip.save()
        # save the history data
        Server.objects.create(serverip=ip, serverinfo=data)
        return HttpResponse(json.dumps({'result': 'success', 'resmsg': 'data is saved'}),
                            content_type='application/json')
    except Exception,e:
        LOG.error(e)
        return HttpResponse(json.dumps({'result': 'error', 'resmsg': 'data is unsaved, please check parameters'}),
                            content_type='application/json')

def get_info(request):
    try:
        ip = request.GET.get('ip','.*')   #<type 'unicode'>
        if request.GET.get('num') and request.GET.get('num').isdigit():
            num = request.GET.get('num')
        else:
            num = None
        # query history data
        if request.GET.get('status') and request.GET.get('status') == 'history':
            info = Server.objects.order_by('-updatetime').filter(serverip__regex = ip )[0:num]
        # query latest data
        elif request.GET.get('status') == 'latest':
            info = Server_latest.objects.filter(serverip__regex = ip)[0:num]
        else:
            LOG.error('parameter is not support')
            return HttpResponse(json.dumps({'result': 'error', 'resmsg': 'parameter is not support'}),
                                content_type='application/json')
        serversinfo = []
        for value in info.values():
            serverinfo = value['serverinfo']
            serverinfo = (ast.literal_eval(serverinfo))
            serversinfo.append(serverinfo)
        return HttpResponse(json.dumps({'result': 'success', 'resmsg': 'data success return',
                                        'data':serversinfo}),content_type='application/json')
    except Exception, e:
        LOG.error(e)
        return HttpResponse(json.dumps({'result': 'error', 'resmsg': 'data has not get, please check parameters'}),
                            content_type='application/json')

def getIp(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip

def osinfo(request):
    for server in conf.iptohost.keys():
        LOG.info(server)
        sshclient = remoterun.SshClient(server, 22, conf.user, conf.password)
        get_info = getinfo.LServer(sshclient)
        os_info = get_info.getstatusdic()
        os_info['serverip'] = server
        os_info['timestamp'] = int(time.time() * 1000)
        info = os_info
        if isinstance(os_info,dict):
            result = requests.post('http://127.0.0.1:8000/api/infomations/', data=json.dumps(os_info))
            LOG.info(result.json()['resmsg'])
    return HttpResponse(json.dumps(result.json()),content_type='application/json')

@csrf_exempt
def topo(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            topoid = data['topoid']
            Topo.objects.create(topoid=topoid, topoinfo=data)
            return HttpResponse(json.dumps({'result': 'success', 'resmsg': 'post data success'}),
                                content_type='application/json')
        elif request.method == 'GET':
            # topoid = request.GET.get('topoid', 1)
            info = Topo.objects.order_by('-createtime')[0].topoinfo
            info = (ast.literal_eval(info))
            return HttpResponse(json.dumps({'result': 'success', 'data': info}),
                                content_type='application/json')
    except Exception, e:
        LOG.error(e)
        return HttpResponse(json.dumps({'result': 'error', 'resmsg': '500, service has error'}),
                            content_type='application/json')
