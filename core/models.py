from django.db import models
from django.contrib.auth.models import User


class Unit(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    imei = models.CharField(max_length=128, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    user = models.ManyToManyField(User, related_name='units')

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.imei)

    def get_lastlocation(self):
        return False

    def get_lastseen(self):
        return False


class Message(models.Model):
    MESSAGE_TYPES = (
        (1, 'logon'),
        (2, 'heartbeat'),
        (3, 'low_battery'),
        (4, 'sos'),
        (5, 'tracker'))

    timestamp = models.DateTimeField(auto_now_add=True)
    unit = models.ForeignKey(Unit, related_name='messages')
    longitude = models.FloatField(blank=True)
    latitude = models.FloatField(blank=True)
    message_type = models.IntegerField(max_length=2,
                                       choices=MESSAGE_TYPES)

    def __unicode__(self):
        return '%s, %s (%s)' % (self.longitude, self.latitude, self.timestamp)
