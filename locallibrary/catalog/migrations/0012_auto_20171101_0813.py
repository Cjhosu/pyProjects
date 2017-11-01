# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-01 12:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20171028_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request_message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, default=None, null=True)),
                ('is_accepted', models.NullBooleanField(default=None)),
            ],
        ),
        migrations.RemoveField(
            model_name='item_request',
            name='message',
        ),
        migrations.AddField(
            model_name='request_message',
            name='request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Item_request'),
        ),
    ]
