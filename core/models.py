from django.db import models
from django.contrib.auth.models import User


class Unit(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    imei = models.CharField(max_length=128, unique=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, related_name='units', db_index=True)
    skip_empty_messages = models.BooleanField(default=False, db_index=True)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.imei)

    def get_lastlocation(self):
        try:
            return self.messages.filter(~models.Q(latitude=None, longitude=None)).order_by('-timestamp')[0]
        except:
            return None

    def get_lastseen(self):
        try:
            return self.messages.filter(~models.Q(latitude=None, longitude=None)).order_by('-timestamp')[0].timestamp
        except:
            return None


class Message(models.Model):
    MESSAGE_TYPES = (
        (1, 'logon'),
        (2, 'heartbeat'),
        (3, 'low_battery'),
        (4, 'sos'),
        (5, 'tracker'))

    timestamp = models.DateTimeField(auto_now_add=True)
    unit = models.ForeignKey(Unit, related_name='messages', db_index=True)
    longitude = models.FloatField(blank=True, null=True, db_index=True)
    latitude = models.FloatField(blank=True, null=True, db_index=True)
    message_type = models.IntegerField(max_length=2,
                                       choices=MESSAGE_TYPES)

    def __unicode__(self):
        return '%s, %s (%s)' % (self.longitude, self.latitude, self.timestamp)

    def position(self):
        return '%s, %s' % (self.longitude, self.latitude)
