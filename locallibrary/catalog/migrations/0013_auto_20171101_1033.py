# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-01 14:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_auto_20171101_0813'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request_message',
            old_name='is_accepted',
            new_name='is_viewed',
        ),
    ]
