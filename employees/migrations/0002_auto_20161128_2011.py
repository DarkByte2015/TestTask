# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 17:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='department',
            table='department',
        ),
        migrations.AlterModelTable(
            name='position',
            table='position',
        ),
    ]
