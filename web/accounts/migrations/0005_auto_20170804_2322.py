# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20170804_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='second_name',
            field=models.CharField(default=None, max_length=128, null=True, verbose_name='second_name'),
        ),
    ]
