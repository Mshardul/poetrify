# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class RhymeWords(models.Model):
    id = models.IntegerField(primary_key=True)
    alphabet = models.CharField(max_length=1)
    word = models.CharField(unique=True, max_length=45)
    rhymingGroup = models.IntegerField(db_column='rhymingGroup', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RhymeWords'

class RhymeGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    words = models.CharField(max_length=450)

    class Meta:
        managed = False
        db_table = 'RhymeGroups'

class Approval(models.Model):
    id = models.IntegerField(primary_key=True)
    wordsList = models.CharField(db_column='wordsList', max_length=200)
    rhymes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Approval'


