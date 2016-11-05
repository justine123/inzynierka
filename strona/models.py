# from __future__ import unicode_literals

from django.db import models


class Sensor(models.Model):
    """
    Sensor, that has unique id, localisation, username & password
    """
    sensor_id = models.IntegerField()
    localisation = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=25)


class Entry(models.Model):
    """
    Single entry, connected to given sensor
    """
    sensor = models.ForeignKey(Sensor)
    date = models.DateTimeField
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    pollution = models.IntegerField()
    # TODO: inne dane pogodowe z zewnetrznego API?
