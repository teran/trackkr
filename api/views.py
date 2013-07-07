import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, HttpResponse, Http404
from django.template import RequestContext
from django.template.defaultfilters import timesince

from core.models import Unit, Message


@login_required
def lastpos(request, imei):
    unit = get_object_or_404(Unit, imei=imei)
    lastloc = unit.get_lastlocation()

    try:
        out = {
            'latitude': lastloc.latitude,
            'longitude': lastloc.longitude,
            'name': unit.name,
            'timestamp': unit.lastseen()
        }
    except:
        out = {
            'latitude': None,
            'longitude': None,
            'name': unit.name,
            'timestamp': None
        }

    return HttpResponse(content=json.dumps(out),
                        content_type='application/json')


@login_required
def location(request, messageid):
    message = get_object_or_404(Message, pk=messageid)

    return HttpResponse(content=json.dumps({'latitude': message.latitude,
                                            'longitude': message.longitude}),
                        content_type='application/json')


@login_required
def units(request):
    units = Unit.objects.filter(user=request.user)

    return HttpResponse(content=json.dumps([{'imei': unit.imei, 'name': unit.name} for unit in units]),
                        content_type='application/json')


@login_required
def recentpos(request):
    unit = Unit.objects.filter(user=request.user)
    lastloc = Message.objects.filter(~Q(latitude=None, longitude=None), unit__in=unit).order_by('-timestamp')[0]

    return HttpResponse(content=json.dumps({'latitude': lastloc.latitude,
                                            'longitude': lastloc.longitude}),
                        content_type='application/json')
