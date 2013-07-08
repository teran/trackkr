import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
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
def location(request):
    try:
        imei = int(request.GET['imei'])
    except:
        units = Unit.objects.filter(user=request.user)
        out = []
        for unit in units:
            location = unit.get_lastlocation()

            if location is not None:
                out.append({
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'name': location.unit.name,
                    'timestamp': str(location.timestamp)
                })

        return HttpResponse(content=json.dumps(out),
                            content_type='application/json')

    if request.GET.has_key('message'):
        messageid = int(request.GET['message'])
        message = get_object_or_404(Message, pk=messageid, unit__imei=imei, unit__user=request.user)

        return HttpResponse(content=json.dumps({
            'longitude': message.longitude,
            'latitude': message.latitude,
            'name': message.unit.name,
            'timestamp': str(location.timestamp)
        }), content_type='application/json')
    else:
        unit = get_object_or_404(Unit, imei=imei, user=request.user)
        location = unit.get_lastlocation()

        try:
            return HttpResponse(content=json.dumps({
                'longitude': location.longitude,
                'latitude': location.latitude,
                'name': location.unit.name,
                'timestamp': str(location.timestamp)
            }), content_type='application/json')
        except:
            return HttpResponseBadRequest(content=json.dumps({
                'status': 'error',
                'reason': 'no options enough to complete query'
            }), content_type='application/json')


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
