# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 09:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20161019_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasourceuser',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_source_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_users',
            field=models.ManyToManyField(blank=True, through='projects.TaskAssignment', to='projects.DataSourceUser'),
        ),
        migrations.AlterField(
            model_name='taskassignment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_assignments', to='projects.DataSourceUser'),
        ),
    ]
