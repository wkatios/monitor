# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-11-03 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20171103_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server_latest',
            fields=[
                ('serverip', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('servername', models.CharField(max_length=100)),
                ('serverinfo', models.TextField()),
                ('description', models.CharField(max_length=100)),
                ('createtime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updatetime', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
