# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-24 10:35
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(help_text='Commit hash or tag name', max_length=40)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(db_index=True, max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='TaskResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.CharField(choices=[('SSH', 'SSH')], max_length=30)),
                ('order', models.IntegerField(blank=True)),
                ('config', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('result', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(db_index=True, max_length=40)),
                ('deployment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_results', to='deployments.Deployment')),
            ],
        ),
    ]