# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poetrify', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RhymeGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('words', models.CharField(max_length=450)),
            ],
            options={
                'db_table': 'RhymeGroups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RhymeWords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alphabet', models.CharField(max_length=1)),
                ('word', models.CharField(max_length=45, unique=True)),
                ('rhymingGroup', models.IntegerField(blank=True, db_column='rhymingGroup', null=True)),
            ],
            options={
                'db_table': 'RhymeWords',
                'managed': False,
            },
        ),
    ]
