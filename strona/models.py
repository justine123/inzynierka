# from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models


class Sensor(models.Model):
    """
    Sensor, that has unique id, localisation, username & password
    It inherits after AbstractUser class because it's actually a model of user that logs in to the system
    """
    sensor_id = models.IntegerField(null=False)
    localisation = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=25)

    # USERNAME_FIELD = 'username'


class Entry(models.Model):
    """
    Single entry for readings from given sensors and weather API
    """
    sensor = models.ForeignKey(Sensor)
    date = models.DateTimeField()
    temperature = models.IntegerField(blank=True, null=True)
    humidity = models.IntegerField(blank=True, null=True)
    pm25 = models.FloatField(blank=True, null=True)
    pm10 = models.FloatField(blank=True, null=True)
    pressure = models.IntegerField(blank=True, null=True)
    wind_speed = models.FloatField(blank=True, null=True)
    wind_direction = models.IntegerField(blank=True, null=True)
