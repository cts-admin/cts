# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-24 04:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fundraising', '0002_ctsdonor_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctsdonor',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile'),
        ),
    ]