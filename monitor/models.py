from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Server(models.Model):
    serverip = models.CharField(max_length=100)
    servername = models.CharField(max_length=100)
    serverinfo = models.TextField()
    description = models.CharField(max_length=100)
    createtime = models.DateTimeField(auto_now_add=True, null=True)
    updatetime = models.DateTimeField(auto_now=True, null=True)

class Server_latest(models.Model):
    serverip = models.CharField(max_length=100, primary_key=True)
    servername = models.CharField(max_length=100)
    serverinfo = models.TextField()
    description = models.CharField(max_length=100)
    createtime = models.DateTimeField(auto_now_add=True, null=True)
    updatetime = models.DateTimeField(auto_now=True, null=True)


class Topo(models.Model):
    topoid = models.CharField(max_length=20)
    topoinfo = models.TextField()
    createtime = models.DateTimeField(auto_now_add=True, null=True)
    updatetime = models.DateTimeField(auto_now=True, null=True)